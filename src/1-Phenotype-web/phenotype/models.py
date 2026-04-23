from __future__ import annotations

import html
import re
from dataclasses import dataclass, field
from typing import Any


def normalize_rsid(value: str) -> str:
    return value.strip().lower()


@dataclass
class SNPRecord:
    rsid: str
    description: str = ""
    clinvar: list[Any] = field(default_factory=list)
    frequency: str = ""
    studies: str = ""
    citations: str = ""
    gene: str = ""
    risk: str = ""
    risk_allele: str = ""
    frequency_percent: float | None = None
    variations: list[Any] = field(default_factory=list)
    clinical_significance: list[str] = field(default_factory=list)
    source_urls: dict[str, str] = field(default_factory=dict)
    classification_updated_at: str = ""

    @classmethod
    def from_legacy(cls, rsid: str, payload: dict[str, Any]) -> SNPRecord:
        return cls(
            rsid=normalize_rsid(rsid),
            description=payload.get("Description", ""),
            clinvar=payload.get("ClinVar") or [],
            frequency=payload.get("Frequency", ""),
            studies=payload.get("Studies", ""),
            citations=payload.get("Citations", ""),
            gene=payload.get("Gene", ""),
            risk=payload.get("Risk", ""),
            risk_allele=normalize_risk_allele(payload.get("Risk", "")),
            frequency_percent=normalize_frequency_percent(payload.get("Frequency", "")),
            variations=payload.get("Variations") or [],
            clinical_significance=normalize_clinical_significance(payload.get("ClinVar") or []),
            source_urls=payload.get("SourceUrls") or {},
            classification_updated_at=payload.get("ClassificationUpdatedAt", ""),
        )

    def to_legacy(self, genotype: str = "(n/a)") -> dict[str, str]:
        snpedia_match = snpedia_genotype_match(self.variations, genotype)
        snpedia_finding = snpedia_matched_finding(self.variations, genotype, snpedia_match)
        clinical_match = clinical_allele_match(genotype, self.risk_allele, self.clinical_significance)
        snpedia_match_actionable = snpedia_actionable_match(snpedia_finding)
        significance = personal_significance(
            self.clinical_significance,
            genotype,
            self.risk_allele,
            self.frequency_percent,
            snpedia_finding,
        )
        findings = clinvar_findings(self.clinvar, self.classification_updated_at)
        if not findings and self.clinical_significance:
            findings = fallback_findings(self.clinical_significance, self.description, self.classification_updated_at)
        top_finding = findings[0] if findings else {}
        if snpedia_finding and snpedia_finding.get("severity_score", 0) > top_finding.get("severity_score", 0):
            top_finding = snpedia_finding
        return {
            "Name": self.rsid,
            "Description": self.description,
            "ClinVar": _join_clinvar(self.clinvar),
            "Genotype": genotype,
            "Frequency": self.frequency,
            "FrequencyDisplay": format_frequency_percent(self.frequency_percent, self.frequency),
            "Citations": self.citations,
            "Gene": self.gene,
            "Risk": self.risk,
            "RiskAllele": self.risk_allele,
            "FrequencyPercent": self.frequency_percent,
            "Significance": significance["label"],
            "SignificanceScore": significance["score"],
            "ClinicalScore": significance["clinical_score"],
            "FrequencyContext": significance["frequency_context"],
            "FindingSummary": top_finding.get("summary", ""),
            "FindingSeverity": top_finding.get("severity", "None"),
            "FindingSeverityScore": top_finding.get("severity_score", 0),
            "FindingSeverityClass": top_finding.get("severity_class", "none"),
            "ClinVarFindings": findings,
            "SNPediaMatchedFinding": snpedia_finding,
            "IsRiskMatch": clinical_match or snpedia_match_actionable,
            "HasFindingAlleleMatch": clinical_match or snpedia_match_actionable,
            "HasClinicalAlleleMatch": clinical_match,
            "HasPrometheaseMatch": clinical_match or snpedia_match_actionable,
            "HasSNPediaMatch": snpedia_match_actionable,
            "SNPediaGenotypeMatch": snpedia_match,
            "AlleleOrientationNote": allele_orientation_note(self.variations, genotype, snpedia_match),
            "Studies": self.studies,
            "Variations": "<br>".join(_format_variation(v, genotype) for v in self.variations),
            "ClinicalSignificance": ", ".join(self.clinical_significance),
            "SourceUrls": self.source_urls,
        }


