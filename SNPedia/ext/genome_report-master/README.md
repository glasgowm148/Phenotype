Make your genome report
===

Only tested with 23andme file

# Install

```
git clone https://github.com/Endika/genome_report
sudo apt-get install wkhtmltopdf
pip install -r requirements.txt
```

# How to run

```
python report.py -g my_genome_file.txt -f html

python report.py -g demo/male01.txt
```

# TODO
- Desing report
- Add more SNP in report
- Multi language
