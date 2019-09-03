#!/usr/bin/python 

from wikitools import wiki, category
import os
import re
import urllib2
import urllib
from bs4 import BeautifulSoup
from bs4 import Comment
import sys
import csv
import sqlite3
from lxml import etree

def load_accepted_rsnumbers(filename):
    return rs_filter(rs.rstrip().lower() for rs in open(filename).read().split('\n'))

def get_snpedia_snp_names():

    site = wiki.Wiki('https://bots.snpedia.com/index.php/')
    snps = category.Category(site, 'Is_a_snp')
    snpedia = set() 

    for article in snps.getAllMembersGen(namespaces=[0]):
        snpedia.add(article.title.lower())

    return snpedia

def download_and_add_snpedia_data(accepted_rsnumbers):
    print 'downloading snpedia pages and generating text html ...'

    conn = sqlite3.connect('snpedia.db') 
    conn.text_factory = str
    c = conn.cursor()
    c.execute('DROP TABLE IF EXISTS main')
    c.execute('CREATE TABLE main (rs text PRIMARY KEY, html text, strand_info text)')


    # get the names of all snps in snpedia
    snpedia = get_snpedia_snp_names()
    print("here1")

    # filter out snp names that aren't rs numbers
    rsnumbers = rs_filter(snpedia)
    
    # filter out rsnumbers we don't want 
    if accepted_rsnumbers:
        rsnumbers = rsnumbers & accepted_rsnumbers

    for idx, rs in enumerate(rsnumbers):
        print 'processing snp {0} out of {1} ...'.format(idx + 1, len(rsnumbers))

        while True:
            print("here1")
            try:
                print("here2")

                query = 'https://bots.snpedia.com/index.php/'+rs
                print("here3")

                response = urllib.request.urlopen(query)
                html = response.read()
            except urllib2.URLError:
                print "error downloading page, trying again ..."
                continue
            break

        c.execute('INSERT INTO main VALUES (?, ?, ?)', (rs, extract_snpedia_text(html), extract_snpedia_strand_info(html)))

    conn.commit()
    conn.close()


def rs_filter(snp_names):
    return set(snp for snp in snp_names if re.match(r'rs\d+', snp))

def extract_snpedia_strand_info(page):
    # the strand info is contained between these unique tags
    regex = r'title="Orientation">Orientation</a></td><td>(plus|minus)</td></tr>'
    m = re.findall(regex, page, re.MULTILINE)

    if(m):
        # plus or minus
        return m[0]
    else:
        return "undefined"

def extract_snpedia_text(html_page):

    soup = BeautifulSoup(html_page)

    # remove comments
    for comment in soup.findAll(text=lambda text:isinstance(text, Comment)):
        comment.extract()

    # remove unwanted tags 
    for t in soup.body.find_all(recursive=False):
        if t in soup.body.find_all('table') or \
                t in soup.body.find_all('div'):
            t.extract()

    # remove dead image links
    for t in soup.body.find_all('a'):
        if t.get('class') and 'image' in t.get('class'):
            t.extract()

    return soup.body.prettify(formatter='html').encode('utf-8')

# def generate_snpedia_charts(rsnumbers):
#     print 'generating snpedia charts ...'
#
#     for idx, rs in enumerate(rsnumbers):
#         print 'processing snp {0} out of {1} ...'.format(idx + 1, len(rsnumbers))
#
#         page = open('snp_db/'+rs+'/snpedia_page.html').read()
#
#
#         m = re.search(url_regex, page)
#
#         if m:
#             soup = BeautifulSoup(m.group(1))
#             urllib.urlretrieve(soup.string, 'snp_db/'+rs+'/snpedia_chart.png')

# def generate_html_for_snpedia_charts(rsnumbers):
#     print 'generating html for snpedia charts ...'
#
#     for idx, rs in enumerate(rsnumbers):
#         print 'processing snp {0} out of {1} ...'.format(idx + 1, len(rsnumbers))
#
#         page = open('snp_db/'+rs+'/snpedia_page.html').read()
#
#         soup = BeautifulSoup(page)
#
#         url_regex = r"'(http://chart\.apis\.google\.com/chart.*?)'"
#         m = re.search(url_regex, page)
#
#         if m:
#             tables = soup.find_all('table')
#             table = [table for table in tables if table.img and table.img.get('src') and re.match(r'http://chart\.apis\.google\.com/chart', table.img.get('src'))][0]
#             table.img['src'] = 'snpedia_chart.png'
#             open('snp_db/'+rs+'/snpedia_chart.html', 'w').write(table.prettify(formatter='html').encode('utf-8'))

