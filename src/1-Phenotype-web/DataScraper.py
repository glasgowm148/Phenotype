############################
#      Phenotype.dev       # 
#     Genome Analysis      #
############################

import json
import argparse
import pprint
import random
import urllib.error
import urllib.request
from pathlib import Path

import pandas as pd
from bs4 import BeautifulSoup

from GenomeImporter import PersonalData #imports your raw data
from SNPGen import GrabSNPs


APP_DIR = Path(__file__).resolve().parent
DATA_DIR = APP_DIR / "data"
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

########################## INITIALISE ####
    def __init__(self, rsids=None, filepath=None, snppath=None):
        rsids = rsids or []
        
        # If .json's already exists
        if filepath and Path(filepath).is_file():
            self.importDict(filepath)
        else: 
            self.scrapedData = {}
        self.rsidList = []
        
        if snppath and Path(snppath).is_file():
            self.importSNPs(snppath) 
        else:
            self.yourData = {}
        rsids = [item.lower() for item in rsids]
        if rsids:
            self.initcrawl(rsids)           # Crawl
        if rsids or not filepath:
            self.export()                   # Export
        self.createList()                   # Create List

#################### crawl ####
    def initcrawl(self, rsids):
        print("####### Starting to crawl.... #######")
        count = 0
        for rsid in rsids:
            print("rsid:" + rsid)
            
            self.grabTable(rsid) #### Goto IMPORTS
            print("output :: ")
            print(self.scrapedData[rsid])
            print("")
            count += 1
            if count % 50 == 0 or count == 5:
                print("#########################")
                print("%i out of %s completed" % (count, len(rsids)))
                print("####### exporting #######")
                self.export() 
                print("#########################")
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(self.scrapedData)

################ IMPORTS ####
    def grabTable(self, rsid):
       # Description & Variation
        try:
            #("Retrieving data..... ")
            url = "https://bots.snpedia.com/index.php/" + rsid.lower()
            if rsid not in self.scrapedData.keys():
                self.scrapedData[rsid.lower()] = {
                    "Description": "",
                    "Variations": [],
                    "ClinVar": [],
                    "Frequency": "",
                    "Studies": "",
                    "Citations": "",
                    "Gene": "",
                    "Risk": ""
                }
                response = urllib.request.urlopen(url, timeout=30)
                html = response.read()
                bs = BeautifulSoup(html, "html.parser")
                table = bs.find("table", {"class": "sortable smwtable"})
                description = bs.find("table", {"style": "border: 1px; background-color: #FFFFC0; border-style: solid; margin:1em; width:90%;"})
                
                if description:
                    d1 = self.tableToList(description)
                    self.scrapedData[rsid]["Description"] = d1[0][0]
                    #print(d1[0][0].encode("utf-8"))

                if table:
                    d2 = self.tableToList(table)
                    self.scrapedData[rsid]["Variations"] = d2[1:]
                    #print(d2[1:])

        except urllib.error.HTTPError:
            print(url + " was not found on snpedia or contained no valid information")
        except urllib.error.URLError:
            print(url + " could not be reached")

######### IMPORTS ####
        # Latest Study
        try:
            url = "https://www.ncbi.nlm.nih.gov/pmc/?term=" + rsid.lower()
            response = urllib.request.urlopen(url, timeout=30)
            html = response.read()
            bs = BeautifulSoup(html, "html.parser")
            study = []
            for div in bs.find_all(class_='title'):
                for childdiv in div.find_all('a'):
                    if childdiv.string != None : 
                        study.append(childdiv.string)
            if (len(study) > 1):
                self.scrapedData[rsid]["Studies"] = study[0]
        except urllib.error.HTTPError:
            print(url + " was not found or on dbSNP term search or contained no valid information")
        except urllib.error.URLError:
            print(url + " was not found or on dbSNP term search or contained no valid information")


        try:
            url = "https://www.ncbi.nlm.nih.gov/snp/" + rsid.lower() + "#publications"
            response = urllib.request.urlopen(url, timeout=30)
            html = response.read()
            bs = BeautifulSoup(html, "html.parser")
            publications = bs.find(id="publication_datatable")
            study = []
            if publications:
                rows = publications.find_all("tr")
                for row in rows:
                    cols = row.find_all("td")
                    cols = [ele.text.strip() for ele in cols]
                    study.append(cols)
            if (len(study) > 1 and not self.scrapedData[rsid]["Studies"]):
                self.scrapedData[rsid]["Studies"] = study[1][1]
        except urllib.error.HTTPError:
            print(url + " was not found or on dbSNP or contained no valid information")
        except urllib.error.URLError:
            print(url + " was not found or on dbSNP or contained no valid information")
    
