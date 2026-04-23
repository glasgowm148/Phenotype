from __future__ import annotations

import argparse
import json
import random
from pathlib import Path

import pandas as pd

from phenotype.genome_importer import PersonalData
from phenotype.models import SNPRecord, normalize_rsid
from phenotype.paths import DATA_DIR, DEFAULT_SCRAPED_JSON
from phenotype.providers.combined import fetch_snp_record
from phenotype.providers.snpedia_ncbi import table_to_list
from phenotype.snpgen import GrabSNPs
from phenotype.storage import PhenotypeStore

DEFAULT_RSIDS = [
    "rs1303",
    "rs1815739",
    "rs53576",
    "rs4680",
    "rs1800497",
    "rs429358",
    "rs9939609",
    "rs4988235",
    "rs6806903",
    "rs4244285",
]


class SNPCrawl:
    def __init__(
        self,
        rsids: list[str] | None = None,
        filepath: str | Path | None = None,
        snppath: str | Path | None = None,
        store: PhenotypeStore | None = None,
    ):
        self.filepath = Path(filepath) if filepath else None
        self.snppath = Path(snppath) if snppath else None
        self.store = store
        self.scrapedData: dict[str, dict] = {}
        self.yourData: dict[str, str] = {}
        self.rsidList: list[dict[str, str]] = []

        if self.filepath and self.filepath.is_file():
            self.importDict(self.filepath)
        if self.snppath and self.snppath.is_file():
            self.importSNPs(self.snppath)

        rsids = [normalize_rsid(item) for item in rsids or []]
        if rsids:
            self.initcrawl(rsids)
        if rsids or not self.filepath:
            self.export()
        self.createList()

    def initcrawl(self, rsids: list[str]) -> None:
        run_id = self.store.create_scrape_run(len(rsids), "CLI scrape", rsids) if self.store else None
        failed = 0
        for count, rsid in enumerate(rsids, start=1):
            try:
                if run_id:
                    self.store.set_scrape_item_status(run_id, rsid, "running")
                self.grabTable(rsid)
                if run_id:
                    self.store.set_scrape_item_status(run_id, rsid, "complete")
            except Exception as exc:
                failed += 1
                if run_id:
                    self.store.set_scrape_item_status(run_id, rsid, "failed", str(exc))
                print(f"{rsid} failed: {exc}")
            if count % 50 == 0 or count == 5:
                self.export()
            if run_id:
                self.store.update_scrape_run(run_id, "running", count, failed)
        if run_id:
            self.store.update_scrape_run(run_id, "complete", len(rsids), failed)

    def grabTable(self, rsid: str) -> None:
        if rsid not in self.scrapedData:
            record = fetch_snp_record(rsid)
            self.scrapedData[rsid] = {
                "Description": record.description,
                "Variations": record.variations,
                "ClinVar": record.clinvar,
                "Frequency": record.frequency,
                "Studies": record.studies,
                "Citations": record.citations,
                "Gene": record.gene,
                "Risk": record.risk,
                "ClinicalSignificance": record.clinical_significance,
                "SourceUrls": record.source_urls,
            }
            if self.store:
                self.store.upsert_snps([record])

    def tableToList(self, table) -> list[list[str]]:
        return table_to_list(table)

    def rank(self, rsid: str) -> None:
        print("##RANK##")
        print(self.scrapedData[rsid]["ClinVar"])

    def createList(self) -> None:
        self.rsidList = [
            SNPRecord.from_legacy(rsid, payload).to_legacy(self.yourData.get(rsid.lower(), "(n/a)"))
            for rsid, payload in self.scrapedData.items()
        ]

    def importDict(self, filepath: str | Path) -> None:
        self.scrapedData = json.loads(Path(filepath).read_text(encoding="utf-8"))

    def importSNPs(self, snppath: str | Path) -> None:
        self.yourData = json.loads(Path(snppath).read_text(encoding="utf-8"))

    def export(self) -> None:
        DATA_DIR.mkdir(exist_ok=True)
        data = pd.DataFrame(self.scrapedData).fillna("-").transpose()
        data.to_csv(DATA_DIR / "scrapedData.csv")
        DEFAULT_SCRAPED_JSON.write_text(json.dumps(self.scrapedData), encoding="utf-8")
        if self.store:
            self.store.upsert_snps(
                SNPRecord.from_legacy(rsid, payload) for rsid, payload in self.scrapedData.items()
            )


def read_rsid_file(filename: str) -> list[str]:
    path = DATA_DIR / filename
    if not path.is_file():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_rsid_list(raw_filepath: str | Path | None = None, genotype_export_path: str | Path | None = None) -> list[str]:
    rsids = list(DEFAULT_RSIDS)
    rsids += read_rsid_file("snps_of_interest.txt")
    rsids += read_rsid_file("one_thousand_and_you.txt")

    if raw_filepath:
        personal_kwargs = {"export_path": genotype_export_path} if genotype_export_path else {}
        personal = PersonalData(raw_filepath, **personal_kwargs)
        snpsofinterest = [snp for snp in personal.snps if personal.hasGenotype(snp)]
        snps = GrabSNPs(crawllimit=60, snpsofinterest=snpsofinterest, target=100).snps
        rsids += snps
        temp = list(personal.snps)
        random.shuffle(temp)
        rsids += temp[:50]

    seen = set()
    unique = []
    for rsid in rsids:
        rsid = normalize_rsid(rsid)
        if rsid and rsid not in seen:
            seen.add(rsid)
            unique.append(rsid)
    return unique


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filepath", help="raw genome file to import before scraping", required=False)
    parser.add_argument("--db", help="SQLite database path", required=False)
    args = parser.parse_args(argv)

    store = PhenotypeStore(args.db) if args.db else PhenotypeStore()
    filepath = DEFAULT_SCRAPED_JSON if DEFAULT_SCRAPED_JSON.is_file() else None
    rsids = build_rsid_list(args.filepath)
    SNPCrawl(rsids=rsids, filepath=filepath, store=store)


if __name__ == "__main__":
    main()