def download_hapmap_data():
    if not os.path.exists('hapmap_archive'):
        print 'downloading and unpacking hapmap data ...'
        # get index
        query = 'http://hapmap.ncbi.nlm.nih.gov/downloads/frequencies/latest_phaseIII_ncbi_b36/fwd_strand/non-redundant/'
        response = urllib.urlopen(query)
        html = response.read()
        soup = BeautifulSoup(html)

        # create local archive
        prefix = 'http://hapmap.ncbi.nlm.nih.gov/downloads/frequencies/latest_phaseIII_ncbi_b36/fwd_strand/non-redundant/'
        os.mkdir('hapmap_archive')
        filenames = set(a['href'] for a in soup.find_all('a') if re.search(r'\.txt\.gz', a['href']))
        for idx, filename in enumerate(filenames): 
            print 'processing file {0} out of {1} ...'.format(idx + 1, len(filenames))
            urllib.urlretrieve(prefix + filename, 'hapmap_archive/' + filename)
            os.system('gunzip hapmap_archive/' + filename)

def create_hapmap_database():
    if not os.path.isfile('hapmap_tmp.db'):
        print 'creating intermediate hapmap database ...'
        conn = sqlite3.connect('hapmap_tmp.db') 
        c = conn.cursor()

        c.execute('DROP TABLE IF EXISTS genotype')
        c.execute('''CREATE TABLE genotype
                (rs text, pop text, ref_allele_homo text, ref_allele_homo_freq real, ref_allele_hetero text, ref_allele_hetero_freq real, other_allele_homo text, other_allele_homo_freq real)''')
        c.execute('CREATE INDEX idx_genotype_rs ON genotype (rs)')

        # c.execute('DROP TABLE IF EXISTS allele')
        # c.execute('''CREATE TABLE allele
        #         (rs text, pop text, ref_allele text, ref_allele_freq real, other_allele text, other_allele_freq real)''')
        # c.execute('CREATE INDEX idx_allele_rs ON allele (rs)')

        hapmap_files = os.listdir('hapmap_archive')
        for idx, f in enumerate(hapmap_files):
            print 'processing file {0} out of {1} ...'.format(idx + 1, len(hapmap_files))

            reader = csv.reader(open('hapmap_archive/' + f), delimiter=' ', quotechar='#')

            next(reader, None) # skip header
            for row in reader:

                pop = re.search(r'(ASW)|(CEU)|(CHB)|(CHD)|(GIH)|(JPT)|(LWK)|(MEX)|(MKK)|(TSI)|(YRI)', f).group(0)

                if re.search(r'genotype', f):
                    c.execute('INSERT INTO genotype VALUES (?, ?, ?, ?, ?, ?, ?, ?)', (row[0].lower(), pop, row[10], row[11], row[13], row[14], row[16], row[17]))
                else:
                    pass
                    # c.execute('INSERT INTO allele VALUES (?, ?, ?, ?, ?, ?)', (row[0].lower(), pop, row[10], row[11], row[13], row[14]))
        conn.commit()
        conn.close()

def add_final_hapmap_data(accepted_rsnumbers):
    print 'generating hapmap charts ...'

    conn = sqlite3.connect('hapmap.db') 
    hapmap_conn = sqlite3.connect('hapmap_tmp.db') 
    c = conn.cursor()
    hapmap_c = hapmap_conn.cursor()

    c.execute('DROP TABLE IF EXISTS main')
    c.execute('''CREATE TABLE main (rs text PRIMARY KEY, genotype1 text, genotype2 text, genotype3 text,
            pop1 text, pop1_freq1 real, pop1_freq2 real, pop1_freq3 real,
            pop2 text, pop2_freq1 real, pop2_freq2 real, pop2_freq3 real,
            pop3 text, pop3_freq1 real, pop3_freq2 real, pop3_freq3 real,
            pop4 text, pop4_freq1 real, pop4_freq2 real, pop4_freq3 real,
            pop5 text, pop5_freq1 real, pop5_freq2 real, pop5_freq3 real,
            pop6 text, pop6_freq1 real, pop6_freq2 real, pop6_freq3 real,
            pop7 text, pop7_freq1 real, pop7_freq2 real, pop7_freq3 real,
            pop8 text, pop8_freq1 real, pop8_freq2 real, pop8_freq3 real,
            pop9 text, pop9_freq1 real, pop9_freq2 real, pop9_freq3 real,
            pop10 text, pop10_freq1 real, pop10_freq2 real, pop10_freq3 real,
            pop11 text, pop11_freq1 real, pop11_freq2 real, pop11_freq3 real)''')

    populations = ['ASW','CEU','CHB','CHD','GIH','JPT','LWK','MEX','MKK','TSI','YRI']

    snps = set(row[0] for row in hapmap_c.execute('SELECT DISTINCT rs FROM genotype'))

    # filter out rsnumbers we don't want 
    if accepted_rsnumbers:
        snps = snps & accepted_rsnumbers

    for idx, rs in enumerate(snps): 
        if (idx + 1) % 100 == 0:
            print '{0} out of {1} snps processed ...'.format(idx + 1, len(snps))

        result = list(hapmap_c.execute('SELECT * FROM genotype WHERE rs = ?', (rs,)))

        # fill in missing data
        data = [] 
        for pop in populations:
            if pop in [row[1] for row in result]: 
                data.append([row for row in result if row[1] == pop][0])
            else:
                data.append([rs, pop, "", 0, "", 0, "", 0])

        parameters = [rs]
        # get the three genotypes in the right format
        row = result[0]
        parameters.extend(''.join(row[i].split('/')) for i in [2,4,6])
        # get the frequencies for each population as percentages
        for row in data:
            parameters.append(row[1])
            for i in [3, 5, 7]:
                parameters.append(row[i]*100)

        c.execute('INSERT INTO main VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)', parameters)

    conn.commit()
    conn.close()
    hapmap_conn.close()

