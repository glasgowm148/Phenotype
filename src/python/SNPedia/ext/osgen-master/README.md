osgen
=====

Open Source GENome Tool Component:
Disease XML Files + python parsing code
opensourcegenome.org

=====
Verion 0.0.1

This version is a proof-of-concept that delivers very limited results for 5 SNPs

How to use:

1. Clone git repo (into terminal, type 'git clone https://github.com/mvolz/osgen.git')

2. CD into folder 'osgen'

3. Into the terminal type 'python main.py -i input_file -o output_file' where input_file is the path to your downloaded raw genome file.

4. Open the resulting .pdf to read your results

=====

Information about each disease and associated SNPs is stored in an XML file. This allows the disease and SNP information to be under source control and is platform agnostic. Files can be changed or added to the repository by contributers, and others can build platforms to analyze their genome using the XML files. For instance, for a web app, the XML files could be loaded into a database, or interpreted by javascript in the browser. They could also be interpreted by a local script. 

Python code is included to parse the XML files locally. 

Includes snpy library from: https://github.com/superbobry/snpy

====
