from __future__ import annotations

import json
import re
import urllib.error
import urllib.parse
import urllib.request
from collections.abc import Iterator
from dataclasses import dataclass
from functools import lru_cache

from phenotype.models import complement_genotype_key, is_homozygous_genotype_key, normalize_genotype_key, normalize_rsid

SNPEDIA_ASK_API = "https://bots.snpedia.com/api.php"


@dataclass(frozen=True)
class SnpediaGenotypeFinding:
    rsid: str
    genotype: str
    magnitude: str
    repute: str
    summary: str
    url: str

    @property
    def variation(self) -> list[str]:
        return [self.genotype, self.magnitude, self.summary, self.repute]


KNOWN_GENOSET_RULES = {
    "gs223": [("rs10483639", "C"), ("rs3783641", "A"), ("rs8007267", "T")],
    "gs281": [("rs4994", "A"), ("rs1042713", "A")],
    "gs311": [("rs3177427", "A"), ("rs7972", "G"), ("rs1046428", "C")],
}


def iter_bad_genotype_findings(page_size: int = 500, timeout: int = 30) -> Iterator[SnpediaGenotypeFinding]:
    offset = 0
    while True:
        payload = _ask(
            "[[Magnitude::>0]][[Repute::Bad]]"
            "|?Magnitude|?Repute|?Summary"
            f"|limit={page_size}|offset={offset}",
            timeout=timeout,
        )
        results = payload.get("query", {}).get("results", {})
        for title, item in results.items():
            finding = _finding_from_result(title, item)
            if finding:
                yield finding
        next_offset = payload.get("query-continue-offset")
        if next_offset is None:
            return
        offset = int(next_offset)


def fetch_matching_genotype_finding(
    rsid: str,
    imported_genotype: str,
    timeout: int = 30,
) -> SnpediaGenotypeFinding | None:
    for title in _candidate_titles(rsid, imported_genotype):
        payload = _ask(f"[[{title}]]|?Magnitude|?Repute|?Summary", timeout=timeout)
        results = payload.get("query", {}).get("results", {})
        for result_title, item in results.items():
            finding = _finding_from_result(result_title, item)
            if finding and matches_imported_genotype(finding, imported_genotype):
                return finding
    return None


def fetch_matching_known_genosets(
    genotypes: dict[str, str],
    timeout: int = 30,
) -> list[SnpediaGenotypeFinding]:
    matches = []
    for gs_id, criteria in KNOWN_GENOSET_RULES.items():
        if all(_allele_matches(genotypes.get(rsid, ""), allele) for rsid, allele in criteria):
            finding = fetch_genoset_finding(gs_id, timeout=timeout)
            if finding:
                matches.append(finding)
    return matches


def fetch_genoset_finding(gs_id: str, timeout: int = 30) -> SnpediaGenotypeFinding | None:
    title = normalize_rsid(gs_id).capitalize()
    payload = _ask(f"[[{title}]]|?Magnitude|?Repute|?Summary", timeout=timeout)
    results = payload.get("query", {}).get("results", {})
    item = results.get(title) or next(iter(results.values()), None)
    if not item:
        return None
    printouts = item.get("printouts", {})
    magnitude = _first(printouts.get("Magnitude"))
    summary = _enrich_summary(title, _first(printouts.get("Summary")))
    repute = _first(printouts.get("Repute"))
    if not magnitude and not summary:
        return None
    return SnpediaGenotypeFinding(
        rsid=normalize_rsid(gs_id),
        genotype="(match)",
        magnitude=str(magnitude),
        repute=str(repute),
        summary=str(summary),
        url=str(item.get("fullurl", "")),
    )


def matches_imported_genotype(finding: SnpediaGenotypeFinding, imported_genotype: str) -> bool:
    imported_key = normalize_genotype_key(imported_genotype)
    finding_key = normalize_genotype_key(finding.genotype)
    complement_allowed = not is_homozygous_genotype_key(imported_key)
    return bool(
        imported_key
        and finding_key
        and (
            imported_key == finding_key
            or (complement_allowed and complement_genotype_key(imported_key) == finding_key)
        )
    )


