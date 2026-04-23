from __future__ import annotations

import hashlib
import json
import re
import sqlite3
from datetime import datetime, timezone
from typing import Any

from phenotype.models import SNPRecord, normalize_clinical_significance, normalize_rsid
from phenotype.snpedia_catalog import enrich_snpedia_summary


def _enrich_cached_snpedia_summary(payload: dict[str, Any]) -> dict[str, Any]:
    finding = payload.get("SNPediaMatchedFinding") or {}
    summary = str(payload.get("FindingSummary") or "")
    if finding and summary and _is_generic_summary(summary):
        enriched = enrich_snpedia_summary(str(payload.get("Name") or ""), summary)
        if enriched and enriched != summary:
            payload["FindingSummary"] = enriched
            finding["summary"] = enriched
            payload["SNPediaMatchedFinding"] = finding
    return payload


def _finding_freshness(classification_updated_at: str, source_updated_at: str, imported_at: str) -> str:
    if not classification_updated_at:
        return "Unclassified"
    if imported_at and classification_updated_at > imported_at:
        return "New since import"
    if source_updated_at and classification_updated_at > source_updated_at:
        return "Updated after source import"
    return "Known at import"


def _severity_search_clause(alias: str, severity: str) -> str:
    text = f"lower(coalesce({alias}.clinical_significance_json, '')) || ' ' || lower(coalesce({alias}.variations_json, ''))"
    if severity == "pathogenic":
        return (
            f"({text} like '%pathogenic%' or {text} like '%likely pathogenic%' or {text} like '%loss of function%' "
            f"or {text} like '%loss-of-function%' or {text} like '%frameshift%' or {text} like '%nonsense%' "
            f"or {text} like '%splice%' or {text} like '%deleterious%' or {text} like '%mutation%' "
            f"or {text} like '%disease%' or {text} like '%disorder%' or {text} like '%syndrome%')"
        )
    if severity == "risk":
        return (
            f"({text} like '%risk%' or {text} like '%susceptib%' or {text} like '%predispos%' "
            f"or {text} like '%association%' or {text} like '%linked%' or {text} like '%increased%' "
            f"or {text} like '%higher%' or {text} like '%elevated%' or {text} like '%affects%')"
        )
    if severity == "drug":
        return f"({text} like '%drug%' or {text} like '%pharmacogen%' or {text} like '%response%' or {text} like '%therapy%')"
    if severity == "modifier":
        return f"({text} like '%modifier%' or {text} like '%impact%')"
    if severity == "uncertain":
        return f"({text} like '%uncertain%' or {text} like '%conflicting%')"
    if severity == "benign":
        return (
            f"({text} like '%benign%' or {text} like '%protective%' or {text} like '%resistance%' "
            f"or {text} like '%resistant to%' or {text} like '%lower risk%' or {text} like '%reduced risk%' "
            f"or {text} like '%decreased risk%' or {text} like '%beneficial%')"
        )
    return ""


def _severity_count_clause(alias: str, severity: str) -> str:
    return _severity_search_clause(alias, severity) or "0"


def _is_generic_summary(summary: str) -> bool:
    return bool(re.fullmatch(r"(?i)(?:[0-9]*\.?[0-9]+x\s*)?risk|normal|common|benign", summary.strip())) or " risk" in summary.lower()


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def _merge_record_update(update: SNPRecord, existing: SNPRecord | None) -> SNPRecord:
    if not existing:
        return update
    return SNPRecord(
        rsid=update.rsid or existing.rsid,
        description=update.description or existing.description,
        clinvar=update.clinvar or existing.clinvar,
        frequency=update.frequency or existing.frequency,
        studies=update.studies or existing.studies,
        citations=update.citations or existing.citations,
        gene=update.gene or existing.gene,
        risk=update.risk or existing.risk,
        risk_allele=update.risk_allele or existing.risk_allele,
        frequency_percent=update.frequency_percent if update.frequency_percent is not None else existing.frequency_percent,
        variations=_merge_lists(update.variations, existing.variations),
        clinical_significance=update.clinical_significance or existing.clinical_significance,
        source_urls={**existing.source_urls, **update.source_urls},
        classification_updated_at=_max_date(update.classification_updated_at, existing.classification_updated_at),
    )


def _merge_lists(primary: list[Any], fallback: list[Any]) -> list[Any]:
    merged = []
    seen = set()
    for item in [*primary, *fallback]:
        marker = repr(item)
        if marker not in seen:
            seen.add(marker)
            merged.append(item)
    return merged


