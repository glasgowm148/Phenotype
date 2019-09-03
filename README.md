# OSGenome
This Git is based on [OSGenome - An Open Source Web Application for Genetic Data (SNPs) using 23AndMe and Data Crawling Technologies](https://github.com/mentatpsi/OSGenome)

## Description
OS Genome is an open source web application that allows users to gather the information they need to make sense of their own genome without needing to rely on outside services with unknown privacy policies. OS Genome's goal is to crawl various sources and give meaning to an individual's genome. It creates a Responsive Grid of the user's specific genome. This allows for everything from filtering to excel exporting. All of which using Flask, Kendo, and Python programming.

## Disclaimer
Raw Data coming from Genetic tests done by Direct To Consumer companies such as 23andMe and Ancestry.com were found to have a false positive rate of 40% for genes with clinical significance in a March 2018 study [*False-positive results released by direct-to-consumer genetic tests highlight the importance of clinical confirmation testing for appropriate patient care*](https://www.nature.com/articles/gim201838). For this reason, it's important to confirm any at risk clinical SNPs with your doctor who can provide genetic tests and send them to a clinical laboratory.


# Customisations

* Fixed py2/3 print bug preventing program from starting
* Switched os.cwd to pathlib for cross-platform support
* Created data/snps_of_interest.txt which can be loaded with SNPs you'd like to specifically query against your dataset
* Added support for dbSNP lookup
* Removed _GUI.py
* Enabled the commented out code and imported panda
* In Progress
  * dbSNP crawler to get risk allele, publications, frequency and crosscheck result from snpedia
  * 

## Installation:

In order to set up the requirements. Make sure you have [python pip](https://packaging.python.org/installing/). The necessary dependencies can therein be added by pip install -r requirements.txt. This will install everything you need to use the script. It is written using Python 3. So make sure to use that when running the script and make sure environmental variables of PATH were set during installation of Python for Windows.

Step 0:
```
pip install -r requirements.txt
```
This sets up the necessary dependencies (such as Flask, used to create a Python based web server and BeautifulSoup used to crawl through SNPedia).

Note: Linux may be pip3.6 and OSX Should be be pip3 


Step 1:
```
python3 SNPedia/DataCrawler.py -f [Absolute path of your downloaded raw 23andMe data]
```
This sets up the datacrawler using your data as a means to highlight what SNPs are relevant to you. 



Step 2:
```
python3 SNPedia/SnpApi.py
```
This sets us the Flask server


## Access the Local Server
Access http://127.0.0.1:5000 (the ip address also known as localhost, it's all hosted on your local machine) to look at your Genome
