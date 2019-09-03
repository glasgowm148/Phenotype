#!/usr/bin/python

'''creates HTML pages from the json reports'''

from bs4 import BeautifulSoup
import urllib2
import json
import re
import glob
import os.path

'''
to do
  *format generated htmls (especially publication links)
  *seperate parse_write_data function in two 
'''


def parse_links():
    variants_dict = {}
    for file in glob.glob(os.path.join('variants/', '*.json')):
        report = open(file, 'r')
        try:
            variant_url = json.load(report)['URL']
            report = open(file, 'r')
            variant_name = json.load(report)['Variant Name']
        except ValueError:
            continue
        variants_dict[variant_name] = variant_url
    return variants_dict


def parse_and_write_data(variants_dict):
    '''
    Parses variant data and generates HTML for each.
    '''
    for variant_name, variant_url in variants_dict.iteritems():
        # Parses data from a variant page (summary, ratings, publications)
        variant_report = urllib2.urlopen(variant_url)
        variant_page = BeautifulSoup(variant_report)

        # get summary report
        soup = variant_page.find('div', {'class': 'container'})
        rows = soup.findAll('p')
        page_text = []
        for row in rows:
            page_text.append(row.text)
        summ_index = page_text.index('Short summary')
        summary = rows[summ_index+1].text.rstrip()

        # get publication links
        publications = []
        for link in variant_page.findAll('a', attrs={'href': re.compile("^http://")}):
            if link.get('href').startswith("http://www.ncbi.nlm.nih.gov/pubmed"):
                publications.append(link.get('href').strip())

        # get score values
        soup = variant_page.find('table', {'class': 'quality_table'})
        rows = soup.findAll('td')
        page_text = []
        for row in rows:
            page_text.append(row.text)

        #comp_index = page_text.index("Computational")
        #func_index = page_text.index("Functional")
        #case_index = page_text.index("Case/Control")
        #fami_index = page_text.index("Familial")
        seve_index = page_text.index("Severity")
        trea_index = page_text.index("Treatability")
        pene_index = page_text.index("Penetrance")

        seve_score = page_text[seve_index+2]
        trea_score = page_text[trea_index+2]
        pene_score = page_text[pene_index+2]

        if not os.path.isdir('variants'):
            os.mkdir('variants')

        # Skip variant if it's already been done.
        html_filepath = "variants/html/" + variant_name + ".html"
        if os.path.exists(html_filepath):
            print html_filepath + " already exists\n"
            continue

        # html folder needs to already exist
        variant_html = open(html_filepath, 'w')
        '''
        write strings into html file here
        '''
        html_str = """
        <!doctype html>
        <html lang=“en”>
        <title>Genome Variant Report</title>
        <h1>Genome Variant Report</h1>
        <h2>
        """
        variant_html.write(html_str)
        variant_html.write(variant_name)
        variant_html.write("</h2><p>")
        variant_html.write(summary.encode("utf8", "ignore")+"</p>")
        html_str = """
        <h3>Ratings</h3>
        <table border="1" style="width:20%">
          <tr>
            <td>Penetrance:</td>
            <td>
        """
        variant_html.write(html_str)
        variant_html.write(pene_score)
        html_str = """
        </td>
          </tr>
          <tr>
            <td>Severity:</td>
            <td>
        """
        variant_html.write(html_str)
        variant_html.write(seve_score)
        html_str = """
        </td>
          </tr>
          <tr>
            <td>Treatability:</td>
            <td>
        """
        variant_html.write(html_str)
        variant_html.write(trea_score)
        html_str = """
        </td>
          </tr>
        </table>
        <h3>Publications</h3>
        <ul>
        """
        variant_html.write(html_str)
        for url in publications:
            variant_html.write("  <li>"+url+"</li>\n")
        variant_html.write("</ul></html>")

        variant_html.close()
        print html_filepath + " was created\n"


if __name__ == '__main__':
    variants_dict = parse_links()
    parse_and_write_data(variants_dict)
