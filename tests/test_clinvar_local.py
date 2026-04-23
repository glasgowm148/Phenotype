import gzip

from phenotype.clinvar_local import iter_variant_summary, normalize_clinvar_date, rsids_from_cell


def test_clinvar_date_and_rsid_helpers():
    assert normalize_clinvar_date("Dec 17, 2024") == "2024-12-17"
    assert normalize_clinvar_date("-") == ""
    assert rsids_from_cell("123|456") == ["rs123", "rs456"]


def test_iter_variant_summary_parses_tsv(tmp_path):
    path = tmp_path / "variant_summary.txt.gz"
    content = "\t".join(
        [
            "#AlleleID",
            "Type",
            "Name",
            "GeneID",
            "GeneSymbol",
            "HGNC_ID",
            "ClinicalSignificance",
            "ClinSigSimple",
            "LastEvaluated",
            "RS# (dbSNP)",
            "nsv/esv (dbVar)",
            "RCVaccession",
            "PhenotypeIDS",
            "PhenotypeList",
            "Origin",
            "OriginSimple",
            "Assembly",
            "ChromosomeAccession",
            "Chromosome",
            "Start",
            "Stop",
            "ReferenceAllele",
            "AlternateAllele",
            "Cytogenetic",
            "ReviewStatus",
            "NumberSubmitters",
            "Guidelines",
            "TestedInGTR",
            "OtherIDs",
            "SubmitterCategories",
            "VariationID",
        ]
    )
    content += "\n10\tSNV\tExample\t1\tGENE\tHGNC:1\tPathogenic\t1\tJan 02, 2025\t123\t-\tRCV1|RCV2\t-\tDisease\t-\t-\tGRCh38\t-\t1\t1\t1\tA\tG\t-\treviewed\t1\t-\tN\t-\t1\t100\n"
    with gzip.open(path, "wt", encoding="utf-8") as file:
        file.write(content)

    rows = list(iter_variant_summary(path))

    assert rows[0]["rsid"] == "rs123"
    assert rows[0]["gene"] == "GENE"
    assert rows[0]["last_evaluated"] == "2025-01-02"
    assert rows[0]["rcv_accession"] == "RCV1"
