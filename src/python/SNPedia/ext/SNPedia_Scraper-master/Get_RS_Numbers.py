import requests
from bs4 import BeautifulSoup
import multiprocessing.dummy
import os




#gets gene page and retry request if not 200 status code
def getGene(gene):
  url="https://www.snpedia.com/index.php/"+gene
  response = requests.get(url)
  tries=1
  while(response.status_code!=200):
    tries=tries+1
    print(gene+" try "+tries)
    response = requests.get(url)
  html = str(response.content)
  soup=BeautifulSoup(html)
  print(gene)
  return [x.text for x in soup.findAll("td",{"class":"smwtype_wpg"})]


#this does the stuff
def Get_All_RS():
  #I did a test and more threads does make it faster...i dont know when i am getting i/o bottlenecking though
  p = multiprocessing.dummy.Pool(2000)
  #file reading
  f=open("Gene_List.txt","r")
  mgenes=f.read().split(",")
  #cleans gene list in case of comma errors
  genes=[]
  for t in mgenes:
    if(t!=""):
      genes.append(t)
  rsTwoDimen=p.map(getGene, genes)
  #rsTwoDemin returns the list of rs numbers by gene and this flattens that array
  rsNumbers=[]
  for rsList in rsTwoDimen:
    for rs in rsList:
      rsNumbers.append(rs)
  #cleans rs number list of anything that doesnt start with rs or i followed by numbers
  cleanRS=[]
  for rs in rsnumbers:
    if(len(rs)>2):
      if ((rs[:2]=='rs' and rs[2:].isdigit()) or (rs[:1]=='i' and rs[1:].isdigit())):
        cleanRS.append(rs)
  #file writing
  os.remove("RS_Numbers.txt")
  k=open("RS_Numbers.txt","w+")
  len(rsnumbers)
  k.write(",".join(rsnumbers))
  k.close()
