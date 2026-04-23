from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path

from phenotype.paths import DEFAULT_GENOTYPES_JSON


@dataclass(frozen=True)
class GenomeVariant:
    rsid: str
    chromosome: str
    position: int | None
    genotype: str
    allele_a: str
    allele_b: str
    zygosity: str
    assembly: str = "GRCh37"
    annotation_release: str = "104"


class PersonalData:
    def __init__(
        self,
        filepath: str | Path,
        export_path: str | Path = DEFAULT_GENOTYPES_JSON,
        assembly: str = "GRCh37",
        annotation_release: str = "104",
    ):
        self.filepath = Path(filepath)
        self.export_path = Path(export_path)
        self.assembly = assembly
        self.annotation_release = annotation_release
        self.personaldata: list[list[str]] = []
        self.variants: list[GenomeVariant] = []
        self.snps: list[str] = []
        self.yourData: dict[str, str] = {}
        if self.filepath.exists():
            self.readData(self.filepath)
            self.export()

    def readData(self, filepath: str | Path) -> None:
        lines = Path(filepath).read_text(encoding="utf-8", errors="replace").splitlines()
        self._detect_metadata(lines)
        is_ancestry = any("Ancestry" in line for line in lines[:5])
        relevantdata = [line for line in lines if line and not line.startswith("#")]
        self.personaldata = [line.split("\t") for line in relevantdata]
        self.personaldata = [item for item in self.personaldata if item and item[0]]
        self.snps = [item[0].lower() for item in self.personaldata]

        if is_ancestry:
            self.yourData = {
                item[0].lower(): item[-2].strip() + "/" + item[-1].strip()
                for item in self.personaldata
                if len(item) >= 2
            }
        else:
            self.yourData = {
                item[0].lower(): "(" + item[3].strip()[0] + ";" + item[3].strip()[-1] + ")"
                for item in self.personaldata
                if len(item) >= 4 and item[3].strip()
            }
            self.variants = [
                build_variant(item, self.assembly, self.annotation_release)
                for item in self.personaldata
                if len(item) >= 4 and item[3].strip()
            ]

    def _detect_metadata(self, lines: list[str]) -> None:
        header = "\n".join(lines[:40])
        if "build 37" in header or "GRCh37" in header:
            self.assembly = "GRCh37"
        release = re.search(r"Annotation Release\s+(\d+)", header, flags=re.IGNORECASE)
        if release:
            self.annotation_release = release.group(1)

    def hasGenotype(self, rsid: str) -> bool:
        genotype = self.yourData.get(rsid.lower(), "(-;-)")
        return genotype != "(-;-)"

    def export(self) -> None:
        self.export_path.parent.mkdir(parents=True, exist_ok=True)
        self.export_path.write_text(json.dumps(self.yourData), encoding="utf-8")


def build_variant(item: list[str], assembly: str, annotation_release: str) -> GenomeVariant:
    rsid = item[0].strip().lower()
    chromosome = item[1].strip() if len(item) > 1 else ""
    position = int(item[2]) if len(item) > 2 and item[2].strip().isdigit() else None
    raw_genotype = item[3].strip().upper() if len(item) > 3 else ""
    allele_a, allele_b = split_genotype(raw_genotype)
    return GenomeVariant(
        rsid=rsid,
        chromosome=chromosome,
        position=position,
        genotype=format_genotype(allele_a, allele_b),
        allele_a=allele_a,
        allele_b=allele_b,
        zygosity=zygosity(allele_a, allele_b),
        assembly=assembly,
        annotation_release=annotation_release,
    )


def split_genotype(value: str) -> tuple[str, str]:
    if not value or value == "--":
        return "-", "-"
    if len(value) == 1:
        return value, value
    return value[0], value[-1]


def format_genotype(allele_a: str, allele_b: str) -> str:
    return f"({allele_a};{allele_b})"


def zygosity(allele_a: str, allele_b: str) -> str:
    if "-" in {allele_a, allele_b}:
        return "no-call"
    if allele_a == allele_b:
        return "homozygous"
    return "heterozygous"
