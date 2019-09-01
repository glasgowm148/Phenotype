import argparse
import os
import string
import json
from pathlib import Path


class PersonalData:
    def __init__(self, rsidpath):
        if os.path.exists(rsidpath):
            self.readData(rsidpath)
            self.export()

    def readData(self, rsidpath):
        with open(rsidpath) as file:
            relevantdata = [line for line in file.readlines() if line[0] != "#"]
            file.close()
        self.personaldata = [line.split("\t") for line in relevantdata]
        self.snps = [item[0].lower() for item in self.personaldata]
        self.snpdict = {item[0].lower(): "(" + item[3].rstrip()[0] + ";" + item[3].rstrip()[-1] + ")" \
                        for item in self.personaldata}

    def hasGenotype(self, rsid):
        genotype = self.snpdict[rsid]
        return not genotype == "(-;-)"

    def export(self):
        rsidpath = Path(__file__).resolve().with_name('data') / 'snpDict.json'
        with open(rsidpath, "w") as jsonfile:
            json.dump(self.snpdict, jsonfile)




if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--rsidpath', help='rsidpath for json dump to be used for import', required=False)

    args = vars(parser.parse_args())

    if args["rsidpath"]:
        pd = PersonalData(rsidpath=args["rsidpath"])
        print(len(pd.personaldata))
        print(pd.snps[:50])
        print(list(pd.snpdict.keys())[:10])
        print(list(pd.snpdict.values())[:10])
