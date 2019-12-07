from Scrape_SNP_Page import Scrape_SNP_Page
from Get_Genes import Get_Genes
import os
#import multiprocessing.dummy
#import time
import csv
#liz=["rs662799","rs9939609","rs1805007","rs1800497"]
#Get_Genes()

#p = multiprocessing.dummy.Pool(4)
#print(list(p.map(Scrape_SNP_Page, liz)))
x=Scrape_SNP_Page("rs28940269")
try:
  os.remove('test.csv')
except:
  pass
l=open('test.csv', 'w')
f=csv.writer(l)
f.writerows(x)


l.close()

#files=open("rsdata.txt","w+")
#files.write(x)
#files.close()
