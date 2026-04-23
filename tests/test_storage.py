from pathlib import Path

from phenotype.genome_importer import PersonalData
from phenotype.models import SNPRecord
from phenotype.storage import PhenotypeStore

FIXTURES = Path(__file__).parent / "fixtures"


def test_store_seeds_legacy_json_and_lists_rows(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    store.seed_from_legacy_files(FIXTURES / "scrapedData.small.json", tmp_path / "missing.json")

    rows = store.list_snps()

    assert len(rows) == 1
    assert rows[0]["Name"] == "rs1303"
    assert rows[0]["Gene"] == "EXAMPLE"
    assert rows[0]["ClinicalSignificance"] == "benign"
    assert rows[0]["RiskAllele"] == "A"
    assert rows[0]["FrequencyPercent"] == 10.0
    assert rows[0]["FrequencyDisplay"] == "10%"
    assert "ClassificationUpdatedAt" in rows[0]


def test_store_filters_by_genotype(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    store.upsert_snps([SNPRecord(rsid="rs1303", risk_allele="A", clinical_significance=["risk factor"])])
    store.upsert_genotypes({"rs1303": "(A;G)"})

    rows = store.list_snps(has_genotype=True)
    mutated = store.list_snps(mutated_only=True)

    assert len(rows) == 1
    assert len(mutated) == 1


def test_store_exposes_personal_significance_and_fixed_frequency(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    store.upsert_snps(
        [
            SNPRecord(
                rsid="rs1",
                frequency=".363",
                risk_allele="A",
                clinical_significance=["pathogenic"],
                classification_updated_at="2024-05-01",
            )
        ]
    )
    store.upsert_genotypes({"rs1": "AA"})

    row = store.list_snps()[0]

    assert row["FrequencyPercent"] == 36.3
    assert row["FrequencyDisplay"] == "36.3%"
    assert row["Significance"] == "Pathogenic match, common"
    assert row["SignificanceScore"] == 35
    assert row["ClinicalScore"] == 100
    assert row["FrequencyContext"] == "common"
    assert row["FindingSummary"] == "Pathogenic: unspecified condition"
    assert row["FindingSeverityClass"] == "pathogenic"
    assert row["ClinVarFindings"]
    assert row["IsRiskMatch"] is True
    assert row["AlleleOrientationNote"] == "No SNPedia genotype table is cached for this SNP."
    assert row["ClassificationUpdatedAt"] == "2024-05-01"


def test_store_does_not_use_scrape_time_as_classification_date(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    store.upsert_snps([SNPRecord(rsid="rs1", clinical_significance=["pathogenic"])])

    row = store.list_snps()[0]

    assert row["ClassificationUpdatedAt"] == ""
    assert row["SourceUpdatedAt"]


def test_store_reports_missing_cached_data(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    store.upsert_snps([SNPRecord(rsid="rs1"), SNPRecord(rsid="rs2", classification_updated_at="2025-01-01")])

    assert store.rsids_missing_annotations(["rs1", "rs3"]) == ["rs3"]
    assert store.rsids_missing_finding_dates(["rs1", "rs2", "rs3"]) == ["rs1", "rs3"]


def test_store_indexes_local_clinvar_and_builds_records(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    store.upsert_genotypes({"rs1": "(A;G)", "rs2": "(C;T)", "rs3": "(G;G)"})
    imported = store.replace_clinvar_variants(
        [
            {
                "rsid": "rs1",
                "allele_id": "10",
                "variation_id": "100",
                "gene": "GENE1",
                "clinical_significance": "Pathogenic",
                "last_evaluated": "2025-01-01",
                "rcv_accession": "RCV1",
                "phenotype_list": "Example disease",
                "assembly": "GRCh38",
                "alternate_allele": "G",
            },
            {
                "rsid": "rs2",
                "allele_id": "20",
                "variation_id": "200",
                "gene": "GENE2",
                "clinical_significance": "Benign",
                "last_evaluated": "2024-01-01",
                "phenotype_list": "Benign example",
                "assembly": "GRCh38",
            },
        ]
    )

    assert imported == 2
    assert store.annotation_stats()["clinvar_genotype_matches"] == 2
    assert store.annotation_stats()["clinvar_heterozygous_matches"] == 2
    assert store.annotation_stats()["clinvar_target_matches"] == 1
    assert store.clinvar_matched_rsids() == ["rs1"]
    assert store.clinvar_matched_rsids(targeted_only=False, heterozygous_only=True) == ["rs1", "rs2"]

    records = store.clinvar_records_for_rsids(["rs1"])
    assert records[0].rsid == "rs1"
    assert records[0].gene == "GENE1"
    assert records[0].clinvar == [["RCV1", "Pathogenic", "Example disease", "2025-01-01"]]
    assert records[0].source_urls["clinvar"].endswith("/100/")


def test_store_lists_unannotated_genotypes(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    store.upsert_genotypes({"rs1": "(A;G)", "rs2": "(C;T)"})
    store.upsert_snps([SNPRecord(rsid="rs1")])

    rows = store.list_unannotated_genotypes()

    assert [row["Name"] for row in rows] == ["rs2"]
    assert rows[0]["Genotype"] == "(C;T)"


def test_store_lists_normalized_genome_variants(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    personal = PersonalData(FIXTURES / "23andme_sample.txt", export_path=tmp_path / "yourData.json")

    store.upsert_genotypes(personal.yourData)
    count = store.upsert_genome_variants(personal.variants)
    rows = store.list_genome_variants(zygosity="heterozygous")
    stats = store.annotation_stats()

    assert count == 3
    assert [row["Name"] for row in rows] == ["rs1303"]
    assert rows[0]["Chromosome"] == "1"
    assert rows[0]["Position"] == 1000
    assert rows[0]["VariantAssembly"] == "GRCh37"
    assert stats["normalized_variants"] == 3
    assert stats["heterozygous_variants"] == 1

    path = store.export_vep_input(tmp_path / "vep.tsv", zygosity="heterozygous")
    assert path.read_text(encoding="utf-8").splitlines() == ["1\t1000\t1000\tA/G\t+\trs1303"]

    ids_path = store.export_vep_ids(tmp_path / "vep_ids.txt")
    assert ids_path.read_text(encoding="utf-8").splitlines() == ["rs1303", "rs1815739"]


def test_store_includes_normalized_variant_metadata_in_snp_rows(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    personal = PersonalData(FIXTURES / "23andme_sample.txt", export_path=tmp_path / "yourData.json")
    store.upsert_genotypes(personal.yourData)
    store.upsert_genome_variants(personal.variants)
    store.upsert_snps([SNPRecord(rsid="rs1303", variations=[["(A;G)", "2", "risk note"]])])

    row = store.list_snps(promethease_only=True)[0]

    assert row["Chromosome"] == "1"
    assert row["Position"] == 1000
    assert row["VariantZygosity"] == "heterozygous"
    assert row["VariantAssembly"] == "GRCh37"


def test_store_uses_exact_rsid_search_when_query_is_rsid(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    store.upsert_genotypes({"rs1208": "(A;G)", "rs12085366": "(C;T)"})
    store.upsert_snps([SNPRecord(rsid="rs1208"), SNPRecord(rsid="rs12085366", gene="GENE2")])

    rows = store.list_snps(search="rs1208", has_genotype=True)

    assert [row["Name"] for row in rows] == ["rs1208"]


def test_store_filters_normalized_variants_by_listed_allele_match(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    personal = PersonalData(FIXTURES / "23andme_sample.txt", export_path=tmp_path / "yourData.json")
    store.upsert_genome_variants(personal.variants)
    store.upsert_snps(
        [
            SNPRecord(rsid="rs1303", risk_allele="G", clinical_significance=["risk factor"]),
            SNPRecord(rsid="rs1815739", risk_allele="C", clinical_significance=["benign"]),
        ]
    )

    rows = store.list_genome_variants(mutated_only=True)

    assert [row["Name"] for row in rows] == ["rs1303"]
    assert rows[0]["IsRiskMatch"] is True


def test_store_filters_normalized_variants_by_snpedia_genotype_risk_note(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    personal = PersonalData(FIXTURES / "23andme_sample.txt", export_path=tmp_path / "yourData.json")
    store.upsert_genome_variants(personal.variants)
    store.upsert_snps(
        [
            SNPRecord(rsid="rs1303", clinical_significance=["benign"], variations=[["(A;G)", "2.8", "risk note"]]),
            SNPRecord(rsid="rs1815739", risk_allele="C", clinical_significance=["benign"]),
        ]
    )

    rows = store.list_genome_variants(mutated_only=True)

    assert [row["Name"] for row in rows] == ["rs1303"]
    assert rows[0]["SNPediaMatchedFinding"]["severity_class"] == "risk"


def test_store_separates_clinical_and_promethease_style_filters(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    store.upsert_genotypes({"rs1": "(A;G)", "rs2": "(C;T)"})
    store.upsert_snps(
        [
            SNPRecord(rsid="rs1", risk_allele="A", clinical_significance=["risk factor"]),
            SNPRecord(rsid="rs2", variations=[["(C;T)", "2.5", "trait note"]]),
        ]
    )

    clinical = store.list_snps(clinical_match_only=True)
    promethease = store.list_snps(promethease_only=True)

    assert [row["Name"] for row in clinical] == ["rs1"]
    assert {row["Name"] for row in promethease} == {"rs1", "rs2"}


def test_store_imports_and_filters_vep_consequences(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    personal = PersonalData(FIXTURES / "23andme_sample.txt", export_path=tmp_path / "yourData.json")
    store.upsert_genome_variants(personal.variants)

    imported = store.replace_vep_consequences(
        [
            {
                "rsid": "rs1303",
                "uploaded_variation": "rs1303",
                "location": "1:1000",
                "allele": "G",
                "gene": "ENSG1",
                "feature": "ENST1",
                "feature_type": "Transcript",
                "consequence": "missense_variant",
                "impact": "MODERATE",
                "symbol": "GENE1",
            }
        ]
    )
    rows = store.list_genome_variants(vep_impact="MODERATE")
    missense = store.list_genome_variants(vep_consequence="missense")
    stats = store.annotation_stats()

    assert imported == 1
    assert [row["Name"] for row in rows] == ["rs1303"]
    assert rows[0]["VepImpact"] == "MODERATE"
    assert rows[0]["VepConsequence"] == "missense_variant"
    assert rows[0]["VepSymbol"] == "GENE1"
    assert [row["Name"] for row in missense] == ["rs1303"]
    assert stats["vep_consequence_rows"] == 1
    assert stats["vep_moderate_rsids"] == 1


def test_store_tracks_scrape_items(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    run_id = store.create_scrape_run(2, "test run", ["rs1", "rs2"])

    store.set_scrape_item_status(run_id, "rs2", "failed", "boom")
    run = store.get_scrape_run(run_id)

    assert run["total"] == 2
    assert store.scrape_items_by_status(run_id, ["failed"]) == ["rs2"]
    assert len(run["items"]) == 2


def test_store_marks_interrupted_runs_failed(tmp_path):
    store = PhenotypeStore(tmp_path / "phenotype.sqlite")
    run_id = store.create_scrape_run(1, "test run", ["rs1"])
    store.set_scrape_item_status(run_id, "rs1", "running")

    store.mark_interrupted_runs()
    run = store.get_scrape_run(run_id)

    assert run["status"] == "failed"
    assert run["items"][0]["status"] == "failed"
