import sys


from bs4 import BeautifulSoup
from random import shuffle


from pathlib import Path

import pandas as pd 
import numpy as np 


import urllib.request
import pprint
import json
import argparse
import os
import random
# rs4534 rs1815739

# filter common</b> & normal</b>

rsid = "rs4680"

from SNPGen import GrabSNPs

 ######################
        # Classification
        try:
            print("####### Clinical Significance  #######")
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
                self.scrapedData[rsid]["ClinVar"] = ClinVar
        except urllib.error.HTTPError:
            print(url + " was not found or on dbSNP or contained no valid information")

    
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


    