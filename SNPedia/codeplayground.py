import sys


from bs4 import BeautifulSoup
from random import shuffle

from GenomeImporter import PersonalData

from pathlib import Path

import pandas as pd 
import numpy as np 


import urllib.request
import pprint
import json
import argparse
import os
import random

#  rs1815739

from SNPGen import GrabSNPs

try:
            print("####### dbSNP import #######")
            url = "https://www.ncbi.nlm.nih.gov/snp/rs1815739" 

            response = urllib.request.urlopen(url)
            html = response.read()
            bs = BeautifulSoup(html, "html.parser")
            risk = []
            for div in bs.find_all(class_='usa-width-one-half'):
                    for childdiv in div.find_all('dd'):
                        if childdiv.string != None : 
                            print(childdiv.string)
                            risk.append(childdiv.string)
            print("risk-print")
            risk = [s.strip() for s in risk]
            print(risk)

            
except urllib.error.HTTPError:
    print(url + " was not found or on dbSNP or contained no valid information")


    