import requests
from bs4 import BeautifulSoup
import os


def findGenesOnPage(sop):
  mw=sop.findAll("div",{"class":"mw-category-group"})

  #finds all unordered lists
  listoflists=[x.findAll("ul") for x in mw]

  #adds all ul elements to mn
  sublists=[]
  for lists in listoflists:
    for lis in lists:
      sublists.append(lis)
  #the page is a list of lists so we gotta do it twice
  listtexts=[]
  for lists in sublists:
    listele=lists.findAll("li")
    for text in listele:
      listtexts.append(text)
  return [x.text for x in listtexts]

#finds and returns next page url if present
def nextpage(sop):
  for x in sop.findAll("a"):
    if(x.text=="next page"):
      return "https://www.snpedia.com"+x['href']
  return None

#gets all gene names
def Get_Genes():
  url = 'https://www.snpedia.com/index.php?title=Category:Is_a_gene'
  try:
    os.remove("GeneList.txt")
  except:
    pass
  files=open("GeneList.txt","w+")

  #snpedia is built like a linked list so this really is the only way
  while(url):
    response = requests.get(url)
    while(response.status_code!=200):
      response = requests.get(url)
    html = str(response.content)
    soup=BeautifulSoup(html)
    page=findGenesOnPage(soup)

    #id gather clean up commas later than risk entering a non gene value
    files.write(",")
    files.write(",".join(page))
    files.write(",")
    url=nextpage(soup)
  files.close()
  print("Genes Saved")
