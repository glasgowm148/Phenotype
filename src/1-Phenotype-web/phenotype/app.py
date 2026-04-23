from __future__ import annotations

import tempfile
import threading
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file, send_from_directory

from phenotype.clinvar_local import download_variant_summary, iter_variant_summary
from phenotype.genome_importer import PersonalData
from phenotype.models import SNPRecord, normalize_rsid
from phenotype.paths import APP_DIR, DATA_DIR, DEFAULT_DB_PATH, DEFAULT_GENOTYPES_JSON, UPLOAD_DIR
from phenotype.providers.combined import fetch_snp_record
from phenotype.providers.myvariant import fetch_myvariant_record
from phenotype.providers.snpedia_ncbi import snpedia_url
from phenotype.scraper import build_rsid_list
from phenotype.snpedia_catalog import (
    fetch_matching_genotype_finding,
    fetch_matching_known_genosets,
    iter_bad_genotype_findings,
    matches_imported_genotype,
)
from phenotype.storage import PhenotypeStore
from phenotype.vep import iter_vep_tab


def create_app(
    database_path: str | Path = DEFAULT_DB_PATH,
    genotypes_path: str | Path = DEFAULT_GENOTYPES_JSON,
    upload_dir: str | Path = UPLOAD_DIR,
    export_dir: str | Path | None = None,
    seed_legacy: bool = True,
) -> Flask:
    app = Flask(__name__, template_folder=str(APP_DIR / "templates"))
    app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024
    store = PhenotypeStore(database_path)
    genotypes_path = Path(genotypes_path)
    upload_dir = Path(upload_dir)
    export_dir = Path(export_dir) if export_dir is not None else (DATA_DIR / "exports" if seed_legacy else Path(database_path).parent / "exports")
    store.mark_interrupted_runs()
    if seed_legacy:
        store.seed_from_legacy_files(genotypes_path=genotypes_path)
    app.config["PHENOTYPE_STORE"] = store

    @app.route("/", methods=["GET", "POST"])
    def main():
        return render_template("snp_resource.html")

    @app.route("/api/rsids", methods=["GET"])
    @app.route("/api/snps", methods=["GET"])
    def get_snps():
        rows = store.list_snps(
            search=request.args.get("search", ""),
            has_genotype=_flag("has_genotype"),
            mutated_only=_flag("mutated_only"),
            clinical_match_only=_flag("clinical_match_only"),
            promethease_only=_flag("promethease_only"),
            limit=_int_arg("limit", 1000),
            offset=_int_arg("offset", 0),
        )
        return jsonify({"results": rows, "count": len(rows)})

    @app.route("/api/variants", methods=["GET"])
    def get_variants():
        rows = store.list_genome_variants(
            search=request.args.get("search", ""),
            zygosity=request.args.get("zygosity", ""),
            clinical_only=_flag("clinical_only"),
            annotated_only=_flag("annotated_only"),
            mutated_only=_flag("mutated_only"),
            clinical_match_only=_flag("clinical_match_only"),
            promethease_only=_flag("promethease_only"),
            vep_impact=request.args.get("vep_impact", ""),
            vep_consequence=request.args.get("vep_consequence", ""),
            limit=_int_arg("limit", 1000),
            offset=_int_arg("offset", 0),
        )
        return jsonify({"results": rows, "count": len(rows)})

    @app.route("/api/snps/<rsid>", methods=["GET"])
    def get_snp(rsid: str):
        row = store.get_snp(rsid)
        if not row:
            return jsonify({"error": "not found"}), 404
        return jsonify(row)

    @app.route("/api/stats", methods=["GET"])
    def get_stats():
        return jsonify(store.annotation_stats())

    @app.route("/api/backlog", methods=["GET"])
    def get_backlog():
        rows = store.list_unannotated_genotypes(
            search=request.args.get("search", ""),
            limit=_int_arg("limit", 1000),
            offset=_int_arg("offset", 0),
        )
        return jsonify({"results": rows, "count": len(rows)})

    @app.route("/api/clinvar/import", methods=["POST"])
    def import_clinvar_reference():
        payload = request.get_json(silent=True) or {}
        run_id = store.create_scrape_run(1, "ClinVar local import")
        thread = threading.Thread(
            target=_run_clinvar_import,
            args=(store, run_id, _bool_payload(payload, "force", False)),
            daemon=True,
        )
        thread.start()
        return jsonify({"run_id": run_id, "total": 1}), 202

    @app.route("/api/clinvar/scan", methods=["POST"])
    def scan_clinvar_matches():
        payload = request.get_json(silent=True) or {}
        rsids = store.clinvar_matched_rsids(
            targeted_only=_bool_payload(payload, "targeted_only", True),
            heterozygous_only=_bool_payload(payload, "heterozygous_only", False),
            missing_only=_bool_payload(payload, "missing_only", False),
            limit=_int_payload(payload, "limit", 20000),
        )
        if not rsids:
            return jsonify({"run_id": None, "total": 0, "cached": 0}), 200
        run_id = store.create_scrape_run(len(rsids), "ClinVar genotype scan", rsids)
        thread = threading.Thread(target=_run_clinvar_scan, args=(store, run_id, rsids), daemon=True)
        thread.start()
        return jsonify({"run_id": run_id, "total": len(rsids)}), 202

    @app.route("/api/snpedia/bad-genotypes/import", methods=["POST"])
    def import_snpedia_bad_genotypes():
        payload = request.get_json(silent=True) or {}
        run_id = store.create_scrape_run(0, "SNPedia bad genotype catalogue")
        thread = threading.Thread(
            target=_run_snpedia_bad_catalog_import,
            args=(store, run_id, _int_payload(payload, "limit", 0)),
            daemon=True,
        )
        thread.start()
        return jsonify({"run_id": run_id}), 202

    @app.route("/api/snpedia/genosets/import", methods=["POST"])
    def import_snpedia_genosets():
        run_id = store.create_scrape_run(0, "SNPedia genoset scan")
        thread = threading.Thread(target=_run_snpedia_genoset_import, args=(store, run_id), daemon=True)
        thread.start()
        return jsonify({"run_id": run_id}), 202

    @app.route("/api/vep/import", methods=["POST"])
    def import_vep_results():
        upload = request.files.get("vep")
        if not upload or not upload.filename:
            return jsonify({"error": "missing VEP output file"}), 400
        upload_dir.mkdir(parents=True, exist_ok=True)
        suffix = Path(upload.filename).suffix or ".txt"
        with tempfile.NamedTemporaryFile(delete=False, dir=upload_dir, suffix=suffix) as temp:
            upload.save(temp.name)
            temp_path = Path(temp.name)
        count = store.replace_vep_consequences(iter_vep_tab(temp_path))
        return jsonify({"imported": count})

    @app.route("/api/import", methods=["POST"])
    def import_genome():
        upload = request.files.get("genome")
        if not upload or not upload.filename:
            return jsonify({"error": "missing genome file"}), 400
        upload_dir.mkdir(parents=True, exist_ok=True)
        suffix = Path(upload.filename).suffix or ".txt"
        with tempfile.NamedTemporaryFile(delete=False, dir=upload_dir, suffix=suffix) as temp:
            upload.save(temp.name)
            temp_path = Path(temp.name)
        personal = PersonalData(temp_path, export_path=genotypes_path)
        store.upsert_genotypes(personal.yourData)
        variants = store.upsert_genome_variants(personal.variants)
        return jsonify(
            {
                "imported": len(personal.yourData),
                "snps": len(personal.snps),
                "variants": variants,
                "assembly": personal.assembly,
                "annotation_release": personal.annotation_release,
            }
        )

    @app.route("/api/genotypes", methods=["DELETE"])
    def clear_genotypes():
        count = store.clear_genotypes()
        if genotypes_path.exists():
            genotypes_path.unlink()
        return jsonify({"deleted": count})

    @app.route("/api/scrape-runs/latest", methods=["GET"])
    def latest_scrape_run():
        return jsonify(store.latest_scrape_run() or {})

    @app.route("/api/scrape-runs/<int:run_id>", methods=["GET"])
    def get_scrape_run(run_id: int):
        run = store.get_scrape_run(run_id)
        if not run:
            return jsonify({"error": "not found"}), 404
        return jsonify(run)

    @app.route("/api/scrape", methods=["POST"])
    def start_scrape():
        payload = request.get_json(silent=True) or {}
        rsids = [normalize_rsid(rsid) for rsid in payload.get("rsids", []) if str(rsid).strip()]
        if not rsids:
            rsids = build_rsid_list()[: _int_payload(payload, "limit", 25)]
        requested = len(rsids)
        if not _bool_payload(payload, "force", False):
            rsids = store.rsids_missing_annotations(rsids)
        if not rsids:
            return jsonify({"run_id": None, "total": 0, "cached": requested}), 200
        run_id = store.create_scrape_run(len(rsids), "Web scrape", rsids)
        thread = threading.Thread(target=_run_scrape, args=(store, run_id, rsids), daemon=True)
        thread.start()
        return jsonify({"run_id": run_id, "total": len(rsids), "cached": requested - len(rsids)}), 202

    @app.route("/api/refresh-findings", methods=["POST"])
    def refresh_findings():
        payload = request.get_json(silent=True) or {}
        rsids = [normalize_rsid(rsid) for rsid in payload.get("rsids", []) if str(rsid).strip()]
        if not rsids:
            return jsonify({"error": "missing rsids"}), 400
        requested = len(rsids)
        if not _bool_payload(payload, "force", False):
            rsids = store.rsids_missing_finding_dates(rsids)
        if not rsids:
            return jsonify({"run_id": None, "total": 0, "cached": requested}), 200
        run_id = store.create_scrape_run(len(rsids), "Finding date refresh", rsids)
        thread = threading.Thread(target=_run_finding_refresh, args=(store, run_id, rsids), daemon=True)
        thread.start()
        return jsonify({"run_id": run_id, "total": len(rsids), "cached": requested - len(rsids)}), 202

    @app.route("/api/scrape/resume", methods=["POST"])
    def resume_scrape():
        latest = store.latest_scrape_run()
        if not latest:
            return jsonify({"error": "no scrape run to resume"}), 404
        rsids = store.scrape_items_by_status(latest["id"], ["pending", "running", "failed"])
        if not rsids:
            return jsonify({"error": "no pending or failed SNPs"}), 400
        run_id = store.create_scrape_run(len(rsids), f"Resume run {latest['id']}", rsids)
        thread = threading.Thread(target=_run_scrape, args=(store, run_id, rsids), daemon=True)
        thread.start()
        return jsonify({"run_id": run_id, "total": len(rsids)}), 202

    @app.route("/api/scrape-runs/<int:run_id>/pause", methods=["POST"])
    def pause_scrape_run(run_id: int):
        store.request_scrape_status(run_id, "pause")
        return jsonify({"run_id": run_id, "requested": "pause"})

    @app.route("/api/scrape-runs/<int:run_id>/cancel", methods=["POST"])
    def cancel_scrape_run(run_id: int):
        store.request_scrape_status(run_id, "cancel")
        return jsonify({"run_id": run_id, "requested": "cancel"})

    @app.route("/api/scrape-runs/<int:run_id>/retry-failed", methods=["POST"])
    def retry_failed_scrape_items(run_id: int):
        rsids = store.scrape_items_by_status(run_id, ["failed"])
        if not rsids:
            return jsonify({"error": "no failed SNPs"}), 400
        retry_run_id = store.create_scrape_run(len(rsids), f"Retry failed from run {run_id}", rsids)
        thread = threading.Thread(target=_run_scrape, args=(store, retry_run_id, rsids), daemon=True)
        thread.start()
        return jsonify({"run_id": retry_run_id, "total": len(rsids)}), 202

    @app.route("/api/export.csv", methods=["GET"])
    def export_csv():
        path = export_dir / "phenotype_export.csv"
        store.export_csv(path)
        return send_file(path, download_name="phenotype_export.csv", as_attachment=True)

    @app.route("/api/export-vep.tsv", methods=["GET"])
    def export_vep():
        zygosity = request.args.get("zygosity", "")
        filename = "phenotype_build37_vep_input.tsv" if not zygosity else f"phenotype_build37_{zygosity}_vep_input.tsv"
        path = export_dir / filename
        store.export_vep_input(path, zygosity=zygosity, limit=_int_arg("limit", 1000000))
        return send_file(path, download_name=filename, as_attachment=True)

    @app.route("/api/export-vep-rsids.txt", methods=["GET"])
    def export_vep_rsids():
        zygosity = request.args.get("zygosity", "")
        filename = "phenotype_build37_vep_rsids.txt" if not zygosity else f"phenotype_build37_{zygosity}_vep_rsids.txt"
        path = export_dir / filename
        store.export_vep_ids(path, zygosity=zygosity, limit=_int_arg("limit", 1000000))
        return send_file(path, download_name=filename, as_attachment=True)

    @app.route("/images/<path:path>")
    def send_image(path):
        return send_from_directory(APP_DIR / "images", path)

    def _flag(name: str) -> bool:
        return request.args.get(name, "").lower() in {"1", "true", "yes", "on"}

    def _int_arg(name: str, default: int) -> int:
        try:
            return int(request.args.get(name, default))
        except (TypeError, ValueError):
            return default

    def _int_payload(payload: dict, name: str, default: int) -> int:
        try:
            return int(payload.get(name, default))
        except (TypeError, ValueError):
            return default

    def _bool_payload(payload: dict, name: str, default: bool) -> bool:
        value = payload.get(name, default)
        if isinstance(value, bool):
            return value
        return str(value).lower() in {"1", "true", "yes", "on"}

    return app


