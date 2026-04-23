from __future__ import annotations

import argparse
import csv
import re
from collections.abc import Iterator
from pathlib import Path
from typing import Any

from phenotype.models import normalize_rsid
from phenotype.paths import DEFAULT_DB_PATH
from phenotype.storage import PhenotypeStore


def iter_vep_tab(path: Path | str) -> Iterator[dict[str, Any]]:
    """Read Ensembl VEP tab output and yield rows keyed for local storage."""
    path = Path(path)
    with path.open(newline="", encoding="utf-8") as file:
        header = _read_header(file)
        if not header:
            return
        reader = csv.DictReader(file, fieldnames=header, delimiter="\t")
        for row in reader:
            uploaded = _value(row, "Uploaded_variation")
            if not uploaded:
                continue
            extra = parse_extra(_value(row, "Extra"))
            consequence = _value(row, "Consequence")
            existing = _value(row, "Existing_variation")
            rsid = _extract_rsid(uploaded, existing)
            if not rsid:
                continue
            yield {
                "rsid": rsid,
                "uploaded_variation": uploaded,
                "location": _value(row, "Location"),
                "allele": _value(row, "Allele"),
                "gene": _value(row, "Gene"),
                "feature": _value(row, "Feature"),
                "feature_type": _value(row, "Feature_type"),
                "consequence": consequence.replace("&", ", "),
                "impact": (_value(row, "IMPACT") or extra.get("IMPACT", "")).upper(),
                "symbol": _value(row, "SYMBOL") or extra.get("SYMBOL", ""),
                "hgvsc": _value(row, "HGVSc") or extra.get("HGVSc", ""),
                "hgvsp": _value(row, "HGVSp") or extra.get("HGVSp", ""),
                "existing_variation": existing,
                "extra": extra,
            }


def parse_extra(value: str) -> dict[str, str]:
    extra = {}
    for item in str(value or "").split(";"):
        if not item:
            continue
        if "=" in item:
            key, entry = item.split("=", 1)
        else:
            key, entry = item, "1"
        extra[key] = entry
    return extra


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Import Ensembl VEP tab output into the local Phenotype cache.")
    parser.add_argument("path", type=Path, help="VEP tab output file")
    parser.add_argument("--db", type=Path, default=DEFAULT_DB_PATH, help="Phenotype SQLite database")
    args = parser.parse_args(argv)

    store = PhenotypeStore(args.db)
    count = store.replace_vep_consequences(iter_vep_tab(args.path))
    print(f"Imported {count} VEP consequence rows into {args.db}")


def _read_header(file) -> list[str]:
    for line in file:
        line = line.rstrip("\n")
        if not line or line.startswith("##"):
            continue
        if line.startswith("#"):
            return [item.lstrip("#") for item in line.split("\t")]
        return line.split("\t")
    return []


def _value(row: dict[str, str], *names: str) -> str:
    for name in names:
        if name in row:
            return str(row.get(name, "") or "")
        alt = f"#{name}"
        if alt in row:
            return str(row.get(alt, "") or "")
    return ""


def _extract_rsid(*values: str) -> str:
    for value in values:
        match = re.search(r"\brs\d+\b", str(value or ""), re.IGNORECASE)
        if match:
            return normalize_rsid(match.group(0))
    return ""


if __name__ == "__main__":
    main()
