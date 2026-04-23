from phenotype import snpedia_catalog
from phenotype.snpedia_catalog import (
    SnpediaGenotypeFinding,
    _finding_from_result,
    fetch_matching_genotype_finding,
    fetch_matching_known_genosets,
    matches_imported_genotype,
)


def test_catalog_result_parses_bad_genotype_page():
    finding = _finding_from_result(
        "Rs1800562(A;G)",
        {
            "printouts": {
                "Magnitude": [3],
                "Repute": ["Bad"],
                "Summary": ["One copy of C282Y"],
            },
            "fullurl": "https://bots.snpedia.com/index.php/Rs1800562(A;G)",
        },
    )

    assert finding.rsid == "rs1800562"
    assert finding.genotype == "(A;G)"
    assert finding.variation == ["(A;G)", "3", "Bad: One copy of C282Y"]


def test_catalog_match_allows_complement_and_indels():
    assert matches_imported_genotype(
        SnpediaGenotypeFinding("rs6025", "(A;G)", "4.1", "Bad", "risk", ""),
        "(C;T)",
    )
    assert not matches_imported_genotype(
        SnpediaGenotypeFinding("rs104893931", "(T;T)", "6", "Bad", "risk", ""),
        "(A;A)",
    )
    assert matches_imported_genotype(
        SnpediaGenotypeFinding("i3003626", "(I;I)", "0", "Bad", "reported", ""),
        "(I;I)",
    )


def test_exact_genotype_fetch_tries_direct_page(monkeypatch):
    def fake_ask(query, timeout):
        assert "[[Rs4307059(T;T)]]" in query
        return {
            "query": {
                "results": {
                    "Rs4307059(T;T)": {
                        "printouts": {
                            "Magnitude": [3],
                            "Repute": ["Bad"],
                            "Summary": ["1.42x risk of Autism"],
                        }
                    }
                }
            }
        }

    monkeypatch.setattr(snpedia_catalog, "_ask", fake_ask)

    finding = fetch_matching_genotype_finding("rs4307059", "(T;T)")

    assert finding.rsid == "rs4307059"
    assert finding.variation == ["(T;T)", "3", "Bad: 1.42x risk of Autism"]


def test_known_genoset_rules_match_imported_genotypes(monkeypatch):
    def fake_ask(query, timeout):
        title = query.split("[[", 1)[1].split("]]", 1)[0]
        return {
            "query": {
                "results": {
                    title: {
                        "printouts": {
                            "Magnitude": [2.1],
                            "Repute": ["Bad"],
                            "Summary": ["Example genoset"],
                        }
                    }
                }
            }
        }

    monkeypatch.setattr(snpedia_catalog, "_ask", fake_ask)

    findings = fetch_matching_known_genosets(
        {
            "rs10483639": "(C;G)",
            "rs3783641": "(A;T)",
            "rs8007267": "(C;T)",
        }
    )

    assert [finding.rsid for finding in findings] == ["gs223"]
    assert findings[0].variation == ["(match)", "2.1", "Bad: Example genoset"]