def normalize_clinical_significance(items: list[Any]) -> list[str]:
    values = []
    for item in items:
        cells = item[1:] if isinstance(item, list) and len(item) > 1 else [item]
        for cell in cells:
            for part in str(cell).replace(";", ",").split(","):
                value = part.strip().lower()
                if value and not ignored_clinical_value(value) and value not in values:
                    values.append(value)
    return values


def ignored_clinical_value(value: str) -> bool:
    return (
        not value
        or value in {"-", "not provided", "none provided"}
        or value.startswith("rcv")
        or bool(re.fullmatch(r"\d{4}-\d{2}-\d{2}", value))
    )


def normalize_risk_allele(value: Any) -> str:
    match = re.search(r"\b([ACGT])\b", str(value).upper())
    return match.group(1) if match else ""


def normalize_frequency_percent(value: Any) -> float | None:
    if isinstance(value, list):
        value = " ".join(str(item) for item in value)
    match = re.search(r"([0-9]*\.?[0-9]+)\s*(%)?", str(value))
    if not match:
        return None
    number = float(match.group(1))
    if number <= 0:
        return None
    if match.group(2):
        return number if number <= 100 else None
    if "." in match.group(1) and 0 <= number <= 1:
        return number * 100
    return number if number <= 100 else None


def format_frequency_percent(percent: float | None, fallback: Any = "") -> str:
    if percent is None:
        return "" if is_zero_frequency_text(fallback) else str(fallback or "")
    return f"{percent:.2f}".rstrip("0").rstrip(".") + "%"


def is_zero_frequency_text(value: Any) -> bool:
    return bool(re.fullmatch(r"\s*(?:[ACGT]\s*=\s*)?0+(?:\.0+)?%?\s*", str(value or ""), re.IGNORECASE))


def genotype_has_risk_allele(genotype: str, risk_allele: str) -> bool:
    return bool(genotype and genotype != "(n/a)" and risk_allele and risk_allele.upper() in genotype.upper())


def has_finding_allele_match(
    genotype: str,
    risk_allele: str,
    clinical_significance: list[str],
    snpedia_finding: dict[str, Any] | None = None,
) -> bool:
    return clinical_allele_match(genotype, risk_allele, clinical_significance) or snpedia_actionable_match(
        snpedia_finding
    )


def clinical_allele_match(genotype: str, risk_allele: str, clinical_significance: list[str]) -> bool:
    if not genotype_has_risk_allele(genotype, risk_allele):
        return False
    _, score = clinical_significance_category(clinical_significance)
    return score >= 40


def snpedia_actionable_match(snpedia_finding: dict[str, Any] | None = None) -> bool:
    if not snpedia_finding:
        return False
    score = int(snpedia_finding.get("severity_score", 0) or 0)
    magnitude = snpedia_numeric_magnitude(snpedia_finding.get("magnitude", ""))
    return score >= 40 or (
        magnitude is not None
        and magnitude > 0
        and meaningful_snpedia_note(str(snpedia_finding.get("note", "") or ""))
    )


def snpedia_genotype_match(variations: list[Any], genotype: str) -> str:
    if str(genotype).lower() == "(match)":
        for variation in variations:
            allele = str(variation[0]) if isinstance(variation, list) and variation else str(variation).split(" ", 1)[0]
            if allele.lower() == "(match)":
                return "direct"
    genotype_key = normalize_genotype_key(genotype)
    if not genotype_key:
        return ""
    complement_key = complement_genotype_key(genotype_key)
    for variation in variations:
        allele = str(variation[0]) if isinstance(variation, list) and variation else str(variation).split(" ", 1)[0]
        variation_key = normalize_genotype_key(allele)
        if variation_key == genotype_key:
            return "direct"
        if variation_key and variation_key == complement_key:
            return "complement"
    return "none" if variations else ""


