from Scrape_SNP_Page import Scrape_SNP_Page
import os
import multiprocessing.dummy
import csv

rsfile=open("RS_Numbers.txt",'r')
rsnumbers=rsfile.read().split(",")

def scap(x):
  print(x)
  return Scrape_SNP_Page(x)

p=multiprocessing.dummy.Pool(12)
rsdata2d=p.map(scap,rsnumbers[0:100:5])
rsdata=[]
for rsd in rsdata2d:
  for rs in rsd:
    rsdata.append(rs)
try:
  os.remove('test.csv')
except:
  pass
l=open('test.csv', 'w')
f=csv.writer(l)
f.writerows(rsdata)
l.close()
