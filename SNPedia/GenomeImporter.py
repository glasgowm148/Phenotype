import argparse
import os
import string
import json
from pathlib import Path


class PersonalData:
    def __init__(self, filepath):
        if os.path.exists(filepath):
            self.readData(filepath)
            self.export()

    def readData(self, filepath):
        dataSource = True #Ugly fix for
        with open(filepath) as file:
            if "Ancestry" in file.readline():
                dataSource = False
            relevantdata = [line for line in file.readlines() if line[0] != "#"]     
            self.personaldata = [line.split("\t") for line in relevantdata]
            self.snps = [item[0].lower() for item in self.personaldata]

            if dataSource == False:
                self.yourData = {item[0].rstrip("\n\t"): item[-2].rstrip("\n\t ") + '/' + item[-1] \
                            for item in self.personaldata}
                print("Ancestry data loaded to data/yourData.json")
            if dataSource ==True:
                self.yourData = {item[0].lower(): ''.join(item[-2:]) \
                    for item in self.personaldata}
                print("23andme data loaded to data/yourData.json")


        file.close()
        
    


    def hasGenotype(self, rsid):
        genotype = self.yourData[rsid]
        return not genotype == "(-;-)"

    def export(self):
        filepath = Path(__file__).resolve().with_name('data') / 'yourData.json'
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
