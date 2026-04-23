from phenotype.vep import iter_vep_tab, parse_extra


def test_parse_extra_reads_vep_key_values():
    assert parse_extra("IMPACT=HIGH;SYMBOL=F5;CANONICAL=YES") == {
        "IMPACT": "HIGH",
        "SYMBOL": "F5",
        "CANONICAL": "YES",
    }


def test_iter_vep_tab_extracts_rsid_and_consequence_fields(tmp_path):
    path = tmp_path / "vep.txt"
    path.write_text(
        "\t".join(
            [
                "#Uploaded_variation",
                "Location",
                "Allele",
                "Gene",
                "Feature",
                "Feature_type",
                "Consequence",
                "Existing_variation",
                "Extra",
            ]
        )
        + "\n"
        + "\t".join(
            [
                "rs6025",
                "1:169519049",
                "A",
                "ENSG00000198734",
                "ENST00000367797",
                "Transcript",
                "missense_variant",
                "rs6025",
                "IMPACT=MODERATE;SYMBOL=F5;HGVSp=ENSP00000356771.4:p.Arg534Gln",
            ]
        )
        + "\n",
        encoding="utf-8",
    )

    rows = list(iter_vep_tab(path))

    assert rows == [
        {
            "rsid": "rs6025",
            "uploaded_variation": "rs6025",
            "location": "1:169519049",
            "allele": "A",
            "gene": "ENSG00000198734",
            "feature": "ENST00000367797",
            "feature_type": "Transcript",
            "consequence": "missense_variant",
            "impact": "MODERATE",
            "symbol": "F5",
            "hgvsc": "",
            "hgvsp": "ENSP00000356771.4:p.Arg534Gln",
            "existing_variation": "rs6025",
            "extra": {
                "IMPACT": "MODERATE",
                "SYMBOL": "F5",
                "HGVSp": "ENSP00000356771.4:p.Arg534Gln",
            },
        }
    ]
