from __future__ import annotations

import csv
import gzip
import re
import shutil
import urllib.request
from collections.abc import Iterable
from datetime import datetime
from pathlib import Path

from phenotype.paths import DATA_DIR

CLINVAR_VARIANT_SUMMARY_URL = "https://ftp.ncbi.nlm.nih.gov/pub/clinvar/tab_delimited/variant_summary.txt.gz"
DEFAULT_CLINVAR_VARIANT_SUMMARY_PATH = DATA_DIR / "downloads" / "clinvar_variant_summary.txt.gz"


def download_variant_summary(
    path: Path | str = DEFAULT_CLINVAR_VARIANT_SUMMARY_PATH,
    url: str = CLINVAR_VARIANT_SUMMARY_URL,
    force: bool = False,
) -> Path:
    path = Path(path)
    if path.is_file() and not force:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    temp_path = path.with_suffix(path.suffix + ".tmp")
    with urllib.request.urlopen(url, timeout=120) as response, temp_path.open("wb") as output:
        shutil.copyfileobj(response, output)
    temp_path.replace(path)
    return path


def iter_variant_summary(path: Path | str) -> Iterable[dict[str, str | int]]:
    with gzip.open(path, "rt", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file, delimiter="\t")
        for row in reader:
            for rsid in rsids_from_cell(row.get("RS# (dbSNP)", "")):
                yield {
                    "rsid": rsid,
                    "allele_id": clean(row.get("#AlleleID", "")),
                    "variation_id": clean(row.get("VariationID", "")),
                    "type": clean(row.get("Type", "")),
                    "name": clean(row.get("Name", "")),
                    "gene": clean(row.get("GeneSymbol", "")),
                    "clinical_significance": clean(row.get("ClinicalSignificance", "")),
                    "clinsig_simple": int_or_zero(row.get("ClinSigSimple", "")),
                    "last_evaluated": normalize_clinvar_date(row.get("LastEvaluated", "")),
                    "rcv_accession": first_pipe_value(row.get("RCVaccession", "")),
                    "phenotype_list": clean(row.get("PhenotypeList", "")),
                    "review_status": clean(row.get("ReviewStatus", "")),
                    "assembly": clean(row.get("Assembly", "")),
                    "reference_allele": clean(row.get("ReferenceAllele", "")),
                    "alternate_allele": clean(row.get("AlternateAllele", "")),
                }


def rsids_from_cell(value: str) -> list[str]:
    if not value or value == "-":
        return []
    return [f"rs{match}" for match in re.findall(r"\d+", value)]


def normalize_clinvar_date(value: str | None) -> str:
    value = clean(value)
    if not value:
        return ""
    for fmt in ("%b %d, %Y", "%b %d %Y", "%Y-%m-%d"):
        try:
            return datetime.strptime(value, fmt).date().isoformat()
        except ValueError:
            pass
    return ""


def first_pipe_value(value: str | None) -> str:
    return clean(value).split("|", 1)[0]


def clean(value: str | None) -> str:
    value = str(value or "").strip()
    return "" if value == "-" else value


def int_or_zero(value: str | None) -> int:
    try:
        return int(str(value or "0"))
    except ValueError:
        return 0
