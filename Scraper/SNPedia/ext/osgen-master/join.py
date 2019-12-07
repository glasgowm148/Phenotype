import sys
sys.path.append('snpy')

from loadgenome import load23andme, loadgensnpy
from parsexml import loadxml, returnSNPs, get_trait_obj, get_xml_filelist
from parsexml import Trait
import sn
from xml.etree.ElementTree import ParseError

#This file primarily provides functions that intersect report xml data and genome data

#classes
class TraitReport():
    '''
    Not used
    Report on which genotypes for a list of RSIDs associated with a trait a
    genome has
    '''
    def __repr__(self):
        traitrep_st = "TraitReport Object: %s" % self.trait.name
        return traitrep_st

    def __init__(self, trait, rsid_report_dict):
        self.trait = trait #trait obj
        self.rsid_report_dict = rsid_report_dict #KEY: RSID, VALUE: GENOTYPE STR


#def join(genome):
    #'''
    #main
    #'''
    #snps_list = []
    #report_list = []  
    #ethnicity_genotype_tuple_list = []
    #my_genome_dict = {}

    ##iterate through files to get all snps
    #for f in get_xml_filelist():

        #try:
            ##get all the SNPs in a file
            #snps = returnSNPs(f)
            ##create rsid lists here to add to trait report
        #except ParseError:
            #pass
        #finally:
            #if len(snps) >= 1:
                #snps_list.extend(snps)
                #current_trait = get_trait_obj(f)
                #rsid_report_list = snps #just rsids now, should be rsids and associated eth/genotype/values
                #current_trait_report = TraitReport(current_trait, rsid_report_list)
                #report_list.append(current_trait_report)
                ##ethnicity_genotype_tuple_list = get_ethnicity_genotype_tuple_list(f)
    
    ##iterate through genome to find all relevant snps
    #gensnpy = loadgensnpy(genome)
    #for s in gensnpy:
        #if s.name in snps_list:
            #my_genome_dict[s.name]=s.genotype
    
    #print my_genome_dict
    #print report_list
                
def get_subset(genome):
    '''
    Returns subset of genome containing SNPs relevant xml files.
    '''
    genome_dict = {}
    snps_list = []
    
    #iterate through files to get all snps
    for f in get_xml_filelist():
        try:
            #get all the SNPs in a file
            snps = returnSNPs(f)
        except ParseError:
            pass
        finally:
            if len(snps) >= 1:
                snps_list.extend(snps)
    
    #iterate through genome to find all relevant snps
    gensnpy = loadgensnpy(genome)
    for s in gensnpy:
        if s.name in snps_list:
            genome_dict[s.name]=s.genotype
    
    #print genome_dict
    return genome_dict

    
def punnett(genome1,genome2):
    '''cross two genomes (make a baby/f1 generation)
    Not written
    '''
    pass


if  __name__ =='__main__':

    join("sample genomes/sample.23andme.txt")
    
    
