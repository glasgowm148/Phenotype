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

rsid = "rs4534"

from SNPGen import GrabSNPs

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
            print(ClinVar)
except urllib.error.HTTPError:
    print(url + " was not found or on dbSNP or contained no valid information")


    