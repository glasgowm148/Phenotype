import xml.etree.ElementTree as ET
import os, glob

#This file primarily deals with functions that interpret the data in the xml files containing trait information
        
##Classes 
class Trait():
    '''
    Object representing trait information from an xml file
    Not used
    '''
    def __repr__(self):
        traitstring = "Trait Object: %s" % self.name
        return traitstring

    def __init__(self, name, wlink, supertrait, subtrait, description):
        self.name = name
        self.wlink = wlink
        self.supertrait = supertrait
        self.subtrait = subtrait
        self.description = description

# Newer OO Functions
def get_trait_obj(xmlfile):
    root = loadxml(xmlfile)
    '''
    Gets information about the trait file and returns Trait object
    Not used
    '''
    name = gettext(root, "name")
    wlink = gettext(root,"wikipedialink")
    supertrait = gettext(root,"supertrait")
    subtrait = gettext(root,"subtrait")
    
    try:
        description = root.getiterator("description")[0]
    except:
        description = None
    
    trait = Trait(name = name, wlink = wlink, supertrait = supertrait, subtrait = subtrait, description = description)
    return trait


# Older Non OO Functions
def get_xml_filelist():
    filelist = []
    #os.chdir("xml files")
    for f in glob.glob("xml files/*.xml"):
        filelist.append(f)
    return filelist

def loadxml(xmlfile):
    tree = ET.parse(xmlfile)
    root = tree.getroot()
    if root.tag != 'data':
        print 'The root tag of the XML file must be an <data> tag.'
        return
    else:
        return root

def returnSNPs(xmlfile):
    '''
    Returns list of rsids of all the SNPs reported on in a file.
    '''
    root = loadxml(xmlfile)
    snps = []
    for o in root.findall("output"):
        for s in o.findall("SNP"):
            snps.append(s.find("rsid").text)
    #print snps
    return snps
        
def get_trait_dict(root):
    '''
    Returns a dict of info about a trait tag. 
    Not used
    Supplanted by Trait class and get_trait_obj
    '''
    
    trait = root.getiterator("trait")[0] #fix this to only get direct children?

    traitdict = {}
    for child in trait:
        traitdict[child.tag] = child.text.strip()
    
    for key, value in traitdict.items():
        print "%s: %s\n" % (key,value)
        
    return traitdict
     
def gettext(root, text):
    '''
    returns variable corresponding to text within a tag
    '''
    try:
        return root.getiterator(text)[0].text.strip()
    except IndexError:
        return None
        
def getreports(root):
    '''
    gets report from each output tag
    Not used
    '''
    report_list = []
    for o in root.findall("output"):
        output_type = o.get("type")
        if output_type == "phenotype":
            report_list.append(reportify_phenotype(o))
        else:
            print "The output type \'%s\' is not currently supported" % output_type
    #print report_list
    return report_list

def getgenotypes(ethnicity):
    '''
    return dict of genotypes and meanings
    Not used
    '''
    genotype_dict = {}
    genotypes = ethnicity.findall("genotype")
    for g in genotypes:
        genotype = g.get('value')
        meanings = {}
        for child in g:
            meanings[child.tag] = child.text.strip() 
        genotype_dict[genotype] = meanings
    return genotype_dict

#create reports - fix to return report objects

def reportify_phenotype(o_tag):
    '''
    Returns a list of tuples in the format (ethnicity_string, genotype_dict)
    Not currently in use
    '''
    
    try:
        gettrait(o_tag) #prints trait information specfic to report
    except:
        pass
        
    report = []
        
    snps = o_tag.findall('SNP')
    for s in snps:
        #each snp should have exactly one rsid
        rsid = "SNP RSID: %s" % s.find("rsid").text
        print rsid
        
        ethnicity = s.findall("ethnicity")
        for e in ethnicity:
            genotype_dict = getgenotypes(e)
            eth_name = e.attrib["value"]
            report.append((eth_name,genotype_dict))
    
    #print report
    return report


#empty methods- todo
def reportify_probability(o_tag):
    '''
    Parses an output tag where a probability
    of the phenotype or disease described in the <outcome> tag.
    Sample XML file is in /xmlschemas/
    Not written
    '''
    pass


if  __name__ =='__main__':

    print get_trait_obj("xml files/refractive_errors.xml")

    