def _classification_hash(clinvar: list[Any], clinical_significance: list[str]) -> str:
    payload = json.dumps(
        {"clinvar": clinvar, "clinical_significance": clinical_significance},
        sort_keys=True,
        separators=(",", ":"),
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _classification_source_date(clinvar: list[Any]) -> str:
    dates = []
    for value in _walk_values(clinvar):
        if isinstance(value, str) and len(value) >= 10 and value[4:5] == "-" and value[7:8] == "-":
            dates.append(value[:10])
    return max(dates) if dates else ""


def _max_date(*values: str) -> str:
    dates = [value[:10] for value in values if value]
    return max(dates) if dates else ""


def _walk_values(value: Any):
    if isinstance(value, dict):
        for item in value.values():
            yield from _walk_values(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_values(item)
    else:
        yield value


CLINVAR_INSERT_SQL = """
    insert or ignore into clinvar_variants (
        rsid, allele_id, variation_id, type, name, gene, clinical_significance,
        clinsig_simple, last_evaluated, rcv_accession, phenotype_list, review_status,
        assembly, reference_allele, alternate_allele, source_updated_at
    ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


VEP_INSERT_SQL = """
    insert or ignore into vep_consequences (
        rsid, uploaded_variation, location, allele, gene, feature, feature_type,
        consequence, impact, symbol, hgvsc, hgvsp, existing_variation, extra_json, imported_at
    ) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
"""


def _clinvar_insert_tuple(row: dict[str, str | int], source_updated_at: str) -> tuple[Any, ...]:
    return (
        normalize_rsid(str(row.get("rsid", ""))),
        str(row.get("allele_id", "") or ""),
        str(row.get("variation_id", "") or ""),
        str(row.get("type", "") or ""),
        str(row.get("name", "") or ""),
        str(row.get("gene", "") or ""),
        str(row.get("clinical_significance", "") or ""),
        int(row.get("clinsig_simple", 0) or 0),
        str(row.get("last_evaluated", "") or ""),
        str(row.get("rcv_accession", "") or ""),
        str(row.get("phenotype_list", "") or ""),
        str(row.get("review_status", "") or ""),
        str(row.get("assembly", "") or ""),
        str(row.get("reference_allele", "") or ""),
        str(row.get("alternate_allele", "") or ""),
        source_updated_at,
    )


def _vep_insert_tuple(row: dict[str, Any], imported_at: str) -> tuple[Any, ...]:
    return (
        normalize_rsid(str(row.get("rsid", "") or "")),
        str(row.get("uploaded_variation", "") or ""),
        str(row.get("location", "") or ""),
        str(row.get("allele", "") or ""),
        str(row.get("gene", "") or ""),
        str(row.get("feature", "") or ""),
        str(row.get("feature_type", "") or ""),
        str(row.get("consequence", "") or ""),
        str(row.get("impact", "") or ""),
        str(row.get("symbol", "") or ""),
        str(row.get("hgvsc", "") or ""),
        str(row.get("hgvsp", "") or ""),
        str(row.get("existing_variation", "") or ""),
        json.dumps(row.get("extra", {}) or {}, sort_keys=True),
        imported_at,
    )


def _vep_best_impact(impacts: str | None, rank: int | None) -> str:
    if not impacts:
        return ""
    wanted = {
        4: "HIGH",
        3: "MODERATE",
        2: "LOW",
        1: "MODIFIER",
    }.get(int(rank or 0), "")
    if wanted and wanted in {part.strip().upper() for part in impacts.split(",")}:
        return wanted
    return impacts.split(",", 1)[0].strip()


def _load_paged_rows(
    conn: sqlite3.Connection,
    sql: str,
    params: list[Any],
    limit: int,
    offset: int,
    row_mapper,
    count_sql: str | None = None,
    post_filters: list[Any] | None = None,
    resort_score: bool = False,
    sort_reverse: bool = False,
) -> tuple[list[dict[str, Any]], int]:
    filters = [predicate for predicate in (post_filters or []) if predicate]
    if filters or resort_score:
        rows = []
        total = 0
        batch_offset = 0
        batch_limit = max(limit * 2, 50)
        while True:
            raw_batch = [row_mapper(row) for row in conn.execute(sql, [*params, batch_limit, batch_offset])]
            batch = raw_batch
            for predicate in filters:
                batch = predicate(batch)
            total += len(batch)
            rows.extend(batch)
            if len(raw_batch) < batch_limit:
                break
            batch_offset += batch_limit
        if resort_score:
            rows.sort(
                key=lambda row: (int(row.get("SignificanceScore", 0) or 0), row.get("Name", "")),
                reverse=sort_reverse,
            )
        return rows[offset : offset + limit], total
    if not count_sql:
        raise ValueError("count_sql required when no post filters are applied")
    total = int(conn.execute(count_sql, params).fetchone()[0])
    rows = [row_mapper(row) for row in conn.execute(sql, [*params, limit, offset])]
    return rows, total


def _clinvar_rows_to_records(rows: list[sqlite3.Row]) -> list[SNPRecord]:
    grouped: dict[str, list[sqlite3.Row]] = {}
    for row in rows:
        grouped.setdefault(row["rsid"], []).append(row)
    return [_clinvar_group_to_record(rsid, group) for rsid, group in grouped.items()]


def _clinvar_group_to_record(rsid: str, rows: list[sqlite3.Row]) -> SNPRecord:
    clinvar = [
        [row["rcv_accession"], row["clinical_significance"], row["phenotype_list"], row["last_evaluated"]]
        for row in rows
    ]
    top = rows[0]
    dates = [row["last_evaluated"] for row in rows if row["last_evaluated"]]
    variation_id = top["variation_id"]
    source_urls = {
        "dbsnp": f"https://www.ncbi.nlm.nih.gov/snp/{rsid}",
        "clinvar": f"https://www.ncbi.nlm.nih.gov/clinvar/variation/{variation_id}/" if variation_id else "",
    }
    return SNPRecord(
        rsid=rsid,
        description=top["phenotype_list"] or top["name"],
        clinvar=clinvar,
        gene=top["gene"],
        risk=top["alternate_allele"],
        risk_allele=_single_base(top["alternate_allele"]),
        clinical_significance=normalize_clinical_significance(clinvar),
        source_urls={key: value for key, value in source_urls.items() if value},
        classification_updated_at=max(dates) if dates else "",
    )


def _single_base(value: str) -> str:
    value = str(value or "").upper()
    return value if value in {"A", "C", "G", "T"} else ""


def _unannotated_row(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "Name": row["rsid"],
        "Description": "No cached annotation yet",
        "ClinVar": "",
        "Genotype": row["genotype"],
        "Frequency": "",
        "FrequencyDisplay": "",
        "Citations": "",
        "Gene": "",
        "Risk": "",
        "RiskAllele": "",
        "FrequencyPercent": None,
        "Significance": "Not scanned",
        "SignificanceScore": 0,
        "ClinicalScore": 0,
        "FrequencyContext": "",
        "FindingSummary": "No cached annotation yet",
        "FindingSeverity": "None",
        "FindingSeverityScore": 0,
        "FindingSeverityClass": "none",
        "ClinVarFindings": [],
        "SNPediaMatchedFinding": {},
        "IsRiskMatch": False,
        "HasClinicalAlleleMatch": False,
        "HasPrometheaseMatch": False,
        "HasSNPediaMatch": False,
        "SNPediaGenotypeMatch": "",
        "AlleleOrientationNote": "No cached annotation for this imported genotype yet.",
        "Studies": "",
        "Variations": "",
        "ClinicalSignificance": "",
        "SourceUrls": {},
        "FirstSeenAt": "",
        "ClassificationUpdatedAt": "",
        "RecentFindingAt": "",
        "SourceUpdatedAt": row["imported_at"],
        "Chromosome": _row_value(row, "chromosome", ""),
        "Position": _row_value(row, "position", ""),
        "VariantZygosity": _row_value(row, "zygosity", ""),
        "VariantAssembly": _row_value(row, "assembly", ""),
        "AnnotationRelease": _row_value(row, "annotation_release", ""),
    }


def _unannotated_variant_row(row: sqlite3.Row) -> dict[str, Any]:
    payload = _unannotated_row(row)
    payload["Description"] = "No cached annotation yet"
    payload["FindingSummary"] = f"{row['zygosity'].replace('-', ' ')} genotype, not annotated"
    payload["Significance"] = "Not annotated"
    return payload


def _variant_metadata(row: sqlite3.Row) -> dict[str, Any]:
    return {
        "Chromosome": _row_value(row, "chromosome", ""),
        "Position": _row_value(row, "position", ""),
        "VariantZygosity": _row_value(row, "zygosity", ""),
        "VariantAssembly": _row_value(row, "assembly", ""),
        "AnnotationRelease": _row_value(row, "annotation_release", ""),
    }


def _row_value(row: sqlite3.Row, key: str, default: Any = "") -> Any:
    return row[key] if key in row.keys() and row[key] is not None else default


def _chunks(values: list[str], size: int):
    for index in range(0, len(values), size):
        yield values[index : index + size]
