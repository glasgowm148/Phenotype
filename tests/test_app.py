from pathlib import Path

from phenotype.app import create_app

FIXTURES = Path(__file__).parent / "fixtures"


def test_api_lists_snps(tmp_path):
    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    app.config["PHENOTYPE_STORE"].seed_from_legacy_files(FIXTURES / "scrapedData.small.json", tmp_path / "missing.json")
    client = app.test_client()

    response = client.get("/api/snps?limit=5")

    assert response.status_code == 200
    assert response.get_json()["count"] >= 1


def test_home_route_serves_app_shell(tmp_path):
    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"Upload genome" in response.data
    assert b"Loaded:" in response.data
    assert b"Build 37 variants" in response.data
    assert b"x;y" in response.data
    assert b"x;x" in response.data
    assert b"Highest magnitude" in response.data
    assert b"Recent findings" in response.data
    assert b"New" in response.data
    assert b"Most publications" in response.data
    assert b"Clear" in response.data
    assert b"Refresh finding dates" in response.data
    assert b"Import ClinVar DB" in response.data
    assert b"Scan x;y ClinVar matches" in response.data
    assert b"Import VEP" in response.data
    assert b"Import report HTML" in response.data
    assert b"Export VEP x;y" in response.data
    assert b"Export VEP rsids" in response.data
    assert b"High impact" in response.data
    assert b"Moderate impact" in response.data
    assert b"Missense" in response.data
    assert b"Splice" in response.data
    assert b"Stop gained" in response.data
    assert b"Unannotated" in response.data
    assert b"Finding date" in response.data
    assert b"SNPedia risk note" in response.data
    assert b"ClinVar findings" in response.data
    assert b"Clinical" in response.data
    assert b"Findings" in response.data
    assert b"Source only" in response.data
    assert b"Clinical match" in response.data
    assert b"Genotype match" in response.data
    assert b"Update SNPedia" in response.data
    assert b"Update genosets" in response.data
    assert b"Promethease-style" not in response.data
    assert b"Pathogenic" in response.data
    assert b"Risk factor" in response.data
    assert b"Drug response" in response.data
    assert b"Uncertain" in response.data
    assert b"Benign" in response.data
    assert b"kendo" not in response.data.lower()


def test_old_vendor_asset_routes_are_removed(tmp_path):
    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    client = app.test_client()

    assert client.get("/js/kendo.all.min.js").status_code == 404
    assert client.get("/css/kendo.material.min.css").status_code == 404


def test_stats_reports_annotation_coverage(tmp_path):
    from phenotype.models import SNPRecord

    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    store = app.config["PHENOTYPE_STORE"]
    store.upsert_genotypes({"rs1": "(A;G)", "rs2": "(C;T)"})
    store.upsert_snps([SNPRecord(rsid="rs1", clinvar=[["RCV1", "Pathogenic", "Condition"]])])

    response = app.test_client().get("/api/stats")

    assert response.status_code == 200
    assert response.get_json() == {
        "annotated_genotypes": 1,
        "cached_snps": 1,
        "cached_with_clinvar": 1,
        "cached_with_finding_dates": 0,
        "clinvar_genotype_matches": 0,
        "clinvar_heterozygous_matches": 0,
        "clinvar_reference_rows": 0,
        "clinvar_reference_rsids": 0,
        "clinvar_target_matches": 0,
        "heterozygous_variants": 0,
        "homozygous_variants": 0,
        "imported_genotypes": 2,
        "no_call_variants": 0,
        "normalized_variants": 0,
        "unannotated_genotypes": 1,
        "vep_consequence_rows": 0,
        "vep_consequence_rsids": 0,
        "vep_high_rsids": 0,
        "vep_moderate_rsids": 0,
    }


def test_backlog_lists_unannotated_genotypes(tmp_path):
    from phenotype.models import SNPRecord

    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    store = app.config["PHENOTYPE_STORE"]
    store.upsert_genotypes({"rs1": "(A;G)", "rs2": "(C;T)"})
    store.upsert_snps([SNPRecord(rsid="rs1")])

    response = app.test_client().get("/api/backlog")

    assert response.status_code == 200
    rows = response.get_json()["results"]
    assert len(rows) == 1
    assert rows[0]["Name"] == "rs2"
    assert rows[0]["FindingSummary"] == "No cached annotation yet"


def test_new_since_import_filters_recent_findings(tmp_path):
    from phenotype.models import SNPRecord

    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    store = app.config["PHENOTYPE_STORE"]
    store.upsert_genotypes({"rs1": "(A;G)"})
    store.upsert_snps(
        [SNPRecord(rsid="rs1", risk_allele="A", clinical_significance=["pathogenic"], classification_updated_at="2099-01-01")]
    )

    response = app.test_client().get("/api/snps?new_since_import_only=1&clinical_match_only=1")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["count"] == 1
    assert [row["Name"] for row in payload["results"]] == ["rs1"]


