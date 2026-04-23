from pathlib import Path

from phenotype.scraper import DEFAULT_RSIDS, build_rsid_list

FIXTURES = Path(__file__).parent / "fixtures"


def test_build_rsid_list_deduplicates_defaults():
    rsids = build_rsid_list()

    assert "rs1303" in rsids
    assert len(rsids) == len(set(rsids))
    assert len(rsids) >= len(DEFAULT_RSIDS)


def test_build_rsid_list_can_include_raw_file_without_network(tmp_path, monkeypatch):
    class FakeGrabSNPs:
        def __init__(self, **kwargs):
            self.snps = ["rs1303", "rs999999"]

    monkeypatch.setattr("phenotype.scraper.GrabSNPs", FakeGrabSNPs)

    rsids = build_rsid_list(FIXTURES / "23andme_sample.txt", genotype_export_path=tmp_path / "yourData.json")

    assert "rs999999" in rsids
    assert "i3000001" in rsids
    assert (tmp_path / "yourData.json").exists()