def _run_scrape(store: PhenotypeStore, run_id: int, rsids: list[str]) -> None:
    completed = 0
    failed = 0
    try:
        genotypes = store.genotype_map()
        for rsid in rsids:
            requested = store.get_scrape_requested_status(run_id)
            if requested == "pause":
                store.update_scrape_run(run_id, "paused", completed, failed, "paused by user")
                return
            if requested == "cancel":
                store.set_scrape_items_status_by_status(run_id, ["pending", "running"], "canceled", "canceled by user")
                store.update_scrape_run(run_id, "canceled", completed, failed, "canceled by user")
                return
            try:
                store.set_scrape_item_status(run_id, rsid, "running")
                record = fetch_snp_record(rsid)
                finding = fetch_matching_genotype_finding(rsid, genotypes.get(rsid, ""), timeout=15)
                if finding and finding.variation not in record.variations:
                    record.variations.append(finding.variation)
                store.upsert_snps([record])
                store.set_scrape_item_status(run_id, rsid, "complete")
            except Exception as exc:
                failed += 1
                store.set_scrape_item_status(run_id, rsid, "failed", str(exc) or "provider failed")
            completed += 1
            store.update_scrape_run(run_id, "running", completed, failed)
        store.update_scrape_run(run_id, "complete", completed, failed)
    except Exception as exc:
        store.update_scrape_run(run_id, "failed", completed, failed, str(exc))


