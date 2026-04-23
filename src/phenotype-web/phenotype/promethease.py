from __future__ import annotations

import base64
import json
import re
import zlib
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from phenotype.models import SNPRecord, normalize_frequency_percent, normalize_rsid

REPORT_CHUNK_RE = re.compile(r"mygenos\.push\.apply\(mygenos,decompressString\('([^']+)'\)\);")


def iter_report_records(
    path: str | Path,
    *,
    repute: str = "Bad",
    ethnicity: str = "CEU",
) -> Iterator[SNPRecord]:
    for item in iter_report_items(path):
        if repute and str(item.get("repute", "")) != repute:
            continue
        rsid = normalize_rsid(str(item.get("rsnum") or item.get("title") or ""))
        genotype = str(item.get("geno") or ("(match)" if rsid.startswith("gs") else ""))
        if not rsid or not genotype:
            continue
        magnitude = item.get("magnitude", "")
        summary = _text(item.get("genosummary") or item.get("rstext"))
        frequency_percent = genotype_frequency_percent(item, genotype, ethnicity)
        frequency = f"{frequency_percent:g}% {ethnicity} genotype" if frequency_percent is not None else ""
        genes = item.get("genes") if isinstance(item.get("genes"), list) else []
        numrefs = item.get("numrefs")
        yield SNPRecord(
            rsid=rsid,
            description=summary,
            frequency=frequency,
            frequency_percent=frequency_percent,
            gene=", ".join(str(gene) for gene in genes if str(gene).strip()),
            citations=str(numrefs) if numrefs is not None else "",
            variations=[[genotype, str(magnitude), summary, str(item.get("repute", "") or "")]],
            classification_updated_at=str(item.get("genotime") or item.get("rstime") or "")[:10],
            source_urls={"snpedia": f"https://www.snpedia.com/index.php/{rsid.capitalize()}"},
        )


def iter_report_metadata_records(path: str | Path, *, ethnicity: str = "CEU") -> Iterator[SNPRecord]:
    for item in iter_report_items(path):
        rsid = normalize_rsid(str(item.get("rsnum") or item.get("title") or ""))
        genotype = str(item.get("geno") or ("(match)" if rsid.startswith("gs") else ""))
        if not rsid or not genotype:
            continue
        frequency_percent = genotype_frequency_percent(item, genotype, ethnicity)
        frequency = f"{frequency_percent:g}% {ethnicity} genotype" if frequency_percent is not None else ""
        genes = item.get("genes") if isinstance(item.get("genes"), list) else []
        numrefs = item.get("numrefs")
        yield SNPRecord(
            rsid=rsid,
            frequency=frequency,
            frequency_percent=frequency_percent,
            gene=", ".join(str(gene) for gene in genes if str(gene).strip()),
            citations=str(numrefs) if numrefs is not None else "",
            classification_updated_at=str(item.get("genotime") or item.get("rstime") or "")[:10],
            source_urls={"snpedia": f"https://www.snpedia.com/index.php/{rsid.capitalize()}"},
        )


def iter_report_items(path: str | Path) -> Iterator[dict[str, Any]]:
    text = Path(path).read_text(encoding="utf-8", errors="replace")
    for chunk in REPORT_CHUNK_RE.findall(text):
        try:
            data = zlib.decompress(base64.b64decode(chunk))
            items = json.loads(data.decode("utf-8"))
        except (ValueError, zlib.error, json.JSONDecodeError):
            continue
        if isinstance(items, list):
            for item in items:
                if isinstance(item, dict):
                    yield item


def genotype_frequency_percent(item: dict[str, Any], genotype: str, ethnicity: str = "CEU") -> float | None:
    all_genotypes = [str(value) for value in item.get("popfreqallgenos") or []]
    all_ethnicities = [str(value) for value in item.get("popfreqalleth") or []]
    all_numbers = item.get("popfreqallnum") or []
    if genotype in all_genotypes and ethnicity in all_ethnicities:
        genotype_index = all_genotypes.index(genotype)
        ethnicity_index = all_ethnicities.index(ethnicity)
        try:
            return normalize_frequency_percent(all_numbers[genotype_index]["data"][ethnicity_index])
        except (IndexError, TypeError, KeyError):
            pass
    popfreq = item.get("popfreq")
    if isinstance(popfreq, dict):
        return normalize_frequency_percent(popfreq.get(ethnicity))
    return None


def _text(value: Any) -> str:
    return re.sub(r"\s+", " ", str(value or "")).strip()