def allele_orientation_note(variations: list[Any], genotype: str, match: str) -> str:
    if not genotype or genotype == "(n/a)":
        return "No imported genotype for this SNP."
    if not variations:
        return "No SNPedia genotype table is cached for this SNP."
    if match == "direct":
        return "SNPedia has a direct genotype match."
    if match == "complement":
        return "SNPedia appears to use the complementary strand for this genotype."
    return "No direct or complementary SNPedia genotype match was found; review source links before interpreting this row."


def snpedia_matched_finding(variations: list[Any], genotype: str, match: str) -> dict[str, str | int]:
    if match not in {"direct", "complement"}:
        return {}
    genotype_key = normalize_genotype_key(genotype)
    complement_key = complement_genotype_key(genotype_key)
    for variation in variations:
        allele = str(variation[0]) if isinstance(variation, list) and variation else str(variation).split(" ", 1)[0]
        variation_key = normalize_genotype_key(allele)
        if variation_key != genotype_key and variation_key != complement_key:
            continue
        magnitude = ""
        note = ""
        if isinstance(variation, list):
            magnitude = str(variation[1]).strip() if len(variation) > 1 else ""
            note = " ".join(str(part).strip() for part in variation[2:] if str(part).strip())
            if not note:
                note = " ".join(str(part).strip() for part in variation[1:] if str(part).strip())
        else:
            text = str(variation)
            note = text.replace(allele, "", 1).strip()
        severity_text = " ".join(part for part in [magnitude, note] if part)
        severity, score, severity_class_name = snpedia_note_severity(severity_text)
        summary_label = severity.lower() if severity != "SNPedia" else "note"
        return {
            "allele": allele,
            "note": note,
            "magnitude": magnitude,
            "match": match,
            "severity": severity,
            "severity_score": score,
            "severity_class": severity_class_name,
            "summary": f"SNPedia {summary_label}: {severity_text}" if severity_text and score > 0 else "",
        }
    return {}


def snpedia_note_severity(note: str) -> tuple[str, int, str]:
    lower = note.lower()
    if not lower.strip(" ?;:-"):
        return "None", 0, "none"
    if re.search(r"\b[0-9]+(?:\.[0-9]+)?(?:-[0-9]+(?:\.[0-9]+)?)?x\b", lower) or "risk" in lower:
        return "Risk", 50, "risk"
    if "carrier" in lower:
        return "Carrier", 45, "modifier"
    if "common" in lower or "normal" in lower:
        return "Common", 0, "benign"
    magnitude = snpedia_numeric_magnitude(note)
    if magnitude is not None and magnitude > 0 and meaningful_snpedia_note(note):
        return "Magnitude", min(40, max(1, round(magnitude * 10))), "modifier"
    return "SNPedia", 10, "uncertain"


def snpedia_numeric_magnitude(value: Any) -> float | None:
    match = re.search(r"\b([0-9]+(?:\.[0-9]+)?)\b", str(value or ""))
    if not match:
        return None
    return float(match.group(1))


def meaningful_snpedia_note(note: str) -> bool:
    lower = re.sub(r"\s+", " ", note.lower()).strip(" ?;:-")
    return bool(lower) and lower not in {
        "common",
        "normal",
        "common/normal",
        "normal/common",
        "unknown",
        "not set",
        "not specified",
        "none",
    }


def normalize_genotype_key(value: str) -> str:
    if str(value).lower() == "(match)":
        return "MATCH"
    alleles = re.findall(r"[ACGTID]", str(value).upper())
    if len(alleles) < 2:
        return ""
    return "".join(sorted(alleles[:2]))


def complement_genotype_key(value: str) -> str:
    complement = str.maketrans("ACGT", "TGCA")
    return "".join(sorted(str(value).translate(complement)))