def _run_finding_refresh(store: PhenotypeStore, run_id: int, rsids: list[str]) -> None:
    completed = 0
    failed = 0
    try:
        for rsid in rsids:
            requested = store.get_scrape_requested_status(run_id)
            if requested == "cancel":
                store.set_scrape_items_status_by_status(run_id, ["pending", "running"], "canceled", "canceled by user")
                store.update_scrape_run(run_id, "canceled", completed, failed, "canceled by user")
                return
            try:
                store.set_scrape_item_status(run_id, rsid, "running")
                store.merge_upsert_snps([fetch_myvariant_record(rsid, timeout=15)])
                store.set_scrape_item_status(run_id, rsid, "complete")
            except Exception as exc:
                failed += 1
                store.set_scrape_item_status(run_id, rsid, "failed", str(exc) or "finding refresh failed")
            completed += 1
            store.update_scrape_run(run_id, "running", completed, failed)
        store.update_scrape_run(run_id, "complete", completed, failed)
    except Exception as exc:
        store.update_scrape_run(run_id, "failed", completed, failed, str(exc))


def _run_clinvar_import(store: PhenotypeStore, run_id: int, force: bool = False) -> None:
    try:
        path = download_variant_summary(force=force)
        count = store.replace_clinvar_variants(iter_variant_summary(path))
        store.update_scrape_run(run_id, "complete", 1, 0, f"imported {count} ClinVar rows")
    except Exception as exc:
        store.update_scrape_run(run_id, "failed", 0, 1, str(exc))