############# IMPORTS ####
        # ncbi.nlm.nih.gov
        try:
            url = "https://www.ncbi.nlm.nih.gov/snp/" + rsid.lower() + "#clinical_significance"
            response = urllib.request.urlopen(url, timeout=30)
            html = response.read()
            bs = BeautifulSoup(html, "html.parser")
            dbSNPTwo = []

            classification = bs.find(id="clinical_significance")
            
            if classification:
                rows = classification.find_all("tr")
                ClinVar = []
                for row in rows:
                    cols = row.find_all("td")
                    cols = [ele.text.strip() for ele in cols]
                    ClinVar.append([ele for ele in cols if ele])
                
                if(len(ClinVar) > 0):
                    if(len(ClinVar) > 7):
                        self.scrapedData[rsid]["ClinVar"] = ClinVar[-6:-1]
                    else:
                        self.scrapedData[rsid]["ClinVar"] = ClinVar[1:]

            ncbi = bs.find(class_="summary-box usa-grid-full")
            if ncbi:
                dbSNP = []

                rows = ncbi.find_all("div")
                
                for row in rows:
                    cols = row.find_all("div")
                    cols = [ele.text.strip() for ele in cols]
                    dbSNP.append(cols)

                try:
                    self.scrapedData[rsid]["Risk"] = dbSNP[2][0][0]
                    self.scrapedData[rsid]["Frequency"] = dbSNP[2][0][3:7]
                except IndexError:
                    print("index error")
                
                rows = ncbi.find_all("dl")
                
                for row in rows:
                    cols = row.find_all("dd")
                    cols = [ele.text.strip() for ele in cols]
                    dbSNPTwo.append(cols)
        
            try:
                print(dbSNPTwo[1][1].split(' ')[0]) #gene
                self.scrapedData[rsid]["Gene"] = dbSNPTwo[1][1].split(' ')[0]
                print(dbSNPTwo[1][2][0]) #publications
                self.scrapedData[rsid]["Citations"] = dbSNPTwo[1][2][0]
            except IndexError:
                    print("index error")


        except urllib.error.HTTPError:
            print(url + " was not found or on dbSNP or contained no valid information")
        except urllib.error.URLError:
            print(url + " was not found or on dbSNP or contained no valid information")


 ############## IMPORT/Variation function ####
    def tableToList(self, table):
        rows = table.find_all("tr")
        data = []
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data

# IMPORT/Rank function ####
    def rank(self, rsid):
        print("##RANK##")
        print(self.scrapedData[rsid]["ClinVar"])


####### Create List ####
    def createList(self):
        make = lambda rsname, description, classifications, freq, risk, citations, gene, study, variations: \
            {
            "Name": rsname,
            "Description": description,
            "ClinVar":  "<br>".join(["<br>".join(s[1:]) if isinstance(s,list) else s for s in classifications]),
            "Genotype": self.yourData[rsname.lower()] if rsname.lower() in self.yourData.keys() else "(n/a)", 
            "Frequency": freq,
            "Citations": citations,
            "Gene": gene,
            "Risk": risk,
            "Studies": study,
            "Variations": str.join("<br>", variations)
             }

        # Highlight users genotype in bold
        formatCell = lambda rsid, variation : \
            "<b>" + str.join(" ", variation) + "</b>" \
                if rsid.lower() in self.yourData.keys() and \
                   self.yourData[rsid.lower()] == variation[0] \
                else str.join(" ", variation)
                
        for rsid in self.scrapedData.keys():
            curdict = self.scrapedData[rsid]
            variations = [formatCell(rsid, variation) for variation in curdict["Variations"]]
            self.rsidList.append(make(rsid, curdict["Description"], curdict["ClinVar"], curdict["Frequency"], curdict["Risk"],curdict["Citations"], curdict["Gene"], curdict["Studies"], variations))
        

    def importDict(self, filepath):
        with open(filepath, 'r') as jsonfile:
            self.scrapedData = json.load(jsonfile)

    def importSNPs(self, snppath):
        with open(snppath, 'r') as jsonfile:
            self.yourData = json.load(jsonfile)

    def export(self):
        data = pd.DataFrame(self.scrapedData)
        data = data.fillna("-")
        data = data.transpose()
        DATA_DIR.mkdir(exist_ok=True)
        datapath = DATA_DIR / "scrapedData.csv"
        data.to_csv(datapath)
        filepath = DATA_DIR / "scrapedData.json"

        with open(filepath,"w") as jsonfile:
            json.dump(self.scrapedData, jsonfile)

def read_rsid_file(filename):
    path = DATA_DIR / filename
    if not path.is_file():
        return []
    return [line.strip() for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def build_rsid_list(raw_filepath=None):
    rsids = list(DEFAULT_RSIDS)
    rsids += read_rsid_file("snps_of_interest.txt")
    rsids += read_rsid_file("one_thousand_and_you.txt")

    if raw_filepath:
        personal = PersonalData(raw_filepath)
        snpsofinterest = [snp for snp in personal.snps if personal.hasGenotype(snp)]
        sp = GrabSNPs(crawllimit=60, snpsofinterest=snpsofinterest, target=100)
        rsids += sp.snps
        print("SNPs of interest to analyse:")
        print(len(sp.snps))
        temp = list(personal.snps)
        random.shuffle(temp)
        print(temp[:10])
        rsids += temp[:50]

    return rsids


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filepath", help="filepath for raw data to be used for import", required=False)
    args = parser.parse_args()

    filepath = DATA_DIR / "scrapedData.json"
    rsids = build_rsid_list(args.filepath)
    dfCrawl = SNPCrawl(rsids=rsids, filepath=filepath if filepath.is_file() else None)
