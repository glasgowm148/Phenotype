############################
#      Phenotype.dev       # 
#     Genome Analysis      #
############################

import sys
if (sys.version_info < (3, 0)):
	print ("Please use Python 3")
	exit()
from random import shuffle
import numpy as np 

from bs4 import BeautifulSoup
from pathlib import Path
import pandas as pd 

import urllib.request
import pprint
import json
import argparse
import os
import random

from GenomeImporter import PersonalData #imports your raw data
from SNPGen import GrabSNPs

class SNPCrawl:

########################## INITIALISE ####
    def __init__(self, rsids=[], filepath=None, snppath=None):
        
        # If .json's already exists
        if filepath and os.path.isfile(filepath): 
            self.importDict(filepath)
            self.rsidList = []
        else: 
            self.scrapedData = {}
            self.rsidList = []
        
        if snppath and os.path.isfile(snppath):
            self.importSNPs(snppath) 
        else:
            self.yourData = {}
        rsids = [item.lower() for item in rsids]
        if rsids:
            self.initcrawl(rsids)           # Crawl
        self.export()                       # Export
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
                response = urllib.request.urlopen(url)
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

######### IMPORTS ####
        # Latest Study
        try:
            url = "https://www.ncbi.nlm.nih.gov/pmc/?term=" + rsid.lower()
            response = urllib.request.urlopen(url)
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
            response = urllib.request.urlopen(url)
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
            if (len(study) > 0 and not self.scrapedData[rsid]["Studies"]):
                self.scrapedData[rsid]["Studies"] = study[1][1]
        except urllib.error.HTTPError:
            print(url + " was not found or on dbSNP or contained no valid information")
    
############# IMPORTS ####
        # ncbi.nlm.nih.gov
        try:
            url = "https://www.ncbi.nlm.nih.gov/snp/" + rsid.lower() + "#clinical_significance"
            response = urllib.request.urlopen(url)
            html = response.read()
            bs = BeautifulSoup(html, "html.parser")

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
                
                dbSNPTwo= []
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
    def rank(self):
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
        datapath = Path(__file__).resolve().with_name("data") / "scrapedData.csv"
        data.to_csv(datapath)
        filepath = Path(__file__).resolve().with_name("data") / "scrapedData.json"

        with open(filepath,"w") as jsonfile:
            json.dump(self.scrapedData, jsonfile)

##################### CLI PARSER ####
parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filepath", help="filepath for raw data to be used for import", required=False)
args = vars(parser.parse_args())
#####################################


##################### LOAD RSIDS ####
# SNPs can also be loaded directly like this
rsid = ["rs1303"]
rsid += ["rs1815739", "Rs53576", "rs4680", "rs1800497", "rs429358", "rs9939609", "rs4988235", "rs6806903", "rs4244285"]
# Load in snps_of_interest.txt
rsid += [line.rstrip() for line in open('SNPedia/data/snps_of_interest.txt')]
# Load in one_thousand_and_you.txt
rsid += [line.rstrip() for line in open('SNPedia/data/one_thousand_and_you.txt')]
#####################################

if args["filepath"]:
    personal = PersonalData(args["filepath"])
    snpsofinterest = [snp for snp in personal.snps if personal.hasGenotype(snp)]
    sp = GrabSNPs(crawllimit=60, snpsofinterest=snpsofinterest, target=100)
    rsid += sp.snps
    print("SNPs of interest to analyse:")
    print(len(sp.snps))
    temp = personal.snps
    random.shuffle(temp)
    print(temp[:10])
    rsid += temp[:50]


if __name__ == "__main__":
    filepath = Path(__file__).resolve().with_name("data") / "scrapedData.json"
    if filepath.is_file():
        dfCrawl = SNPCrawl(rsids=rsid, filepath=filepath)

    else:
        dfCrawl = SNPCrawl(rsids=rsid)