def test_severity_filter_pulls_full_benign_set(tmp_path):
    from phenotype.models import SNPRecord

    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    store = app.config["PHENOTYPE_STORE"]
    store.upsert_genotypes({"rs1": "(A;G)", "rs2": "(A;G)", "rs3": "(A;G)"})
    store.upsert_snps(
        [
            SNPRecord(rsid="rs1", clinical_significance=["benign"]),
            SNPRecord(rsid="rs2", clinical_significance=["benign"]),
            SNPRecord(rsid="rs3", clinical_significance=["pathogenic"]),
        ]
    )

    response = app.test_client().get("/api/snps?severity_filters=benign&has_genotype=1")

    assert response.status_code == 200
    payload = response.get_json()
    assert payload["count"] == 2
    assert {row["Name"] for row in payload["results"]} == {"rs1", "rs2"}


def test_variants_api_lists_normalized_build37_rows(tmp_path):
    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    store = app.config["PHENOTYPE_STORE"]

    from phenotype.genome_importer import PersonalData
    from phenotype.models import SNPRecord

    personal = PersonalData(FIXTURES / "23andme_sample.txt", export_path=tmp_path / "yourData.json")
    store.upsert_genotypes(personal.yourData)
    store.upsert_genome_variants(personal.variants)
    store.upsert_snps(
        [
            SNPRecord(rsid="rs1303", risk_allele="G", clinical_significance=["risk factor"]),
            SNPRecord(rsid="rs1815739", risk_allele="T", clinical_significance=["risk factor"]),
        ]
    )

    response = app.test_client().get("/api/variants?zygosity=heterozygous")
    matched = app.test_client().get("/api/variants?mutated_only=1")

    assert response.status_code == 200
    rows = response.get_json()["results"]
    assert [row["Name"] for row in rows] == ["rs1303"]
    assert rows[0]["Chromosome"] == "1"
    assert rows[0]["Position"] == 1000
    assert rows[0]["VariantZygosity"] == "heterozygous"
    assert [row["Name"] for row in matched.get_json()["results"]] == ["rs1303"]


def test_vep_export_uses_normalized_build37_rows(tmp_path):
    from phenotype.genome_importer import PersonalData

    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    store = app.config["PHENOTYPE_STORE"]
    personal = PersonalData(FIXTURES / "23andme_sample.txt", export_path=tmp_path / "yourData.json")
    store.upsert_genotypes(personal.yourData)
    store.upsert_genome_variants(personal.variants)

    response = app.test_client().get("/api/export-vep.tsv?zygosity=heterozygous")

    assert response.status_code == 200
    assert response.data.decode("utf-8").splitlines() == ["1\t1000\t1000\tA/G\t+\trs1303"]


def test_vep_rsid_export_uses_normalized_build37_rows(tmp_path):
    from phenotype.genome_importer import PersonalData

    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    store = app.config["PHENOTYPE_STORE"]
    personal = PersonalData(FIXTURES / "23andme_sample.txt", export_path=tmp_path / "yourData.json")
    store.upsert_genotypes(personal.yourData)
    store.upsert_genome_variants(personal.variants)

    response = app.test_client().get("/api/export-vep-rsids.txt")

    assert response.status_code == 200
    assert response.data.decode("utf-8").splitlines() == ["rs1303", "rs1815739"]


def test_vep_import_endpoint_caches_consequences(tmp_path):
    import io

    from phenotype.genome_importer import PersonalData

    app = create_app(
        tmp_path / "phenotype.sqlite",
        genotypes_path=tmp_path / "yourData.json",
        upload_dir=tmp_path / "uploads",
        seed_legacy=False,
    )
    store = app.config["PHENOTYPE_STORE"]
    personal = PersonalData(FIXTURES / "23andme_sample.txt", export_path=tmp_path / "yourData.json")
    store.upsert_genome_variants(personal.variants)
    text = (
        "#Uploaded_variation\tLocation\tAllele\tGene\tFeature\tFeature_type\tConsequence\tExisting_variation\tExtra\n"
        "rs1303\t1:1000\tG\tENSG1\tENST1\tTranscript\tmissense_variant\trs1303\tIMPACT=MODERATE;SYMBOL=GENE1\n"
    )

    response = app.test_client().post(
        "/api/vep/import",
        data={"vep": (io.BytesIO(text.encode("utf-8")), "vep.txt")},
    )
    variants = app.test_client().get("/api/variants?vep_impact=MODERATE")

    assert response.status_code == 200
    assert response.get_json() == {"imported": 1}
    rows = variants.get_json()["results"]
    assert [row["Name"] for row in rows] == ["rs1303"]
    assert rows[0]["VepConsequence"] == "missense_variant"