def _run_clinvar_scan(store: PhenotypeStore, run_id: int, rsids: list[str]) -> None:
    completed = 0
    failed = 0
    try:
        for chunk in _chunks(rsids, 100):
            requested = store.get_scrape_requested_status(run_id)
            if requested == "pause":
                store.update_scrape_run(run_id, "paused", completed, failed, "paused by user")
                return
            if requested == "cancel":
                store.set_scrape_items_status_by_status(run_id, ["pending", "running"], "canceled", "canceled by user")
                store.update_scrape_run(run_id, "canceled", completed, failed, "canceled by user")
                return
            for rsid in chunk:
                store.set_scrape_item_status(run_id, rsid, "running")
            try:
                store.merge_upsert_snps(store.clinvar_records_for_rsids(chunk))
                for rsid in chunk:
                    store.set_scrape_item_status(run_id, rsid, "complete")
                completed += len(chunk)
            except Exception as exc:
                failed += len(chunk)
                for rsid in chunk:
                    store.set_scrape_item_status(run_id, rsid, "failed", str(exc) or "ClinVar scan failed")
            store.update_scrape_run(run_id, "running", completed, failed)
        store.update_scrape_run(run_id, "complete", completed, failed)
    except Exception as exc:
        store.update_scrape_run(run_id, "failed", completed, failed, str(exc))


