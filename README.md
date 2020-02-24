# Phenotype

## Jupyter Notebook

There's two Jupyter notebooks which are pretty much functional.

### Scrape & Save

[Scrape & Save](https://github.com/glasgowm148/Phenotype/blob/master/DNA%20Pandas/Scrape_and_Save.ipynb) queries your rsids against ClinVar and returns assosciations, risk allele's, frequency - and stores it in a datatable. 

### Load & Analyse

[Load & Analyse](https://github.com/glasgowm148/Phenotype/blob/master/DNA%20Pandas/Load_and_Analyse%20.ipynb) matches your rsids against the ClinVar dataframe pulled from [Scrape & Save](https://github.com/glasgowm148/Phenotype/blob/master/DNA%20Pandas/Scrape_and_Save.ipynb). This can be exported to CSV or HTML.

### Limitations

Currently only tested with 23andme V4 & V5. 


### ToDo 

* Prettify HTML datatable using DataTables
* Flatten all DTC file formats into a consistent dataframe for manipulation
* Add more sources of data
  * SNPedia
  * ONIM