def clinical_significance_category(values: list[str]) -> tuple[str, int]:
    text = " ".join(str(value).lower().replace("_", "-") for value in values)
    rules = [
        ("likely pathogenic", "Likely pathogenic", 90),
        ("pathogenic", "Pathogenic", 100),
        ("drug-response", "Drug response", 60),
        ("drug response", "Drug response", 60),
        ("risk-factor", "Risk factor", 50),
        ("risk factor", "Risk factor", 50),
        ("likely risk allele", "Likely risk allele", 45),
        ("risk allele", "Risk allele", 40),
        ("affects", "Affects", 40),
        ("protective", "Protective", 35),
        ("association", "Association", 30),
        ("uncertain-significance", "Uncertain", 20),
        ("uncertain significance", "Uncertain", 20),
        ("conflicting", "Conflicting", 10),
        ("likely benign", "Benign", 0),
        ("benign", "Benign", 0),
    ]
    for marker, label, score in rules:
        if marker in text:
            return label, score
    return "None", 0


def personal_significance(
    values: list[str],
    genotype: str,
    risk_allele: str,
    frequency_percent: float | None = None,
    snpedia_finding: dict[str, Any] | None = None,
) -> dict[str, int | str]:
    label, score = clinical_significance_category(values)
    snpedia_score = int((snpedia_finding or {}).get("severity_score", 0) or 0)
    snpedia_label = str((snpedia_finding or {}).get("severity", "") or "SNPedia")
    snpedia_note_label = "SNPedia note" if snpedia_label == "SNPedia" else f"SNPedia {snpedia_label.lower()} note"
    if score == 0:
        if snpedia_score > 0:
            return _significance_result(
                snpedia_note_label,
                frequency_adjusted_score(snpedia_score, frequency_percent),
                snpedia_score,
                frequency_percent,
            )
        return _significance_result("None", 0, score, frequency_percent)
    if not genotype or genotype == "(n/a)":
        return _significance_result(f"{label} (no genotype)", 0, score, frequency_percent)
    if risk_allele:
        if genotype_has_risk_allele(genotype, risk_allele):
            return _significance_result(f"{label} match", frequency_adjusted_score(score, frequency_percent), score, frequency_percent)
        if snpedia_score > 0:
            return _significance_result(
                f"{label} review; {snpedia_note_label}",
                frequency_adjusted_score(max(score - 20, snpedia_score), frequency_percent),
                max(score, snpedia_score),
                frequency_percent,
            )
        return _significance_result(f"{label} not present", 0, score, frequency_percent)
    review_score = max(score - 20, 1)
    return _significance_result(
        f"{label} review",
        frequency_adjusted_score(review_score, frequency_percent),
        score,
        frequency_percent,
    )


def frequency_adjusted_score(score: int, frequency_percent: float | None) -> int:
    if frequency_percent is None:
        return score
    return min(score, frequency_priority_cap(frequency_percent))


def frequency_priority_cap(frequency_percent: float) -> int:
    if frequency_percent <= 1:
        return 100
    if frequency_percent <= 5:
        return 90
    if frequency_percent <= 10:
        return 75
    if frequency_percent <= 25:
        return 55
    if frequency_percent <= 50:
        return 35
    return 20


def frequency_context(frequency_percent: float | None) -> str:
    if frequency_percent is None:
        return "frequency unknown"
    if frequency_percent <= 1:
        return "rare"
    if frequency_percent <= 5:
        return "low frequency"
    if frequency_percent <= 10:
        return "uncommon"
    if frequency_percent <= 25:
        return "moderate frequency"
    if frequency_percent <= 50:
        return "common"
    return "very common"


def _significance_result(
    label: str,
    score: int,
    clinical_score: int,
    frequency_percent: float | None,
) -> dict[str, int | str]:
    context = frequency_context(frequency_percent)
    if score > 0 and frequency_percent is not None:
        label = f"{label}, {context}"
    return {
        "label": label,
        "score": score,
        "clinical_score": clinical_score,
        "frequency_context": context,
    }


