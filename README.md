# Phenotype.dev

![Example of output](https://github.com/glasgowm148/Phenotype/blob/master/images/phenotype.png)
## Description
Phenotype is an open source web application that allows users to gather the information they need to make sense of their own genome without needing to rely on outside services with unknown privacy policies. OS Genome's goal is to crawl various sources and give meaning to an individual's genome. It creates a Responsive Grid of the user's specific genome. This allows for everything from filtering to excel exporting. All of which using Flask, Kendo, and Python programming.

## Disclaimer
Raw Data coming from Genetic tests done by Direct To Consumer companies such as 23andMe and Ancestry.com were found to have a false positive rate of 40% for genes with clinical significance in a March 2018 study [*False-positive results released by direct-to-consumer genetic tests highlight the importance of clinical confirmation testing for appropriate patient care*](https://www.nature.com/articles/gim201838). For this reason, it's important to confirm any at risk clinical SNPs with your doctor who can provide genetic tests and send them to a clinical laboratory.

With genome analysis, sometimes sites will report on the negative strand - meaning that if a rare gene pops up which is pathogenic for some thing you've never heard of - this is likely the case. If you had such a gene it's likely 23andme would've notified you - This tool is more aimed at created custom phenotypes which combine several low-risk, benign or carrier genes - to demonstrate phenotypes where diseases could be manifesting as the cause of a combination of several genes - rather than one SNP.


# Timeline
* Done
    * Enabled cross-platform support
    * snps_of_interest.txt can be loaded with SNPs to specifically query against your dataset
    * one_thousand_and_you.txt is ~1000 rsids related to health, drug metabolism, hormones, autoimmune, eds, asd/adhd, pots/mcas, etc..
    * dbSNP lookup functionality added
    * CSV Export working
    * Crawl dbSNP - added to import risk allele / freq
    * Crawl Clinivar - import clinical significance
    * Highlighting based on Risk Allele (Still some bugs)
* In Progress
  * Tidying up HTML/CSS/Tabular 
  * Filter by mutations only
* To Do
  * ONIM Support
  * User Login with upload
    * Custom reports
    * 'Save to ->' 
    * Email notifications when new studies are published with the users genotype
  * Other sources to utilise
    * Reload DB Data
    * Genomix source
    * SNPEdia_Scraper
    * genome_report

## Installation:


0.
```
pip install -r requirements.txt
```
1. 
```
python3 SNPedia/DataScraper.py -f [Absolute path of your downloaded raw DNA data]
```

2.
```
python3 SNPedia/SnpApi.py
```
```
## Access the Local Server
http://127.0.0.1:5000
```

This Git is based on OSGenome - An Open Source Web Application for Genetic Data (SNPs) using 23AndMe and Data Crawling Technologies

