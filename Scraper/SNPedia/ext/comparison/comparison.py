import pandas as pd
import numpy as np

def load_snps(filename): 
    d = pd.read_csv( filename, index_col='rsid',delim_whitespace=True,comment="#")
    d = d[d["genotype"]!='--']
    return d
    
d1 = load_snps('SNPedia/data/example.txt')
d2 = load_snps('SNPedia/data/example.txt')
    
print "2013 cnt {}".format(d1.shape[0])
print "2016 cnt {}".format(d2.shape[0])

crossection = d1.merge(d2, left_index=True, right_index=True, how='inner', suffixes=["_2013","_2016"])

print "crossection cnt {}".format(crossection.shape[0])

differences = crossection[ crossection["genotype_2013"] != crossection["genotype_2016"] ]


print "Differences: {}".format(differences.shape[0])

print "2013: {}%\n2016: {}% ".format(
    np.round( differences.shape[0] * 100.0 / d1.shape[0], decimals=3 ),
    np.round( differences.shape[0] * 100.0 / d2.shape[0], decimals=3 ) )