def download_and_add_hapmap_data(accepted_rsnumbers):
    download_hapmap_data()
    create_hapmap_database()
    add_final_hapmap_data(accepted_rsnumbers)

# def get_omim_text(rsnumbers):
#     for rs in rsnumbers:
#         query = 'http://www.ncbi.nlm.nih.gov/omim/?term='+rs+'&report=uilist&format=text'
#         response = urllib2.urlopen(query)
#         html = response.read()
#         soup = BeautifulSoup(html)
#         entry = soup.pre.text.split('\n')[0]
#         if entry:
#             url = 'http://api.omim.org/api/entry?apiKey=45CB5D7EF90D6522646B46F5095277D7B225F453&include=text&format=html&mimNumber=' + entry
#             print url
#             # urllib.urlretrieve(url, 'snp_db/' + rs + '/omim_entry.html')
#             urllib.urlretrieve(url, 'test.html')

def download_and_add_dbsnp_data(accepted_rsnumbers):
    print 'downloading, parsing and adding dbsnp data ...'

    conn = sqlite3.connect('dbsnp.db') 
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS main')
    c.execute('''CREATE TABLE main
            (rs text PRIMARY KEY, gene_id text, symbol text)''')

    # get index
    query = 'http://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b141_GRCh38/XML/'
    response = urllib.urlopen(query)
    html = response.read()
    soup = BeautifulSoup(html)

    # download and parse files 
    prefix = 'ftp://ftp.ncbi.nlm.nih.gov/snp/organisms/human_9606_b141_GRCh38/XML/'
    filenames = set(a['href'] for a in soup.find_all('a') if re.search(r'\.xml\.gz', a['href']))
    namespace = '{http://www.ncbi.nlm.nih.gov/SNP/docsum}'
    for idx, filename in enumerate(filenames): 

        print 'processing file {0} out of {1} ...'.format(idx + 1, len(filenames))

        urllib.urlretrieve(prefix + filename, 'dbsnp_tmp.xml.gz')
        os.system('gunzip dbsnp_tmp.xml.gz')

        context = etree.iterparse('dbsnp_tmp.xml', events=['start', 'end'])
        context = iter(context)
        _, root = context.next()
        inside_rs_element = False
        children = set() 
        for event, element in context:
            if event == 'start' and element.tag == namespace+'Rs':
                # must remember that we are inside an rs element so prematurely clear child nodes
                inside_rs_element = True
            if event == 'end':
                if element.tag == namespace+'Rs':
                    rs = 'rs' + element.get('rsId')
                    if (not accepted_rsnumbers) or (rs in accepted_rsnumbers):
                        assembly = element.find(namespace+'Assembly')
                        if assembly is not None:
                            component = assembly.find(namespace+'Component')
                            if component is not None:
                                maploc = component.find(namespace+'MapLoc')
                                if maploc is not None:
                                    fxnset = maploc.find(namespace+'FxnSet')
                                    if fxnset is not None:
                                        gene_id = fxnset.get('geneId')
                                        symbol = fxnset.get('symbol')
                                        try:
                                            c.execute('INSERT INTO main VALUES (?, ?, ?)', (rs, gene_id, symbol))
                                        except sqlite3.IntegrityError:
                                            pass

                    # leaving the rs element, so the children can now safely be cleared
                    inside_rs_element = False
                    for child in children:
                        child.clear()
                    children.clear()

                if inside_rs_element:
                    # can't clear it yet, but must remember to clear later
                    children.add(element)
                else:
                    element.clear()
                    if element.getparent() is root:
                        root.remove(element)

        conn.commit()
        os.remove('dbsnp_tmp.xml')

    conn.close()

def generate_complete_database(accepted_rsnumbers=set()):
    
    print 'generating databases in ' + os.getcwd() + ' ...'

    # download, process and add the data from snpedia 
    download_and_add_snpedia_data(accepted_rsnumbers)

    # download, process and add the data from hapmap
    download_and_add_hapmap_data(accepted_rsnumbers)

    # download, process and add the data from dbsnp
    download_and_add_dbsnp_data(accepted_rsnumbers)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        generate_complete_database(accepted_rsnumbers=load_accepted_rsnumbers(sys.argv[1]))
    else:
        generate_complete_database()

