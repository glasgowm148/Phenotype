from __future__ import annotations

from typing import Any

import requests

from phenotype.models import SNPRecord, normalize_clinical_significance, normalize_frequency_percent, normalize_rsid

MYVARIANT_URL = "https://myvariant.info/v1/variant/{rsid}"


def fetch_myvariant_record(rsid: str, timeout: int = 30) -> SNPRecord:
    rsid = normalize_rsid(rsid)
    record = SNPRecord(rsid=rsid)
    record.source_urls = {"myvariant": MYVARIANT_URL.format(rsid=rsid)}

    try:
        response = requests.get(record.source_urls["myvariant"], timeout=timeout)
        response.raise_for_status()
    except requests.RequestException:
        return record

    try:
        data = response.json()
    except ValueError:
        return record
    variant = _select_variant(data, rsid)
    if not variant:
        return record

    record.gene = _first_text(_extract_path(variant, "dbsnp", "gene", "symbol"))
    if not record.gene:
        record.gene = _first_text(_extract_path(variant, "clinvar", "gene", "symbol"))
    if not record.gene:
        record.gene = _first_text(_extract_path(variant, "snpeff", "ann", "genename"))
    record.clinvar = _clinvar_rows(variant.get("clinvar"))
    record.clinical_significance = normalize_clinical_significance(record.clinvar)
    record.description = _description(variant.get("clinvar"))
    record.frequency, record.frequency_percent = _frequency(variant.get("dbsnp", {}).get("alleles"))
    record.classification_updated_at = _classification_updated_at(variant.get("clinvar"))
    return record


def _select_variant(data: Any, rsid: str) -> dict[str, Any] | None:
    candidates = data if isinstance(data, list) else [data]
    records = [item for item in candidates if isinstance(item, dict)]
    matching = [
        item
        for item in records
        if normalize_rsid(_first_text(_extract_path(item, "dbsnp", "rsid"))) == rsid
    ]
    candidates = matching or records
    return max(candidates, key=_variant_score) if candidates else None


def _variant_score(item: dict[str, Any]) -> int:
    score = 0
    if _as_list(_extract_path(item, "clinvar", "rcv")):
        score += 10
    if _classification_updated_at(item.get("clinvar")):
        score += 5
    if _first_text(_extract_path(item, "clinvar", "gene", "symbol")):
        score += 1
    return score


def _clinvar_rows(clinvar: Any) -> list[list[str]]:
    rows = []
    for rcv in _as_list(_extract_path(clinvar, "rcv")):
        if not isinstance(rcv, dict):
            continue
        significance = _first_text(
            rcv.get("clinical_significance")
            or rcv.get("clinicalsignificance")
            or rcv.get("review_status")
            or rcv.get("clinical_significance_description")
        )
        condition = _first_text(_extract_path(rcv, "conditions", "name"))
        accession = _first_text(rcv.get("accession"))
        date = _first_text(rcv.get("last_evaluated") or rcv.get("date_last_evaluated"))
        row = [value for value in [accession, significance, condition, date[:10]] if value]
        if row:
            rows.append(row)
    return rows


def _description(clinvar: Any) -> str:
    conditions = []
    for rcv in _as_list(_extract_path(clinvar, "rcv")):
        condition = _first_text(_extract_path(rcv, "conditions", "name"))
        if condition and condition not in conditions:
            conditions.append(condition)
    return "; ".join(conditions)


def _classification_updated_at(clinvar: Any) -> str:
    dates = []
    for rcv in _as_list(_extract_path(clinvar, "rcv")):
        if isinstance(rcv, dict):
            value = _first_text(rcv.get("last_evaluated") or rcv.get("date_last_evaluated"))
            if value:
                dates.append(value[:10])
    return max(dates) if dates else ""


def _frequency(alleles: Any) -> tuple[str, float | None]:
    values = []
    for allele in _as_list(alleles):
        if not isinstance(allele, dict):
            continue
        base = _first_text(allele.get("allele"))
        raw_frequency = allele.get("frequency", allele.get("freq"))
        percent = normalize_frequency_percent(raw_frequency)
        if base and percent is not None:
            values.append((base, percent))
    if not values:
        return "", None
    base, percent = max(values, key=lambda item: item[1])
    return f"{base}={percent:g}%", percent


def _extract_path(value: Any, *path: str) -> Any:
    current = value
    for key in path:
        if isinstance(current, list):
            current = [_extract_path(item, key) for item in current]
        elif isinstance(current, dict):
            current = current.get(key)
        else:
            return None
    return current


def _as_list(value: Any) -> list[Any]:
    if value is None:
        return []
    return value if isinstance(value, list) else [value]


def _first_text(value: Any) -> str:
    if isinstance(value, list):
        for item in value:
            text = _first_text(item)
            if text:
                return text
        return ""
    if isinstance(value, dict):
        for key in ("name", "symbol", "value", "label", "description"):
            text = _first_text(value.get(key))
            if text:
                return text
        return ""
    return str(value).strip() if value is not None else ""
