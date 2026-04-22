import argparse
import json
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent / "data"


class PersonalData:
    def __init__(self, filepath):
        self.personaldata = []
        self.snps = []
        self.yourData = {}
        if Path(filepath).exists():
            self.readData(filepath)
            self.export()

    def readData(self, filepath):
        lines = Path(filepath).read_text(encoding="utf-8", errors="replace").splitlines()
        is_ancestry = any("Ancestry" in line for line in lines[:5])
        relevantdata = [line for line in lines if line and not line.startswith("#")]
        self.personaldata = [line.split("\t") for line in relevantdata]
        self.personaldata = [item for item in self.personaldata if item and item[0]]
        self.snps = [item[0].lower() for item in self.personaldata]

        if is_ancestry:
            self.yourData = {
                item[0].lower(): item[-2].strip() + "/" + item[-1].strip()
                for item in self.personaldata
                if len(item) >= 2
            }
            print("Ancestry data loaded to data/yourData.json")
        else:
            self.yourData = {
                item[0].lower(): "(" + item[3].strip()[0] + ";" + item[3].strip()[-1] + ")"
                for item in self.personaldata
                if len(item) >= 4 and item[3].strip()
            }
            print("23andme data loaded to data/yourData.json")


    def hasGenotype(self, rsid):
        genotype = self.yourData.get(rsid.lower(), "(-;-)")
        return not genotype == "(-;-)"

    def export(self):
        DATA_DIR.mkdir(exist_ok=True)
        filepath = DATA_DIR / 'yourData.json'
        with open(filepath, "w") as jsonfile:
            json.dump(self.yourData, jsonfile)




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--filepath', help='filepath for json dump to be used for import', required=False)

    args = vars(parser.parse_args())

    if args["filepath"]:
        pd = PersonalData(filepath=args["filepath"])
        print(len(pd.personaldata))
        print(pd.snps[:50])
        print(list(pd.yourData.keys())[:10])
        print(list(pd.yourData.values())[:10])
