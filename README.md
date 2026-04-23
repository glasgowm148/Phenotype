# Phenotype




<!--[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]-->
[![MIT License][license-shield]][license-url]
[![LinkedIn][linkedin-shield]][linkedin-url]



<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/glasgowm148/Phenotype">
    <img src="https://github.com/glasgowm148/Phenotype/blob/master/docs/img/logo.png" alt="Logo">
  </a>

  <h3 align="center">Phenotype</h3>

  <p align="center">
    Genomic Analysis
    <br />
    <a href="https://github.com/glasgowm148/Phenotype/tree/main/Phenotype/data/docs"><strong>Explore the docs »</strong></a>
    <br />
    <br />
    <a href="https://github.com/glasgowm148/Phenotype/data/demo">View Demo</a>
    ·
    <a href="https://github.com/glasgowm148/Phenotype/issues">Report Bug</a>
    ·
    <a href="https://github.com/glasgowm148/Phenotype/issues">Request Feature</a>
  </p>
</p>



<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#contributing">Contributing</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

![Phenotype Screen Shot](https://github.com/glasgowm148/Phenotype/blob/master/docs/img/phenotype.png)

Phenotype is an open source local web application that helps users explore cached genome annotations without sending raw genome data to outside services. It uses Flask, SQLite, and plain JavaScript to import local genotype data, filter SNP annotations, refresh selected annotations, and export CSV data.

## Quick Start

Phenotype has two main workflows:

* View existing cached SNP data in the Flask web app.
* Refresh the cached SNP data from a raw 23andMe or AncestryDNA-style export.

### Install

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

### Run the Web App

```bash
cd src/1-Phenotype-web
../../.venv/bin/python -m flask --app SnpApi run --host 127.0.0.1 --port 5000
```

Open [http://127.0.0.1:5000](http://127.0.0.1:5000).

If port `5000` is already in use:

```bash
python -m flask --app SnpApi run --host 127.0.0.1 --port 5001
```

Then open [http://127.0.0.1:5001](http://127.0.0.1:5001).

The app reads cached legacy data from `src/1-Phenotype-web/data/scrapedData.json`, imports it into local SQLite at `src/1-Phenotype-web/data/phenotype.sqlite`, and overlays genotypes from `src/1-Phenotype-web/data/yourData.json` when present.

### Web App Features

* Search by rsid, gene, or description.
* Filter to SNPs with imported genotypes.
* Filter to rows where the imported genotype contains the listed risk allele.
* Sort and filter by personal clinical significance.
* Sort by recent classification changes after annotations are refreshed.
* Cache annotations in local SQLite so rsids are not re-scraped unless missing or explicitly refreshed.
* Link directly to SNPedia, PubMed searches, and source records from the SNP detail panel.
* Show color-coded ClinVar finding summaries with dates, severity, and source accessions.
* Import a raw 23andMe/Ancestry-style genome file from the browser.
* Refresh annotations for a small batch from the browser and watch progress.
* Pause or cancel active scrape runs.
* Resume incomplete scrape runs or retry failed SNP annotations.
* Export the current local SQLite data to CSV.
* Export build 37 variants or rsids for Ensembl VEP, then import VEP consequence output.
* Filter locally cached VEP consequences by high/moderate impact, missense, splice, and stop-gained calls.
* Delete locally imported genotypes before sharing the workspace.

### Whole-Chip VEP Consequence Scan

After importing a 23andMe build 37 file, use **Build 37 variants** and **x;y** in the app to focus on heterozygous rows. Use **Export VEP x;y** for coordinate/allele VEP input, or **Export VEP rsids** for an rsid list.

With Docker Desktop running, install the GRCh37 VEP cache and FASTA:

```bash
mkdir -p "$HOME/vep_data"
docker run -t -i -v "$HOME/vep_data:/data" ensemblorg/ensembl-vep INSTALL.pl -a cf -s homo_sapiens -y GRCh37
```

Run VEP on the exported heterozygous build 37 variants:

```bash
docker run --rm \
  -v "$HOME/vep_data:/data" \
  -v "$PWD/src/1-Phenotype-web/data/exports:/work" \
  ensemblorg/ensembl-vep \
  vep --cache --offline --assembly GRCh37 --format ensembl \
  --input_file /work/phenotype_build37_heterozygous_vep_input.tsv \
  --output_file /work/phenotype_vep_output.txt \
  --force_overwrite --tab --symbol --hgvs --canonical --variant_class --no_stats
```

Import the result from the browser with **Import VEP**, or from the command line:

```bash
.venv/bin/phenotype-vep-import src/1-Phenotype-web/data/exports/phenotype_vep_output.txt
```

The raw 23andMe file contains observed alleles, not a confirmed reference allele. Treat VEP consequence filters as functional annotation evidence; clinical interpretation still needs ClinVar/SNPedia context and confirmation.

### API

* `GET /api/snps`
* `GET /api/snps/<rsid>`
* `GET /api/variants`
* `POST /api/import`
* `POST /api/scrape`
* `POST /api/scrape/resume`
* `POST /api/vep/import`
* `GET /api/scrape-runs/latest`
* `GET /api/scrape-runs/<run_id>`
* `POST /api/scrape-runs/<run_id>/pause`
* `POST /api/scrape-runs/<run_id>/cancel`
* `POST /api/scrape-runs/<run_id>/retry-failed`
* `GET /api/export.csv`
* `GET /api/export-vep.tsv`
* `GET /api/export-vep-rsids.txt`
* `DELETE /api/genotypes`

### Refresh the Data

To import a raw genome file and refresh the scraped data:

```bash
source .venv/bin/activate
cd src/1-Phenotype-web
python DataScraper.py -f data/example2.txt
```

Scraping can take a long time because it queries external annotation sources. The app now asks MyVariant.info first, then falls back to SNPedia/NCBI HTML pages when API fields are missing. Progress is exported periodically to `data/scrapedData.json` and `data/scrapedData.csv`.

### Development

```bash
.venv/bin/python -m pytest
.venv/bin/python -m ruff check src/1-Phenotype-web/phenotype tests
.venv/bin/python -m ruff format src/1-Phenotype-web/phenotype tests
```

A `Makefile` is also included for the same workflows when `make` is available on your machine.


## Jupyter-playground

Various notebooks used to explore SNP data. The two main files retrieve batches of rsids using [MyVariant.info](https://myvariant.info/).

Currently exports a plain HTML table, NaN and 23andme i-rsid's dropped and sorted by adviser rating.

![](https://github.com/glasgowm148/Phenotype/blob/master/docs/img/html_table.png)


* [Scrape & Save](/src/2-Jupyter-playground/Scrape_and_Save.ipynb) queries your rsids against ClinVar and returns assosciations, risk allele's, frequency - and stores it in a datatable. 
* [Load & Analyse](/src/2-Jupyter-playground/Load_and_Analyse.ipynb) matches your rsids against the ClinVar dataframe pulled from [Scrape & Save](/src/2-Jupyter-playground/Scrape_and_Save.ipynb). This can be exported to CSV or HTML.

### Limitations

Currently only tested with 23andme V4 & V5. 

This project is for personal exploration only. Direct-to-consumer genetic data can contain false positives and should not be treated as clinical advice without confirmatory testing.


### ToDo 

* Beautify HTML datatable using DataTables
* Flatten all DTC file formats into a consistent dataframe for manipulation
* Add more sources of data
  * SNPedia
  * ONIM
* Data-validaiton
  * strand orientation
  * risk allelle debugging

<!-- GETTING STARTED 
## Getting Started
### Installation




<!-- USAGE EXAMPLES 
## Overview





<!-- ROADMAP 
## Roadmap

See the [open issues](https://github.com/glasgowm148/Phenotype/issues) for a list of proposed features (and known issues).



<!-- CONTRIBUTING -->
## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request



<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE` for more information.


<!-- CONTACT -->
## Contact

Mark Glasgow - markglasgow@gmail.com


<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements
* [OSGenome](https://github.com/mentatpsi/OSGenome)
* [SNPApi](https://github.com/leaena/snp-api),  
* [Snappy](https://github.com/zhaofengli/snappy)


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/glasgowm148/Phenotype.svg?style=for-the-badge
[contributors-url]: https://github.com/glasgowm148/Phenotype/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/glasgowm148/Phenotype.svg?style=for-the-badge
[forks-url]: https://github.com/glasgowm148/Phenotype/network/members
[stars-shield]: https://img.shields.io/github/stars/glasgowm148/Phenotype.svg?style=for-the-badge
[stars-url]: https://github.com/glasgowm148/Phenotype/stargazers
[issues-shield]: https://img.shields.io/github/issues/othneildrew/Best-README-Template.svg?style=for-the-badge
[issues-url]: https://github.com/glasgowm148/Phenotype/issues
[license-shield]: https://img.shields.io/github/license/othneildrew/Best-README-Template.svg?style=for-the-badge
[license-url]: https://github.com/glasgowm148/Phenotype/blob/master/LICENSE.txt
[linkedin-shield]: https://img.shields.io/badge/-LinkedIn-black.svg?style=for-the-badge&logo=linkedin&colorB=555
[linkedin-url]: https://www.linkedin.com/in/glasgowmark/