def _candidate_titles(rsid: str, imported_genotype: str) -> list[str]:
    normalized = normalize_rsid(rsid)
    prefix = normalized[0].upper() + normalized[1:]
    keys = [normalize_genotype_key(imported_genotype)]
    complement = complement_genotype_key(keys[0]) if keys[0] else ""
    if complement and complement not in keys:
        keys.append(complement)
    return [f"{prefix}({key[0]};{key[1]})" for key in keys if len(key) >= 2]


def _allele_matches(genotype: str, allele: str) -> bool:
    if not genotype:
        return False
    allele = allele.upper()
    genotype_text = str(genotype).upper()
    if allele in re.findall(r"[ACGTID]", genotype_text):
        return True
    complement = str.maketrans("ACGT", "TGCA")
    return allele.translate(complement) in re.findall(r"[ACGTID]", genotype_text)


def _ask(query: str, timeout: int) -> dict:
    url = SNPEDIA_ASK_API + "?" + urllib.parse.urlencode({"action": "ask", "query": query, "format": "json"})
    request = urllib.request.Request(url, headers={"User-Agent": "Phenotype-local/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return {}


def _parse_wikitext(page: str, timeout: int = 20) -> str:
    url = SNPEDIA_ASK_API + "?" + urllib.parse.urlencode(
        {"action": "parse", "page": page, "prop": "wikitext", "format": "json"}
    )
    request = urllib.request.Request(url, headers={"User-Agent": "Phenotype-local/1.0"})
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
            return str(payload.get("parse", {}).get("wikitext", {}).get("*", "") or "")
    except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return ""


@lru_cache(maxsize=4096)
def _enrich_summary(page: str, summary: str) -> str:
    summary = str(summary or "").strip()
    if summary and not _is_generic_snpedia_summary(summary):
        return summary
    condition = _extract_snpedia_condition(_parse_wikitext(page))
    if not condition:
        return summary
    if summary:
        return f"{summary} of {condition}"
    return condition


def _is_generic_snpedia_summary(summary: str) -> bool:
    text = summary.strip()
    if bool(re.fullmatch(r"(?i)(?:[0-9]*\.?[0-9]+x\s*)?risk|normal|common|benign", text)):
        return True
    body = re.sub(r"(?i)^snpedia\s+\w+\s*:\s*", "", text).strip()
    if body.lower() in {"normal", "common", "benign"}:
        return True
    return bool(re.fullmatch(r"(?i)(?:[0-9]*\.?[0-9]+\s+)?(?:[0-9]*\.?[0-9]+x\s+)?risk", body))


def _extract_snpedia_condition(wikitext: str) -> str:
    text = re.sub(r"\{\{[^{}]*\}\}", " ", wikitext, flags=re.S)
    patterns = [
        r"associated with \[\[([^\]|#]+)",
        r"risk of \[\[([^\]|#]+)",
        r"linked to \[\[([^\]|#]+)",
        r"for \[\[([^\]|#]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, text, re.I)
        if match:
            return match.group(1).replace("_", " ").strip()
    return ""


def enrich_snpedia_summary(page: str, summary: str) -> str:
    return _enrich_summary(page, summary)


def _finding_from_result(title: str, item: dict) -> SnpediaGenotypeFinding | None:
    parsed = _parse_title(title)
    if not parsed:
        return None
    rsid, genotype = parsed
    printouts = item.get("printouts", {})
    magnitude = _first(printouts.get("Magnitude"))
    summary = _enrich_summary(title, _first(printouts.get("Summary")))
    repute = _first(printouts.get("Repute"))
    if not magnitude and not summary:
        return None
    return SnpediaGenotypeFinding(
        rsid=rsid,
        genotype=genotype,
        magnitude=str(magnitude),
        repute=str(repute),
        summary=str(summary),
        url=str(item.get("fullurl", "")),
    )


def _parse_title(title: str) -> tuple[str, str] | None:
    match = re.match(r"^([A-Za-z]+\d+)\(([ACGTID]);([ACGTID])\)$", title.strip(), re.IGNORECASE)
    if not match:
        return None
    return normalize_rsid(match.group(1)), f"({match.group(2).upper()};{match.group(3).upper()})"


def _first(values: object) -> object:
    if isinstance(values, list) and values:
        return values[0]
    return ""
