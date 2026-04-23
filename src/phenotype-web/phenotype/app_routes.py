from __future__ import annotations

import tempfile
import threading
import time
from collections.abc import Callable
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file, send_from_directory

from phenotype.app_jobs import (
    _SNPS_CACHE_TTL,
    _SNPS_RESPONSE_CACHE,
    _refresh_and_clear_snps_cache,
    _severity_filters,
    _snps_cache_key,
    _summary_counts_cache_key,
    import_clinvar_reference,
    import_report_results,
    import_vep_results,
    run_clinvar_scan,
    run_finding_refresh,
    run_scrape,
    run_snpedia_bad_catalog_import,
    run_snpedia_genoset_import,
)
from phenotype.genome_importer import PersonalData
from phenotype.models import normalize_rsid
from phenotype.paths import APP_DIR
from phenotype.promethease import iter_report_metadata_records, iter_report_records
from phenotype.scraper import build_rsid_list
from phenotype.storage import PhenotypeStore


def register_routes(app: Flask, store: PhenotypeStore, genotypes_path: Path, upload_dir: Path, export_dir: Path, fetch_snp_record: Callable[[str], object]) -> None:
    @app.route("/", methods=["GET", "POST"])
    def main():
        return render_template("snp_resource.html")

    @app.route("/api/rsids", methods=["GET"])
    @app.route("/api/snps", methods=["GET"])
    def get_snps():
        cache_key = _snps_cache_key(store.db_path, request.args)
        cached = _SNPS_RESPONSE_CACHE.get(cache_key)
        now = time.monotonic()
        if cached and now - cached[0] < _SNPS_CACHE_TTL:
            return jsonify(cached[1])
        if _flag("counts_only"):
            cache_key = _summary_counts_cache_key(request.args)
            if cache_key:
                cached_counts = store.cached_summary_counts(cache_key)
                if cached_counts is not None:
                    return jsonify({"counts": cached_counts})
            severity_filters = _severity_filters(request.args.get("severity_filters", ""))
            payload = {
                "counts": store.snp_summary_counts(
                    search=request.args.get("search", ""),
                    has_genotype=_flag("has_genotype"),
                    mutated_only=_flag("mutated_only"),
                    clinical_match_only=_flag("clinical_match_only"),
                    promethease_only=_flag("promethease_only"),
                    new_since_import_only=_flag("new_since_import_only"),
                    severity_filters=severity_filters,
                    summary_only=True,
                )
            }
            _SNPS_RESPONSE_CACHE[cache_key] = (now, payload)
            return jsonify(payload)
        rows, total = store.list_snps(
            search=request.args.get("search", ""),
            has_genotype=_flag("has_genotype"),
            mutated_only=_flag("mutated_only"),
            clinical_match_only=_flag("clinical_match_only"),
            promethease_only=_flag("promethease_only"),
            new_since_import_only=_flag("new_since_import_only"),
            severity_filters=_severity_filters(request.args.get("severity_filters", "")),
            summary_only=True,
            sort_field=request.args.get("sort_field", ""),
            sort_dir=request.args.get("sort_dir", ""),
            limit=_int_arg("limit", 1000),
            offset=_int_arg("offset", 0),
            with_total=True,
        )
        payload = {"results": rows, "count": total}
        _SNPS_RESPONSE_CACHE[cache_key] = (now, payload)
        return jsonify(payload)

    @app.route("/api/variants", methods=["GET"])
    def get_variants():
        rows, total = store.list_genome_variants(
            search=request.args.get("search", ""),
            zygosity=request.args.get("zygosity", ""),
            clinical_only=_flag("clinical_only"),
            annotated_only=_flag("annotated_only"),
            mutated_only=_flag("mutated_only"),
            clinical_match_only=_flag("clinical_match_only"),
            promethease_only=_flag("promethease_only"),
            new_since_import_only=_flag("new_since_import_only"),
            vep_impact=request.args.get("vep_impact", ""),
            vep_consequence=request.args.get("vep_consequence", ""),
            sort_field=request.args.get("sort_field", ""),
            sort_dir=request.args.get("sort_dir", ""),
            limit=_int_arg("limit", 1000),
            offset=_int_arg("offset", 0),
            with_total=True,
        )
        return jsonify({"results": rows, "count": total})

    @app.route("/api/snps/<rsid>", methods=["GET"])
    def get_snp(rsid: str):
        row = store.get_snp(rsid, enrich_snpedia=True)
        if not row:
            return jsonify({"error": "not found"}), 404
        return jsonify(row)

    @app.route("/api/stats", methods=["GET"])
    def get_stats():
        return jsonify(store.annotation_stats())

    @app.route("/api/backlog", methods=["GET"])
    def get_backlog():
        rows = store.list_unannotated_genotypes(search=request.args.get("search", ""), limit=_int_arg("limit", 1000), offset=_int_arg("offset", 0))
        return jsonify({"results": rows, "count": len(rows)})

    @app.route("/api/clinvar/import", methods=["POST"])
    def import_clinvar_reference_route():
        payload = request.get_json(silent=True) or {}
        run_id = store.create_scrape_run(1, "ClinVar local import")
        threading.Thread(target=import_clinvar_reference, args=(store, run_id, _bool_payload(payload, "force", False)), daemon=True).start()
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
        threading.Thread(target=run_clinvar_scan, args=(store, run_id, rsids), daemon=True).start()
        return jsonify({"run_id": run_id, "total": len(rsids)}), 202

    @app.route("/api/snpedia/bad-genotypes/import", methods=["POST"])
    def import_snpedia_bad_genotypes():
        payload = request.get_json(silent=True) or {}
        run_id = store.create_scrape_run(0, "SNPedia bad genotype catalogue")
        threading.Thread(target=run_snpedia_bad_catalog_import, args=(store, run_id, _int_payload(payload, "limit", 0)), daemon=True).start()
        return jsonify({"run_id": run_id}), 202

    @app.route("/api/snpedia/genosets/import", methods=["POST"])
    def import_snpedia_genosets():
        run_id = store.create_scrape_run(0, "SNPedia genoset scan")
        threading.Thread(target=run_snpedia_genoset_import, args=(store, run_id), daemon=True).start()
        return jsonify({"run_id": run_id}), 202

    @app.route("/api/vep/import", methods=["POST"])
    def import_vep_results_route():
        upload = request.files.get("vep")
        if not upload or not upload.filename:
            return jsonify({"error": "missing VEP output file"}), 400
        upload_dir.mkdir(parents=True, exist_ok=True)
        suffix = Path(upload.filename).suffix or ".txt"
        with tempfile.NamedTemporaryFile(delete=False, dir=upload_dir, suffix=suffix) as temp:
            upload.save(temp.name)
            temp_path = Path(temp.name)
        count = import_vep_results(store, temp_path)
        return jsonify({"imported": count})

    @app.route("/api/report/import", methods=["POST"])
    def import_report_html():
        upload = request.files.get("report")
        if not upload or not upload.filename:
            return jsonify({"error": "missing report file"}), 400
        upload_dir.mkdir(parents=True, exist_ok=True)
        suffix = Path(upload.filename).suffix or ".html"
        with tempfile.NamedTemporaryFile(delete=False, dir=upload_dir, suffix=suffix) as temp:
            upload.save(temp.name)
            temp_path = Path(temp.name)
        metadata_records = list(iter_report_metadata_records(temp_path))
        finding_records = list(iter_report_records(temp_path))
        import_report_results(store, finding_records, metadata_records)
        _refresh_and_clear_snps_cache(store)
        return jsonify({"imported": len(finding_records), "metadata": len(metadata_records)})

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
        _refresh_and_clear_snps_cache(store)
        return jsonify({"imported": len(personal.yourData), "snps": len(personal.snps), "variants": variants, "assembly": personal.assembly, "annotation_release": personal.annotation_release})

    @app.route("/api/genotypes", methods=["DELETE"])
    def clear_genotypes():
        count = store.clear_genotypes()
        if genotypes_path.exists():
            genotypes_path.unlink()
        _refresh_and_clear_snps_cache(store)
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
        threading.Thread(target=run_scrape, args=(store, run_id, rsids, fetch_snp_record), daemon=True).start()
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
        threading.Thread(target=run_finding_refresh, args=(store, run_id, rsids), daemon=True).start()
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
        threading.Thread(target=run_scrape, args=(store, run_id, rsids, fetch_snp_record), daemon=True).start()
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
        threading.Thread(target=run_scrape, args=(store, retry_run_id, rsids, fetch_snp_record), daemon=True).start()
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
