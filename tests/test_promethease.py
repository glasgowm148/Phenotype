import base64
import json
import zlib

from phenotype.promethease import genotype_frequency_percent, iter_report_records


def test_promethease_report_records_use_genotype_specific_frequency(tmp_path):
    item = {
        "rsnum": "rs1815739",
        "geno": "(T;T)",
        "repute": "Bad",
        "magnitude": 2.2,
        "genosummary": "Impaired muscle performance",
        "genes": ["ACTN3"],
        "numrefs": 18,
        "genotime": "2016-04-19",
        "popfreqalleth": ["CEU", "YRI"],
        "popfreqallgenos": ["(C;C)", "(C;T)", "(T;T)"],
        "popfreqallnum": [{"data": [22.1, 0]}, {"data": [58.4, 20.4]}, {"data": [19.5, 79.6]}],
    }
    payload = base64.b64encode(zlib.compress(json.dumps([item]).encode("utf-8"))).decode("ascii")
    path = tmp_path / "report.html"
    path.write_text(f"mygenos.push.apply(mygenos,decompressString('{payload}'));", encoding="utf-8")

    records = list(iter_report_records(path))

    assert len(records) == 1
    assert records[0].rsid == "rs1815739"
    assert records[0].frequency == "19.5% CEU genotype"
    assert records[0].frequency_percent == 19.5
    assert records[0].gene == "ACTN3"
    assert records[0].citations == "18"
    assert records[0].classification_updated_at == "2016-04-19"


def test_promethease_frequency_falls_back_to_popfreq():
    assert genotype_frequency_percent({"popfreq": {"CEU": 2.7}}, "(A;G)") == 2.7
