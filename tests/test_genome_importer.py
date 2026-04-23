from pathlib import Path

from phenotype.genome_importer import PersonalData

FIXTURES = Path(__file__).parent / "fixtures"


def test_imports_23andme_format(tmp_path):
    export_path = tmp_path / "yourData.json"
    personal = PersonalData(FIXTURES / "23andme_sample.txt", export_path=export_path)

    assert personal.yourData["rs1303"] == "(A;G)"
    assert personal.assembly == "GRCh37"
    assert personal.annotation_release == "104"
    assert personal.variants[0].chromosome == "1"
    assert personal.variants[0].position == 1000
    assert personal.variants[0].zygosity == "heterozygous"
    assert personal.hasGenotype("rs1303")
    assert not personal.hasGenotype("missing")
    assert export_path.exists()


def test_imports_ancestry_format(tmp_path):
    personal = PersonalData(FIXTURES / "ancestry_sample.txt", export_path=tmp_path / "yourData.json")

    assert personal.yourData["rs1303"] == "A/G"
    assert personal.yourData["rs1815739"] == "C/C"
