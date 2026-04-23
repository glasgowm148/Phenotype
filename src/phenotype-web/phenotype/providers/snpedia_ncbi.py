from __future__ import annotations

import re
import urllib.error
import urllib.request

from bs4 import BeautifulSoup

from phenotype.models import SNPRecord, normalize_clinical_significance, normalize_rsid


def fetch_snp_record(rsid: str, timeout: int = 30) -> SNPRecord:
    rsid = normalize_rsid(rsid)
    record = SNPRecord(rsid=rsid)
    record.source_urls = {
        "snpedia": snpedia_url(rsid),
        "ncbi": f"https://www.ncbi.nlm.nih.gov/snp/{rsid}",
        "studies": f"https://pubmed.ncbi.nlm.nih.gov/?term={rsid}",
    }
    _fetch_snpedia(record, timeout)
    _fetch_ncbi_studies(record, timeout)
    _fetch_ncbi_summary(record, timeout)
    return record


def table_to_list(table) -> list[list[str]]:
    rows = table.find_all("tr")
    data = []
    for row in rows:
        cols = [ele.text.strip() for ele in row.find_all("td")]
        data.append([ele for ele in cols if ele])
    return data


def _read_html(url: str, timeout: int) -> BeautifulSoup | None:
    try:
        response = urllib.request.urlopen(url, timeout=timeout)
        return BeautifulSoup(response.read(), "html.parser")
    except (urllib.error.HTTPError, urllib.error.URLError):
        return None


def _fetch_snpedia(record: SNPRecord, timeout: int) -> None:
    bs = _read_html(snpedia_url(record.rsid), timeout)
    if not bs:
        return
    table = bs.find("table", {"class": "sortable smwtable"})
    description = bs.find(
        "table",
        {"style": "border: 1px; background-color: #FFFFC0; border-style: solid; margin:1em; width:90%;"},
    )
    if description:
        data = table_to_list(description)
        record.description = data[0][0] if data and data[0] else ""
    if table:
        data = table_to_list(table)
        record.variations = data[1:]


def _fetch_ncbi_studies(record: SNPRecord, timeout: int) -> None:
    bs = _read_html(f"https://www.ncbi.nlm.nih.gov/pmc/?term={record.rsid}", timeout)
    if bs:
        studies = [
            child.string
            for div in bs.find_all(class_="title")
            for child in div.find_all("a")
            if child.string is not None
        ]
        if studies:
            record.studies = studies[0]

    bs = _read_html(f"https://www.ncbi.nlm.nih.gov/snp/{record.rsid}#publications", timeout)
    if not bs or record.studies:
        return
    publications = bs.find(id="publication_datatable")
    if publications:
        rows = []
        for row in publications.find_all("tr"):
            cols = [ele.text.strip() for ele in row.find_all("td")]
            rows.append(cols)
        if len(rows) > 1 and len(rows[1]) > 1:
            record.studies = rows[1][1]


def _fetch_ncbi_summary(record: SNPRecord, timeout: int) -> None:
    bs = _read_html(f"https://www.ncbi.nlm.nih.gov/snp/{record.rsid}#clinical_significance", timeout)
    if not bs:
        return
    classification = bs.find(id="clinical_significance")
    if classification:
        clinvar = []
        for row in classification.find_all("tr"):
            cols = [ele.text.strip() for ele in row.find_all("td")]
            clinvar.append([ele for ele in cols if ele])
        if clinvar:
            record.clinvar = clinvar[-6:-1] if len(clinvar) > 7 else clinvar[1:]
            record.clinical_significance = normalize_clinical_significance(record.clinvar)

    ncbi = bs.find(class_="summary-box usa-grid-full")
    if not ncbi:
        return

    summary_text = ncbi.get_text(" ", strip=True)
    allele_frequency = re.search(r"\b([ACGT])\s*=\s*([0-9.]+%?)", summary_text)
    if allele_frequency:
        record.risk = allele_frequency.group(1)
        record.risk_allele = allele_frequency.group(1)
        record.frequency = allele_frequency.group(2)
        record.frequency_percent = float(allele_frequency.group(2).strip("%"))
    else:
        dbsnp = []
        for row in ncbi.find_all("div"):
            cols = [ele.text.strip() for ele in row.find_all("div")]
            dbsnp.append(cols)
        try:
            record.risk = dbsnp[2][0][0]
            record.risk_allele = record.risk
            record.frequency = dbsnp[2][0][3:7]
        except IndexError:
            pass

    dds = []
    for row in ncbi.find_all("dl"):
        dds.append([ele.text.strip() for ele in row.find_all("dd")])
    try:
        record.gene = dds[1][1].split(" ")[0]
        record.citations = dds[1][2][0]
    except IndexError:
        pass


def snpedia_url(rsid: str) -> str:
    title = "Rs" + normalize_rsid(rsid).removeprefix("rs")
    return f"https://www.snpedia.com/index.php/{title}"
