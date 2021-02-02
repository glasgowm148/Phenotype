#!/usr/bin/python
"""
Use Selenium to simulate pressing the "Show All" radio button
Grab report page source, parse it, and produce JSON file

Contributors:
Nicole Francisco, for Wellesley HCI Lab
Madeleine Ball, PersonalGenomes.org
"""
import json
import os
import re
import urllib2

from bs4 import BeautifulSoup
from ordereddict import OrderedDict
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

EV_IMPACT_RANK = {
    'Well-established protective': 1,
    'Likely protective': 2,
    'Well-established benign': 3,
    'Likely benign': 4,
    'Uncertain protective': 5,
    'Uncertain benign': 6,
    'Uncertain not reviewed': 7,
    'Uncertain pathogenic': 8,
    'Likely pathogenic': 9,
    'Well-established pathogenic': 10,
    'Likely pharmacogenetic': 11,
    'Uncertain pharmacogenetic': 12,
    'Well-established pharmacogenetic': 13}

HEADERS = ["Variant Name", "Variant Page", "Clinical Importance",
           "Evidence", "Impact", "Inheritance", "Status", "Allele Frequency",
           "Summary"]


def reports():
    '''
    Generate a dictionary of personID's and their genomic report IDs
    '''
    genomes_source = urllib2.urlopen(
        "https://my.pgp-hms.org/public_genetic_data?data_type=Complete+Genomics&commit=Search").read()

    print "Done retrieving genome report URL."
    # pgp = BeautifulSoup(genomes_source)
    pgp = BeautifulSoup(genomes_source, "lxml")  # 6.9.15 Johanna changed

    genomes_table = pgp.find("div",
                             {"class": "profile-data"})

    persons = genomes_table.findChildren('tr')
    persons.pop(0)

    report_vals = dict()

    for person in persons:
        cells = person.findAll("td")

        # personID = cells[1].find('a')
        personID = cells[1].a
        if personID:
            personID = personID.string
        else:
            # If we don't have personID, we can't use this row.
            continue

        reportID = cells[7].find('a')
        if not reportID:
            # If this isn't found, there's no GET-Evidence report data.
            continue

        reportID = reportID.get('href')

        # If there are multiple reports for an individual, this takes the
        # last report, which is the most recent one.
        report_vals[personID] = reportID

    return report_vals


def get_all_reports():
    '''
    Convert all online genomic reports to JSON files
    '''
    pgp_genomes = reports()
    for personID in pgp_genomes.keys():
        write_genome_report(personID, pgp_genomes[personID])


def get_genome_report_data(personID, genome_id):
    '''
    Given a person's ID, produce JSON file of his/her genome report
    '''
    reportUrl = (genome_id)
    print "Analyzing " + reportUrl

    # EXTRACT PAGE SOURCE
    browser = webdriver.Firefox()
    browser.get(reportUrl)

    try:
        # As of Apr 2016 this creates an error, another element is "on top"
        # show_all = browser.find_element_by_id('variant_filter_radio1')
        # ... this seems to get that "correct" element.
        show_all = browser.find_element_by_class_name('ui-corner-right')
        # if browser can't find element, then...?
        show_all.click()
        print "Clicked on filter button"
    except NoSuchElementException:  # Can't find element via Selenium
        print "No variant filter button available."
        print "Aborting report for {} at URL {}".format(personID, genome_id)
        browser.quit()
        return

    # grab the page source from the page "Variant report for hu0E64A1"
    html_source = browser.page_source
    browser.quit()
    print "Source retrieved"

    # SETUP (parser, csv writer, and peripheral data to create new columns)
    # Beautiful Soup
    html_encode = html_source.encode("utf-8")
    pgp = BeautifulSoup(html_encode)

    report_data = {'Participant': personID,
                   'Report URL': reportUrl,
                   'Variants': []}

    # PARSE WEBPAGE
    # Find relevant table (first of three)--> parse ea. column w/in ea. row
    table_children = pgp.findChildren("table")
    genome_report = table_children[0].findChildren("tr")
    link = "http://evidence.pgp-hms.org/"

    # Grab all person's variant information, store for later JSON file creation
    for row in genome_report:
        cols = row.findChildren("td")
        if not cols:
            continue

        data = {k: None for k in HEADERS}

        # Parse out variant name and expected URL.
        data['Variant Name'] = cols[0].string
        data['Variant Page'] = link + cols[0].string

        # Parse out clinical importance.
        data['Clinical Importance'] = cols[1].string

        # Parse out 'Impact' and 'Status'.
        # These are the manipulations the code previously performed, not
        # necessarily the best approach.
        evidence_list = [r'Well-established', r'Likely', r'Uncertain']
        impact_list = [r'not reviewed', r'pathogenic', r'protective',
                       r'benign', r'pharmacogenetic']
        inheritance_list = [r'Complex/Other', r'Unknown', r'Recessive',
                            r'Dominant']
        status_list = [r'Homozygous', r'Heterozygous',
                       r'Carrier \(Heterozygous\)']
        col2_re = (
            r'^(?P<evidence>' + r'|'.join(evidence_list) + r') ' +
            r'(?P<impact>' + r'|'.join(impact_list) + r')\W*' +
            r'(?P<inheritance>' + r'|'.join(inheritance_list) + r'), ' +
            r'(?P<status>' + r'|'.join(status_list) + r')$'
        )
        col2_re_match = re.match(col2_re, cols[2].text)
        data['Evidence'] = col2_re_match.group('evidence')
        data['Impact'] = col2_re_match.group('impact').title()
        data['Inheritance'] = col2_re_match.group('inheritance')
        data['Status'] = col2_re_match.group('status')
        if data['Status'] == 'Carrier (Heterozygous)':
            data['Status'] = 'Heterozygous'

        data['Allele Frequency'] = cols[3].string
        data['Summary'] = cols[4].string

        if '%' in data['Allele Frequency']:
            data['Allele Frequency'] = str(float(
                data['Allele Frequency'].replace('%', ''))/100)
        else:
            data['Allele frequency'] = None

        # By constructing the final output dict this way, we guarantee
        # that the output contains the HEADERS keys and only those keys.
        data_out = OrderedDict([(k, data[k]) for k in HEADERS])
        report_data['Variants'].append(data_out)

    return report_data


def write_genome_report(person_id, genome_id):
    # JSON file writer. Data from each row is stored in json_arr.
    if not os.path.isdir('reports'):
        os.mkdir('reports')
    json_report = open("reports/" + person_id + "_GenomeReport.json", 'w')

    report_data = get_genome_report_data(person_id, genome_id)

    # Sort all the data from variant rows, then dump to JSON file
    json.dump(report_data, json_report, indent=4)


if __name__ == '__main__':
    # grab variant report information for hu43860C
    # get_genome_report("hu43860C", "8280b5e784be559f7e817261129575d5dc10c46e");

    # Get reports only for personIDs matching 'harvard_pgp_attendees.txt'
    # As of 2015/06/11, this gets 17 available reports.
    # existing_reports()

    # Get all available reports.
    get_all_reports()
