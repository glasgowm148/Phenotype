from phenotype.models import (
    clinical_significance_category,
    clinvar_findings,
    normalize_frequency_percent,
    personal_significance,
    snpedia_genotype_match,
    snpedia_matched_finding,
)


def test_frequency_normalization_handles_decimal_fractions():
    assert normalize_frequency_percent(".363") == 36.3
    assert normalize_frequency_percent("0.12") == 12.0
    assert normalize_frequency_percent("1") == 1.0
    assert normalize_frequency_percent("12%") == 12.0
    assert normalize_frequency_percent("0") is None
    assert normalize_frequency_percent("A=0%") is None
    assert normalize_frequency_percent("363") is None


def test_personal_significance_scores_clinical_risk_matches():
    result = personal_significance(["pathogenic"], "AG", "A")

    assert result == {
        "label": "Pathogenic match",
        "score": 100,
        "clinical_score": 100,
        "frequency_context": "frequency unknown",
    }
    assert personal_significance(["pathogenic"], "GG", "A")["score"] == 0


def test_personal_significance_penalizes_common_variants():
    assert personal_significance(["pathogenic"], "AG", "A", 71)["score"] == 20
    assert personal_significance(["pathogenic"], "AG", "A", 37.3)["score"] == 35
    assert personal_significance(["pathogenic"], "AG", "A", 6)["score"] == 75


def test_snpedia_genotype_match_detects_complementary_strand():
    assert snpedia_genotype_match([["A;G", "direct"]], "(G;A)") == "direct"
    assert snpedia_genotype_match([["C;T", "complement"]], "(A;G)") == "complement"
    assert snpedia_genotype_match([["T;T", "homozygous complement"]], "(A;A)") == "none"
    assert snpedia_genotype_match([["T;T", "different"]], "(A;G)") == "none"


def test_clinvar_findings_summarize_severity_and_dates():
    findings = clinvar_findings(
        [
            ["RCV1", "Benign", "not specified", "2024-01-01"],
            ["RCV2", "risk factor", "Hashimoto thyroiditis", "2025-02-03"],
        ]
    )

    assert findings[0]["summary"] == "Risk factor: Hashimoto thyroiditis"
    assert findings[0]["severity_class"] == "risk"
    assert findings[0]["date"] == "2025-02-03"


def test_clinvar_findings_handle_condition_significance_order():
    findings = clinvar_findings([["RCV1", "Ischemic stroke, susceptibility to", "Risk-Factor"]])

    assert findings[0]["significance"] == "Risk-Factor"
    assert findings[0]["condition"] == "Ischemic stroke, susceptibility to"
    assert findings[0]["severity_class"] == "risk"


def test_clinvar_findings_classify_filter_categories():
    findings = clinvar_findings(
        [
            ["RCV1", "drug response", "Warfarin response", "2025-01-01"],
            ["RCV2", "benign/likely benign", "not specified", "2025-01-02"],
            ["RCV3", "likely risk allele", "Trait association", "2025-01-03"],
        ]
    )

    by_significance = {finding["significance"]: finding for finding in findings}
    assert by_significance["drug response"]["severity_class"] == "drug"
    assert by_significance["benign/likely benign"]["severity_class"] == "benign"
    assert by_significance["likely risk allele"]["severity_class"] == "risk"
    assert clinical_significance_category(["benign/likely benign"]) == ("Benign", 0)


def test_snpedia_matched_finding_summarizes_complement_risk_note():
    finding = snpedia_matched_finding(
        [["A;G", "4.1", "3.5-4.4x risk of thrombosis"]],
        "(C;T)",
        "complement",
    )

    assert finding["severity"] == "Risk"
    assert finding["severity_class"] == "risk"
    assert finding["magnitude"] == "4.1"
    assert finding["note"] == "3.5-4.4x risk of thrombosis"


def test_snpedia_risk_note_can_raise_benign_clinvar_row():
    from phenotype.models import SNPRecord

    row = SNPRecord(
        rsid="rs180223",
        clinical_significance=["benign"],
        variations=[["(G;T)", "2.8", "1.3x to 11.5x increased risk"]],
    ).to_legacy("(G;T)")

    assert row["Significance"] == "SNPedia risk note"
    assert row["SignificanceScore"] == 50
    assert row["FindingSeverityClass"] == "risk"
    assert row["IsRiskMatch"] is True


def test_snpedia_magnitude_match_counts_as_finding_match():
    from phenotype.models import SNPRecord

    row = SNPRecord(
        rsid="rs53576",
        clinical_significance=["benign"],
        variations=[["(A;G)", "2.8", "Lack of empathy?"]],
    ).to_legacy("(A;G)")

    assert row["Significance"] == "SNPedia magnitude note"
    assert row["SignificanceScore"] == 28
    assert row["FindingSeverityClass"] == "modifier"
    assert row["IsRiskMatch"] is True


def test_snpedia_genoset_match_counts_as_promethease_match():
    from phenotype.models import SNPRecord

    row = SNPRecord(
        rsid="gs223",
        variations=[["(match)", "2.1", "Bad: One copy of GCH1 variant"]],
    ).to_legacy("(match)")

    assert row["HasClinicalAlleleMatch"] is False
    assert row["HasPrometheaseMatch"] is True
    assert row["SNPediaGenotypeMatch"] == "direct"


def test_snpedia_unknown_note_does_not_raise_rating():
    finding = snpedia_matched_finding([["(A;G)", "?", "?"]], "(A;G)", "direct")

    assert finding["severity_score"] == 0
    assert finding["summary"] == ""


def test_source_allele_match_requires_actionable_clinical_assertion():
    from phenotype.models import SNPRecord

    benign = SNPRecord(rsid="rs1", risk_allele="A", clinical_significance=["benign"]).to_legacy("(A;G)")
    risk = SNPRecord(rsid="rs2", risk_allele="A", clinical_significance=["risk factor"]).to_legacy("(A;G)")

    assert benign["IsRiskMatch"] is False
    assert risk["IsRiskMatch"] is True
