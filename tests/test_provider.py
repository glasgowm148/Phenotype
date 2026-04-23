import json
from pathlib import Path

from bs4 import BeautifulSoup
from phenotype.models import SNPRecord
from phenotype.providers import combined, myvariant, snpedia_ncbi

FIXTURES = Path(__file__).parent / "fixtures"


def test_provider_extracts_record_from_saved_html(monkeypatch):
    def fake_read_html(url, timeout):
        if "snpedia.com" in url:
            path = FIXTURES / "snpedia_rs1303.html"
        elif "pmc" in url:
            path = FIXTURES / "pmc_rs1303.html"
        else:
            path = FIXTURES / "ncbi_rs1303.html"
        return BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")

    monkeypatch.setattr(snpedia_ncbi, "_read_html", fake_read_html)

    record = snpedia_ncbi.fetch_snp_record("RS1303")

    assert record.rsid == "rs1303"
    assert record.description == "Example SNPedia description"
    assert record.variations[0] == ["A", "Example variation A"]
    assert record.studies == "Example PMC study title"
    assert record.clinical_significance == ["benign"]
    assert record.gene == "EXAMPLE"
    assert record.risk == "A"
    assert record.risk_allele == "A"
    assert record.frequency_percent == 12.0


def test_provider_tolerates_missing_tables(monkeypatch):
    def fake_read_html(url, timeout):
        return BeautifulSoup((FIXTURES / "empty_provider_page.html").read_text(encoding="utf-8"), "html.parser")

    monkeypatch.setattr(snpedia_ncbi, "_read_html", fake_read_html)

    record = snpedia_ncbi.fetch_snp_record("rs404")

    assert record.rsid == "rs404"
    assert record.description == ""
    assert record.variations == []
    assert record.source_urls["ncbi"].endswith("/rs404")
    assert record.source_urls["studies"].endswith("term=rs404")


def test_myvariant_provider_extracts_api_record(monkeypatch):
    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return json.loads((FIXTURES / "myvariant_rs1303.json").read_text(encoding="utf-8"))

    monkeypatch.setattr(myvariant.requests, "get", lambda url, timeout: Response())

    record = myvariant.fetch_myvariant_record("RS1303")

    assert record.rsid == "rs1303"
    assert record.gene == "SERPINA1"
    assert record.description == "Example ClinVar condition"
    assert record.clinical_significance == ["benign", "example clinvar condition"]
    assert record.clinvar[0] == ["RCV000000001", "Benign", "Example ClinVar condition", "2024-03-15"]
    assert record.frequency == "T=88%"
    assert record.frequency_percent == 88
    assert record.classification_updated_at == "2024-03-15"
    assert record.source_urls["myvariant"].endswith("/rs1303")


def test_combined_provider_merges_api_and_html_records(monkeypatch):
    api_record = SNPRecord(
        rsid="rs1",
        gene="API",
        clinical_significance=["benign"],
        classification_updated_at="2024-01-02",
        source_urls={"myvariant": "https://myvariant.info/v1/variant/rs1"},
    )
    html_record = SNPRecord(
        rsid="rs1",
        description="HTML description",
        gene="HTML",
        risk_allele="A",
        variations=[["A", "variation"]],
        source_urls={"ncbi": "https://www.ncbi.nlm.nih.gov/snp/rs1"},
    )
    monkeypatch.setattr(combined, "fetch_myvariant_record", lambda rsid, timeout: api_record)
    monkeypatch.setattr(combined, "fetch_snpedia_ncbi_record", lambda rsid, timeout: html_record)

    record = combined.fetch_snp_record("rs1")

    assert record.gene == "API"
    assert record.description == "HTML description"
    assert record.risk_allele == "A"
    assert record.classification_updated_at == "2024-01-02"
    assert record.variations == [["A", "variation"]]
    assert record.source_urls == {
        "ncbi": "https://www.ncbi.nlm.nih.gov/snp/rs1",
        "myvariant": "https://myvariant.info/v1/variant/rs1",
    }


def test_myvariant_prefers_variant_with_clinvar_date(monkeypatch):
    class Response:
        def raise_for_status(self):
            return None

        def json(self):
            return [
                {"dbsnp": {"rsid": "rs1", "gene": {"symbol": "OLD"}}},
                {
                    "dbsnp": {"rsid": "rs1"},
                    "clinvar": {
                        "gene": {"symbol": "NEW"},
                        "rcv": {
                            "accession": "RCV1",
                            "clinical_significance": "Pathogenic",
                            "last_evaluated": "2025-02-02",
                            "conditions": {"name": "Example"},
                        },
                    },
                },
            ]

    monkeypatch.setattr(myvariant.requests, "get", lambda url, timeout: Response())

    record = myvariant.fetch_myvariant_record("rs1")

    assert record.gene == "NEW"
    assert record.classification_updated_at == "2025-02-02"
    assert record.clinical_significance == ["pathogenic", "example"]
