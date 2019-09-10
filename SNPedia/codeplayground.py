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

rsid = "rs9378252"

from SNPGen import GrabSNPs


 # ncbi.nlm.nih.gov
try:
    url = "https://www.ncbi.nlm.nih.gov/snp/" + rsid.lower() + "#clinical_significance"
    response = urllib.request.urlopen(url)
    html = response.read()
    bs = BeautifulSoup(html, "html.parser")
  
    ncbi = bs.find(class_="summary-box usa-grid-full")
    dbSNP = []
    if ncbi:
        rows = ncbi.find_all("dl")
        
        for row in rows:
            cols = row.find_all("dd")
            cols = [ele.text.strip() for ele in cols]
            dbSNP.append(cols)
    print(dbSNP[1][2][0])
    print(dbSNP[1][1].split(' ')[0])

except urllib.error.HTTPError:
    print(url + " was not found or on dbSNP or contained no valid information")