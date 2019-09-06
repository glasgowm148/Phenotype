############################
#    Phenotype.dev          
#    Genome Analysis       


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

from GenomeImporter import PersonalData 
from SNPGen import GrabSNPs

class SNPCrawl:
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
            self.initcrawl(rsids)
        self.export()
        self.createList()

    def initcrawl(self, rsids):
        print("####### Starting to crawl.... #######")
        count = 0
        for rsid in rsids:
            print("RSID:" + rsid)
            self.grabTable(rsid) # imports
            print("")
            count += 1
            if count % 25 == 0 or count == 5:
                print("%i out of %s completed" % (count, len(rsids)))
                self.export()
                print("exporting current results")
        pp = pprint.PrettyPrinter(indent=1)
        pp.pprint(self.scrapedData)


    def grabTable(self, rsid):
       
       #########################
       # Description & Variation
        try:
            print("####### SNPedia import for " + rsid )
            url = "https://bots.snpedia.com/index.php/" + rsid.lower()
            if rsid not in self.scrapedData.keys():
                self.scrapedData[rsid.lower()] = {
                    "Description": "",
                    "Variations": [],
                    "ClinVar": [],
                    "Frequency": "",
                    "Studies": "",
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
                    print(d1[0][0].encode("utf-8"))

                if table:
                    d2 = self.tableToList(table)
                    self.scrapedData[rsid]["Variations"] = d2[1:]
                    print(d2[1:])

        except urllib.error.HTTPError:
            print(url + " was not found on snpedia or contained no valid information")


        #########################
        # Frequency & Risk Allele
        try:
            print("####### dbSNP import for " + rsid)
            #url = "https://www.ncbi.nlm.nih.gov/pmc/?term= + rsid.lower()
            url = "https://www.ncbi.nlm.nih.gov/snp/" + rsid.lower()
           
            response = urllib.request.urlopen(url)
            html = response.read()
            bs = BeautifulSoup(html, "html.parser")
            freq = []
            risk = []

            for div in bs.find_all(class_='usa-width-one-half'):
                for childdiv in div.find_all('div'):
                    freq.append(childdiv.string)

                for childdiv in div.find_all('dd'):
                    if childdiv.string != None : 
                        risk.append(childdiv.string)
            
            
            risk = [s.strip() for s in risk]
            print("dbSNP Scraped Data ::")
            if (len(freq) > 1 and len(risk) > 0):
                print(freq[2])
                print(risk[1])

                self.scrapedData[rsid]["Frequency"] = freq[2]
                self.scrapedData[rsid]["Risk"] = risk[1]

        except urllib.error.HTTPError:
            print(url + " was not found or on dbSNP or contained no valid information")

        ##########################
        # Most recent study import
        try:
            print("####### Study import #######")
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
                print(study[1])
        except urllib.error.HTTPError:
            print(url + " was not found or on dbSNP term search or contained no valid information")
        except urllib.error.URLError:
            print(url + " was not found or on dbSNP term search or contained no valid information")
    
        #################
        # Classification
        try:
            print("####### Clinical Significance  #######")
            url = "https://www.ncbi.nlm.nih.gov/snp/" + rsid.lower() + "#clinical_significance"
            response = urllib.request.urlopen(url)
            html = response.read()
            bs = BeautifulSoup(html, "html.parser")
            ClinVar = []
            for div in bs.find_all(id="clinical_significance"):
                for childdiv in div.find_all('td'):
                    if childdiv.string != None : 
                        ClinVar.append(childdiv.string)
            if(len(ClinVar) > 0):
                print(ClinVar)
                self.scrapedData[rsid]["ClinVar"] = ClinVar
        except urllib.error.HTTPError:
            print(url + " was not found or on dbSNP or contained no valid information")

    
    def tableToList(self, table):
        rows = table.find_all("tr")
        data = []
        for row in rows:
            cols = row.find_all("td")
            cols = [ele.text.strip() for ele in cols]
            data.append([ele for ele in cols if ele])
        return data
        
    def createList(self):
        make = lambda rsname, description, classifications, freq, risk, study, variations: \
            {

            "Name": rsname,
            "Description": description,
            "ClinVar": str.join("  ", classifications),
            "Genotype": self.yourData[rsname.lower()] if rsname.lower() in self.yourData.keys() else "(n/a)", 
            "Frequency": freq,
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
            classifications = [formatCell(rsid, classification) for classification in curdict["ClinVar"]]
            self.rsidList.append(make(rsid, curdict["Description"], curdict["ClinVar"], curdict["Frequency"], curdict["Risk"], curdict["Studies"], variations))
        

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

parser = argparse.ArgumentParser()
parser.add_argument("-f", "--filepath", help="filepath for raw data to be used for import", required=False)
args = vars(parser.parse_args())


# SNPs can also be loaded directly like this
rsid = ["rs1815739", "Rs53576", "rs4680", "rs1800497", "rs429358", "rs9939609", "rs4988235", "rs6806903", "rs4244285"]

#load in snps_of_interest.txt
rsid += [line.rstrip() for line in open('SNPedia/data/snps_of_interest.txt')]


if args["filepath"]:
    personal = PersonalData(args["filepath"])
    snpsofinterest = [snp for snp in personal.snps if personal.hasGenotype(snp)]
    sp = GrabSNPs(crawllimit=60, snpsofinterest=snpsofinterest, target=100)
    rsid += sp.snps
    print("Extra 'SNPs of interest' to be analysed:")
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