def test_report_import_endpoint_caches_bad_findings(tmp_path):
    import base64
    import io
    import json
    import zlib

    app = create_app(
        tmp_path / "phenotype.sqlite",
        genotypes_path=tmp_path / "yourData.json",
        upload_dir=tmp_path / "uploads",
        seed_legacy=False,
    )
    app.config["PHENOTYPE_STORE"].upsert_genotypes({"rs1": "(A;G)"})
    payload = base64.b64encode(
        zlib.compress(
            json.dumps(
                [
                    {
                        "rsnum": "rs1",
                        "geno": "(A;G)",
                        "repute": "Bad",
                        "magnitude": 2.5,
                        "genosummary": "risk note",
                    }
                ]
            ).encode("utf-8")
        )
    ).decode("ascii")
    html = f"mygenos.push.apply(mygenos,decompressString('{payload}'));"

    response = app.test_client().post(
        "/api/report/import",
        data={"report": (io.BytesIO(html.encode("utf-8")), "report.html")},
    )

    assert response.status_code == 200
    assert response.get_json() == {"imported": 1, "metadata": 1}
    assert app.config["PHENOTYPE_STORE"].get_snp("rs1")["SNPediaMatchedFinding"]["note"] == "risk note"
    assert app.config["PHENOTYPE_STORE"].get_snp("rs1")["SNPediaMatchedFinding"]["repute"] == "Bad"


def test_upload_imports_genotypes(tmp_path):
    app = create_app(
        tmp_path / "phenotype.sqlite",
        genotypes_path=tmp_path / "yourData.json",
        upload_dir=tmp_path / "uploads",
        seed_legacy=False,
    )
    client = app.test_client()

    with (FIXTURES / "23andme_sample.txt").open("rb") as file:
        response = client.post("/api/import", data={"genome": (file, "23andme_sample.txt")})

    assert response.status_code == 200
    assert response.get_json()["imported"] == 3


def test_scrape_run_detail_and_retry_failed(tmp_path, monkeypatch):
    from phenotype.models import SNPRecord

    monkeypatch.setattr("phenotype.app.fetch_snp_record", lambda rsid: SNPRecord(rsid=rsid))
    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    store = app.config["PHENOTYPE_STORE"]
    run_id = store.create_scrape_run(2, "test", ["rs1", "rs2"])
    store.set_scrape_item_status(run_id, "rs1", "complete")
    store.set_scrape_item_status(run_id, "rs2", "failed", "boom")
    client = app.test_client()

    detail = client.get(f"/api/scrape-runs/{run_id}")
    retry = client.post(f"/api/scrape-runs/{run_id}/retry-failed")

    assert detail.status_code == 200
    assert len(detail.get_json()["items"]) == 2
    assert retry.status_code == 202
    assert retry.get_json()["total"] == 1


def test_scrape_skips_cached_annotations(tmp_path, monkeypatch):
    from phenotype.models import SNPRecord

    monkeypatch.setattr("phenotype.app.fetch_snp_record", lambda rsid: SNPRecord(rsid=rsid))
    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    app.config["PHENOTYPE_STORE"].upsert_snps([SNPRecord(rsid="rs1")])
    client = app.test_client()

    response = client.post("/api/scrape", json={"rsids": ["rs1"]})

    assert response.status_code == 200
    assert response.get_json() == {"cached": 1, "run_id": None, "total": 0}


def test_refresh_findings_skips_cached_dates(tmp_path):
    from phenotype.models import SNPRecord

    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    app.config["PHENOTYPE_STORE"].upsert_snps([SNPRecord(rsid="rs1", classification_updated_at="2025-01-01")])
    client = app.test_client()

    response = client.post("/api/refresh-findings", json={"rsids": ["rs1"]})

    assert response.status_code == 200
    assert response.get_json() == {"cached": 1, "run_id": None, "total": 0}


def test_pause_and_cancel_scrape_run_requests(tmp_path):
    app = create_app(tmp_path / "phenotype.sqlite", genotypes_path=tmp_path / "yourData.json", seed_legacy=False)
    store = app.config["PHENOTYPE_STORE"]
    run_id = store.create_scrape_run(1, "test", ["rs1"])
    client = app.test_client()

    pause = client.post(f"/api/scrape-runs/{run_id}/pause")
    assert pause.status_code == 200
    assert store.get_scrape_requested_status(run_id) == "pause"

    store.update_scrape_run(run_id, "running", 0, 0)
    cancel = client.post(f"/api/scrape-runs/{run_id}/cancel")
    assert cancel.status_code == 200
    assert store.get_scrape_requested_status(run_id) == "cancel"
