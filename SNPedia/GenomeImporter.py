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
        with open(filepath) as file:
            if "Ancestry" in file.readline():
                dataSource = "Ancestry"
                print("Ancestry data loaded")
            elif "23andme" in file.readline():
                dataSource = "23andme"
                print("23andme data loaded")
                
            relevantdata = [line for line in file.readlines() if line[0] != "#"]
                        
            
                   
            file.close()
        self.personaldata = [line.split("\t") for line in relevantdata]
        self.snps = [item[0].lower() for item in self.personaldata]
        
        # convert AncestryDNA raw data
       # self.yourData = {item[0].lower(): "(" + ''.join(item[-2:]) + ")" \
       #         for item in self.personaldata}
        self.yourData = {item[0].lower().strip("\n\t "): item[-2] + '/' + item[-1] \
                        for item in self.personaldata}
        ###################
        
        
        #
        # 23andme code
        #self.yourData = {item[0].lower(): "(" + item[3].rstrip()[0] + ";" + item[3].rstrip()[-1] + ")" \
        #                for item in self.personaldata}

        # for item in self.personaldata:
         #   if "23andme" in item:
          #      self.yourData = {item[0].lower(): "(" + item[3].rstrip()[0] + ";" + item[3].rstrip()[-1] + ")" }
           # elif "Ancestry" in item:
            #    self.yourData = {item[0].lower().strip("\n\t "): item[-2] + '/' + item[-1] }


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
