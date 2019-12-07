#!/usr/bin/python

from bs4 import BeautifulSoup
import urllib2
import json
import re
import os.path


def parse_links():
    '''
    returns list of genome report urls to visit
    '''
    genome_reports = urllib2.urlopen("https://my.pgp-hms.org/public_genetic_data?data_type=Complete+Genomics&commit=Search")
    soup = BeautifulSoup(genome_reports)
    texts = soup.find('div', {"class": "profile-data"})
    rows = texts.findAll('a')
    genome_urls = []

    for row in rows:
        if row.get('href').startswith('http://evidence.pgp-hms.org/genomes?display_genome_id='):
            genome_urls.append(row.get('href'))
            
    return genome_urls

def get_variants(url):
    '''
    visits a genome report page and stores all variants
    found in a dictionary of its name and url.
    '''
    variant_dict = {}
    variant_report = urllib2.urlopen(url)
    soup = BeautifulSoup(variant_report)
    texts = soup.find('table', {"class": 'report_table variant_table datatables_please'})
    rows = texts.findAll('a')
    for row in rows:
        variant_dict[row.text] = 'http://evidence.pgp-hms.org/' + row.text
    return variant_dict

def parse_all_links(genome_urls):
    '''
    returns dict stored with every url for each variant
    in a person's genome report.
    '''
    variants_mList = []
    for url in genome_urls:
        try:
            variant_dict = get_variants(url)
        except AttributeError:
            print 'All links parsed'
            return variants_mList
        variants_mList.append(variant_dict)
    return variants_mList


def map_score(score):
    '''
    Map GET-Evidence text score display to numeric or None

    The score displayed by GET-Evidence is confusing. No score (an empty
    string) actually means the author gave it a rank of "no stars" (or "0"),
    while a hyphen ("-") means it wasn't scored at all (i.e. "None").
    '''
    if score == '':
        return '0'
    elif score == '-':
        return None
    else:
        return score


def parse_data(variant_name, variant_url):
    '''
    Parses data from a variant page (PMID, writeup, build 37 coordinates, the
    7 scores, dpSNP_ID), returns data as a dict
    '''
    variant_report = urllib2.urlopen(variant_url)
    variant_page = BeautifulSoup(variant_report)

    # get gene symbol
    if '-' in variant_name:
        gene_symbol = variant_name.split('-')[0]
    else:
        gene_symbol = None

    # get PMIDs and dbSNP_IDs
    PMIDs = []
    dbSNP_IDs = []
    for link in variant_page.findAll('a', attrs={'href': re.compile("^http://")}):
        index = link.text.find("PMID:")
        if index >= 0:
            PMIDs.append(link.text[index + 6: index + 15])
        linkhref = link.get('href')
        if re.match(
                r"http://www\.ncbi\.nlm\.nih\.gov/projects/SNP/snp_ref" +
                r"\.cgi\?searchType=adhoc_search&type=rs&rs=", linkhref):
            dbSNP_IDs.append(link.text)

    # number of PMIDs in a variants page
    PMID_count = len(PMIDs)

    # get score values
    soup = variant_page.find('table', {"class": "quality_table"})
    rows = soup.findAll('td')
    page_text = []
    for row in rows:
        page_text.append(row.text)

    comp_index = page_text.index("Computational")
    func_index = page_text.index("Functional")
    case_index = page_text.index("Case/Control")
    fami_index = page_text.index("Familial")
    seve_index = page_text.index("Severity")
    trea_index = page_text.index("Treatability")
    pene_index = page_text.index("Penetrance")

    scores = {"Computational": page_text[comp_index+2],
              "Functional": page_text[func_index+2],
              "Case/Control": page_text[case_index+2],
              "Familial": page_text[fami_index+2],
              "Severity": page_text[seve_index+2],
              "Treatability": page_text[trea_index+2],
              "Penetrance": page_text[pene_index+2]}
    scores = {k: map_score(scores[k]) for k in scores.keys()}

    # get build 37 coordinates
    build37 = []
    re_b37_evs = r'^([ACGT]+) @ (chr[1-9XYM][0-9]?):([0-9]+): '
    rows = variant_page.find('div', attrs={'id': 'allele_frequency'})
    b37_var_allele, b37_chrom, b37_pos = None, None, None
    for row in rows.findAll('li'):
        if " in EVS" in row.text:
            (b37_var_allele, b37_chrom, b37_pos) = re.match(
                re_b37_evs, row.text).groups()
            break


    # fill json with data
    report_JSON = {"Build37 coordinates:": build37, "Scores": scores,
                   "PMID Count": PMID_count, "URL": variant_url,
                   "Variant Name": variant_name}
    if PMIDs:
        report_JSON['PMID List'] = PMIDs
    if dbSNP_IDs:
        report_JSON['dbSNP IDs'] = dbSNP_IDs
    if gene_symbol:
        report_JSON['Gene Symbol'] = gene_symbol
    if b37_var_allele and b37_chrom and b37_pos:
        report_JSON.update({
            'Build 37 Variant Allele': b37_var_allele,
            'Build 37 Chromosome': b37_chrom,
            'Build 37 Position': b37_pos,
        })

    return report_JSON


def parse_and_write_data(variants_mList):
    '''
    Parses data from a variants page (PMID, writeup, build 37 coordinates,
    the 7 scores, dpSNP_ID), creates json files for each variant inside
    the master array
    '''
    # loop runs for each dictionary (variants in each report) inside the array
    for variants_dict in variants_mList:

        # loop runs for each variant inside a dictionary
        for variant_name, variant_url in variants_dict.iteritems():
            if not os.path.isdir('variants'):
                os.mkdir('variants')

            # Skip variant if it's already been done.
            json_filepath = "variants/" + variant_name + "_variantReport.json"
            if os.path.exists(json_filepath):
                print json_filepath + " already exists\n"
                continue

            variant_data = parse_data(variant_name, variant_url)
            variant_json_file = open(json_filepath, 'w')
            json.dump(variant_data, variant_json_file, indent=4)
            print json_filepath + " was created\n"


if __name__ == '__main__':
    genome_reports = parse_links()
    variants_mList = parse_all_links(genome_reports)
    parse_and_write_data(variants_mList)