def _run_snpedia_bad_catalog_import(store: PhenotypeStore, run_id: int, limit: int = 0) -> None:
    scanned = 0
    matched = 0
    batch: list[SNPRecord] = []
    try:
        genotypes = store.genotype_map()
        for finding in iter_bad_genotype_findings():
            requested = store.get_scrape_requested_status(run_id)
            if requested == "pause":
                store.update_scrape_run(run_id, "paused", matched, 0, f"scanned {scanned}; matched {matched}")
                return
            if requested == "cancel":
                store.update_scrape_run(run_id, "canceled", matched, 0, "canceled by user")
                return
            scanned += 1
            if limit and scanned > limit:
                break
            genotype = genotypes.get(finding.rsid)
            if genotype and matches_imported_genotype(finding, genotype):
                matched += 1
                batch.append(
                    SNPRecord(
                        rsid=finding.rsid,
                        variations=[finding.variation],
                        source_urls={"snpedia": snpedia_url(finding.rsid)},
                    )
                )
            if len(batch) >= 100:
                store.merge_upsert_snps(batch)
                batch = []
            if scanned % 500 == 0:
                store.update_scrape_run(run_id, "running", matched, 0, f"scanned {scanned}; matched {matched}")
        if batch:
            store.merge_upsert_snps(batch)
        store.update_scrape_run(run_id, "complete", matched, 0, f"scanned {scanned}; matched {matched}")
    except Exception as exc:
        if batch:
            store.merge_upsert_snps(batch)
        store.update_scrape_run(run_id, "failed", matched, 1, str(exc))


def _run_snpedia_genoset_import(store: PhenotypeStore, run_id: int) -> None:
    try:
        findings = fetch_matching_known_genosets(store.genotype_map())
        if findings:
            store.upsert_genotypes({finding.rsid: "(match)" for finding in findings})
            store.merge_upsert_snps(
                SNPRecord(
                    rsid=finding.rsid,
                    description=finding.summary,
                    variations=[finding.variation],
                    source_urls={"snpedia": f"https://www.snpedia.com/index.php/{finding.rsid.capitalize()}"},
                )
                for finding in findings
            )
        store.update_scrape_run(run_id, "complete", len(findings), 0, f"matched {len(findings)} genosets")
    except Exception as exc:
        store.update_scrape_run(run_id, "failed", 0, 1, str(exc))


def _chunks(values: list[str], size: int):
    for index in range(0, len(values), size):
        yield values[index : index + size]
