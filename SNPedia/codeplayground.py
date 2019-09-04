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

#  rs1815739
rsid = "rs55901263"

from SNPGen import GrabSNPs

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
            print(study[1])
except urllib.error.HTTPError:
    print(url + " was not found or on dbSNP or contained no valid information")


    