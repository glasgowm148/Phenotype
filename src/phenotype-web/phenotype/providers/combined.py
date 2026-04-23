from __future__ import annotations

from typing import Any

from phenotype.models import SNPRecord, normalize_clinical_significance, normalize_rsid
from phenotype.providers.myvariant import fetch_myvariant_record
from phenotype.providers.snpedia_ncbi import fetch_snp_record as fetch_snpedia_ncbi_record


def fetch_snp_record(rsid: str, timeout: int = 30) -> SNPRecord:
    rsid = normalize_rsid(rsid)
    api_record = fetch_myvariant_record(rsid, timeout=timeout)
    html_record = fetch_snpedia_ncbi_record(rsid, timeout=timeout)
    return merge_records(api_record, html_record)


def merge_records(primary: SNPRecord, fallback: SNPRecord) -> SNPRecord:
    record = SNPRecord(rsid=primary.rsid or fallback.rsid)
    for field in ("description", "frequency", "studies", "citations", "gene", "risk", "risk_allele"):
        setattr(record, field, getattr(primary, field) or getattr(fallback, field))
    record.frequency_percent = (
        primary.frequency_percent if primary.frequency_percent is not None else fallback.frequency_percent
    )
    record.clinvar = _merge_lists(primary.clinvar, fallback.clinvar)
    record.variations = _merge_lists(primary.variations, fallback.variations)
    record.clinical_significance = normalize_clinical_significance(
        _merge_lists(primary.clinical_significance, fallback.clinical_significance)
    )
    record.source_urls = {**fallback.source_urls, **primary.source_urls}
    record.classification_updated_at = primary.classification_updated_at or fallback.classification_updated_at
    return record


def _merge_lists(primary: list[Any], fallback: list[Any]) -> list[Any]:
    merged = []
    seen = set()
    for item in [*primary, *fallback]:
        marker = repr(item)
        if marker not in seen:
            seen.add(marker)
            merged.append(item)
    return merged
