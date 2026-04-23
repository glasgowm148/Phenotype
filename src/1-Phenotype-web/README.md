# Phenotype.dev

![Example of output](https://github.com/glasgowm148/Phenotype/blob/master/images/phenotype.png)
## Description
Phenotype is an open source local web application that helps users explore cached genome annotations without sending raw genome data to outside services. It uses Flask, SQLite, and plain JavaScript to import local genotype data, filter SNP annotations, refresh selected annotations, and export CSV data.

## Disclaimer
Raw Data coming from Genetic tests done by Direct To Consumer companies such as 23andMe and Ancestry.com were found to have a false positive rate of 40% for genes with clinical significance in a March 2018 study [*False-positive results released by direct-to-consumer genetic tests highlight the importance of clinical confirmation testing for appropriate patient care*](https://www.nature.com/articles/gim201838). For this reason, it's important to confirm any at risk clinical SNPs with your doctor who can provide genetic tests and send them to a clinical laboratory.

With genome analysis, sometimes sites will report on the negative strand - meaning that if a rare gene pops up which is pathogenic for some thing you've never heard of - this is likely the case. If you had such a gene it's likely 23andme would've notified you - This tool is more aimed at created custom phenotypes which combine several low-risk, benign or carrier genes - to demonstrate phenotypes where diseases could be manifesting as the cause of a combination of several genes - rather than one SNP.


## Use

Ensure you are using Python 3.10 or newer.

```bash
cd ../../
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Start the local web app with cached data:

```bash
cd src/1-Phenotype-web
../../.venv/bin/python -m flask --app SnpApi run --host 127.0.0.1 --port 5000
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

If port `5000` is already in use:

```bash
python -m flask --app SnpApi run --host 127.0.0.1 --port 5001
```

Open [http://127.0.0.1:5001](http://127.0.0.1:5001).

Refresh the scraped data from a raw genome file:

```bash
cd src/1-Phenotype-web
../../.venv/bin/python DataScraper.py -f data/example2.txt
```

Scraping can take several hours. The app asks MyVariant.info first, then falls back to SNPedia/NCBI HTML pages when API fields are missing. It exports periodically to `data/scrapedData.json` and `data/scrapedData.csv`. The web app overlays genotype data from `data/yourData.json` when that file exists.

The browser app can also import genome files, filter/search SNPs, sort by personal clinical significance, sort by recent classification changes, show color-coded ClinVar finding summaries, link selected SNPs to SNPedia/PubMed/source records, export CSV, delete local genotypes, refresh missing annotation data into the local SQLite cache, refresh missing finding dates from MyVariant/ClinVar, pause or cancel active refresh runs, resume incomplete runs, and retry failed SNP annotations through the API.

Useful development commands:

```bash
cd ../../
.venv/bin/python -m pytest
.venv/bin/python -m ruff check src/1-Phenotype-web/phenotype tests
.venv/bin/python -m ruff format src/1-Phenotype-web/phenotype tests
```


# Log
* Done
    * Enabled cross-platform support
    * snps_of_interest.txt can be loaded with SNPs to specifically query against your dataset
    * one_thousand_and_you.txt is ~1000 rsids related to health, drug metabolism, hormones, autoimmune, eds, asd/adhd, pots/mcas, etc..
    * dbSNP lookup functionality added
    * CSV Export working
    * Crawl dbSNP - added to import risk allele / freq
    * Crawl dbSNP - import clinical significance
    * Highlighting based on Risk Allele (Still some bugs)
    * Support for AncestryDNA
    * GeneticGenie + NutriHacker SNPs loaded
    * Export to PDF
* In Progress
  * Tidying up HTML/CSS/Tabular 
  * Filter by mutations only
* To Do
  * +/- strand orientation check
  * 23andme i -> rsid
  * User Login with upload
    * Custom reports / phenotypes
    * 'Save to ->' 
    * Email notifications when new studies are published with specified rsids
  * Other sources to utilise
    * Reload DB Data
    * Genomix source
    * SNPEdia_Scraper
    * genome_report

## Acknowledgements 
This Git is based on [OSGenome](osgenome/SNPedia at master · mentatpsi/OSGenome), [SNPApi](https://github.com/leaena/snp-api), and [Snappy](https://github.com/zhaofengli/snappy)