def clinvar_findings(items: list[Any], fallback_date: str = "") -> list[dict[str, str | int]]:
    findings = []
    seen = set()
    for item in items:
        parsed = parse_clinvar_item(item, fallback_date)
        if not parsed["condition"] and not parsed["significance"]:
            continue
        marker = (parsed["date"], parsed["significance"].lower(), parsed["condition"].lower())
        if marker in seen:
            continue
        seen.add(marker)
        label, score = clinical_significance_category([parsed["significance"]])
        parsed["severity"] = label
        parsed["severity_score"] = score
        parsed["severity_class"] = severity_class(score, label)
        parsed["summary"] = finding_summary(parsed)
        findings.append(parsed)
    return sorted(findings, key=lambda finding: (finding["severity_score"], finding["date"]), reverse=True)


def fallback_findings(values: list[str], condition: str = "", date: str = "") -> list[dict[str, str | int]]:
    label, score = clinical_significance_category(values)
    if score == 0:
        return []
    finding = {
        "accession": "",
        "significance": label,
        "condition": condition or "unspecified condition",
        "date": date[:10],
        "severity": label,
        "severity_score": score,
        "severity_class": severity_class(score, label),
    }
    finding["summary"] = finding_summary(finding)
    return [finding]


def parse_clinvar_item(item: Any, fallback_date: str = "") -> dict[str, str | int]:
    if isinstance(item, dict):
        accession = str(item.get("accession", "") or "")
        significance = str(item.get("significance", item.get("clinical_significance", "")) or "")
        condition = str(item.get("condition", item.get("conditions", "")) or "")
        date = str(item.get("date", item.get("last_evaluated", fallback_date)) or "")
    elif isinstance(item, list):
        cells = [str(cell) for cell in item]
        accession = cells[0] if cells and cells[0].startswith("RCV") else ""
        offset = 1 if accession else 0
        significance = cells[offset] if len(cells) > offset else ""
        condition = cells[offset + 1] if len(cells) > offset + 1 else ""
        date = cells[offset + 2] if len(cells) > offset + 2 else fallback_date
        if (
            clinical_significance_category([significance])[1] == 0
            and clinical_significance_category([condition])[1] > 0
        ):
            significance, condition = condition, significance
            date = cells[offset + 3] if len(cells) > offset + 3 and re.match(r"\d{4}-", cells[offset + 3]) else fallback_date
    else:
        accession = ""
        significance = str(item)
        condition = ""
        date = fallback_date
    return {
        "accession": accession,
        "significance": significance,
        "condition": condition,
        "date": date[:10],
    }


def severity_class(score: int, label: str) -> str:
    lower = label.lower()
    if "pathogenic" in lower or score >= 90:
        return "pathogenic"
    if "drug" in lower:
        return "drug"
    if "risk" in lower or score >= 50:
        return "risk"
    if "benign" in lower:
        return "benign"
    if score >= 30:
        return "modifier"
    if score >= 10:
        return "uncertain"
    return "none"


def finding_summary(finding: dict[str, str | int]) -> str:
    condition = str(finding.get("condition", "") or "unspecified condition")
    significance = str(finding.get("significance", "") or "unspecified significance")
    severity = str(finding.get("severity", "") or "Finding")
    if finding.get("severity_score", 0):
        return f"{severity}: {condition}"
    return f"{significance}: {condition}"


def _join_clinvar(items: list[Any]) -> str:
    values = []
    for item in items:
        if isinstance(item, list):
            values.append("<br>".join(html.escape(str(value)) for value in item[1:]))
        else:
            values.append(html.escape(str(item)))
    return "<br>".join(values)


def _format_variation(variation: Any, genotype: str) -> str:
    if isinstance(variation, list):
        text = " ".join(str(part) for part in variation)
        allele = str(variation[0]) if variation else ""
    else:
        text = str(variation)
        allele = text.split(" ", 1)[0]

    escaped = html.escape(text)
    match = snpedia_genotype_match([[allele]], genotype)
    if match == "direct":
        return f"<b>{escaped}</b>"
    if match == "complement":
        return f"<b>{escaped} (complement strand match)</b>"
    return escaped
