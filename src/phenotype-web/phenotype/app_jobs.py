from __future__ import annotations

import threading
import time
from pathlib import Path

from phenotype.clinvar_local import download_variant_summary, iter_variant_summary
from phenotype.models import SNPRecord
from phenotype.providers.combined import fetch_snp_record
from phenotype.providers.myvariant import fetch_myvariant_record
from phenotype.providers.snpedia_ncbi import snpedia_url
from phenotype.snpedia_catalog import (
    fetch_matching_genotype_finding,
    fetch_matching_known_genosets,
    iter_bad_genotype_findings,
    matches_imported_genotype,
)
from phenotype.storage import PhenotypeStore
from phenotype.storage_helpers import _chunks
from phenotype.vep import iter_vep_tab

_SNPS_RESPONSE_CACHE: dict[str, tuple[float, dict]] = {}
_SNPS_CACHE_TTL = 120.0


def start_background_refresh(store: PhenotypeStore) -> None:
    threading.Thread(target=_refresh_summary_counts_cache, args=(store,), daemon=True).start()
    threading.Thread(target=_prime_default_snps_cache, args=(store,), daemon=True).start()


def import_clinvar_reference(store: PhenotypeStore, run_id: int, force: bool = False) -> None:
    try:
        path = download_variant_summary(force=force)
        count = store.replace_clinvar_variants(iter_variant_summary(path))
        store.update_scrape_run(run_id, "complete", 1, 0, f"imported {count} ClinVar rows")
    except Exception as exc:
        store.update_scrape_run(run_id, "failed", 0, 1, str(exc))
    finally:
        _refresh_and_clear_snps_cache(store)


def import_vep_results(store: PhenotypeStore, file_path: Path) -> int:
    return store.replace_vep_consequences(iter_vep_tab(file_path))


def import_report_results(store: PhenotypeStore, finding_records: list[SNPRecord], metadata_records: list[SNPRecord]) -> None:
    store.upsert_genotypes({record.rsid: "(match)" for record in finding_records if record.rsid.startswith("gs")})
    store.merge_upsert_snps(metadata_records)
    store.merge_upsert_snps(finding_records)


def run_scrape(
    store: PhenotypeStore,
    run_id: int,
    rsids: list[str],
    snp_fetcher=fetch_snp_record,
) -> None:
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
                record = snp_fetcher(rsid)
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
    finally:
        _refresh_and_clear_snps_cache(store)


def run_finding_refresh(store: PhenotypeStore, run_id: int, rsids: list[str]) -> None:
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
    finally:
        _refresh_and_clear_snps_cache(store)


def run_clinvar_scan(store: PhenotypeStore, run_id: int, rsids: list[str]) -> None:
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
    finally:
        _refresh_and_clear_snps_cache(store)


def run_snpedia_bad_catalog_import(store: PhenotypeStore, run_id: int, limit: int = 0) -> None:
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
    finally:
        _refresh_and_clear_snps_cache(store)


def run_snpedia_genoset_import(store: PhenotypeStore, run_id: int) -> None:
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
    finally:
        _refresh_and_clear_snps_cache(store)


def _snps_cache_key(db_path: str | Path, args) -> str:
    items = sorted((key, value) for key, value in args.items())
    return f"{Path(db_path)}::" + "&".join(f"{key}={value}" for key, value in items)


def _summary_counts_cache_key(args) -> str | None:
    search = str(args.get("search", "") or "").strip()
    if search:
        return None
    severity_filters = ",".join(sorted(_severity_filters(args.get("severity_filters", ""))))
    suffix = f":{severity_filters}" if severity_filters else ""
    if str(args.get("new_since_import_only", "")).lower() in {"1", "true", "yes", "on"}:
        return f"new{suffix}"
    if str(args.get("clinical_match_only", "")).lower() in {"1", "true", "yes", "on"}:
        return f"clinical{suffix}"
    if str(args.get("has_genotype", "")).lower() in {"1", "true", "yes", "on"}:
        return f"all{suffix}"
    if str(args.get("promethease_only", "")).lower() in {"1", "true", "yes", "on"}:
        return f"findings{suffix}"
    return None


def _severity_filters(value: str) -> list[str]:
    return [part.strip().lower() for part in str(value or "").split(",") if part.strip()]


def _prime_default_snps_cache(store: PhenotypeStore) -> None:
    try:
        rows, total = store.list_snps(
            search="",
            has_genotype=False,
            mutated_only=False,
            clinical_match_only=False,
            promethease_only=True,
            summary_only=True,
            sort_field="SnpediaMagnitude",
            sort_dir="desc",
            limit=25,
            offset=0,
            with_total=True,
        )
        _SNPS_RESPONSE_CACHE[_snps_cache_key(store.db_path, {
            "search": "",
            "has_genotype": "0",
            "mutated_only": "0",
            "clinical_match_only": "0",
            "promethease_only": "1",
            "sort_field": "SnpediaMagnitude",
            "sort_dir": "desc",
            "limit": "25",
            "offset": "0",
        })] = (time.monotonic(), {"results": rows, "count": total})
        counts = store.snp_summary_counts(
            search="",
            has_genotype=False,
            mutated_only=False,
            clinical_match_only=False,
            promethease_only=True,
            summary_only=True,
        )
        _SNPS_RESPONSE_CACHE[_snps_cache_key(store.db_path, {
            "search": "",
            "has_genotype": "0",
            "mutated_only": "0",
            "clinical_match_only": "0",
            "promethease_only": "1",
            "counts_only": "1",
        })] = (time.monotonic(), {"counts": counts})
    except Exception:
        pass


def _refresh_summary_counts_cache(store: PhenotypeStore) -> None:
    try:
        store.refresh_summary_counts_cache()
    except Exception:
        pass


def _clear_snps_cache() -> None:
    _SNPS_RESPONSE_CACHE.clear()


def _refresh_and_clear_snps_cache(store: PhenotypeStore) -> None:
    _refresh_summary_counts_cache(store)
    _clear_snps_cache()
