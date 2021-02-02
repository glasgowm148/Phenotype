'''
This program reads in the variant descriptions and then assigns the variant
a category based on the diseases in the description.

    for each element in dictionary
        for item in array of search terms
            if description has one of key word (command - in )
                add category to new line
'''
import json
import re
import sys

CATEGORY_FILE = 'categories.json'
SYNDROME_FILE = 'syndromes_categories.json'


def tags_and_match_terms_from_summary(summary, cat_dict=None, synd_dict=None):
    """
    Return a list of tuples (tag, search_term) matched for a given summary.
    """
    tags_and_match_terms = []
    if not summary:
        return tags_and_match_terms
    category_dict, syndrome_dict = load_and_check_dicts(cat_dict, synd_dict)

    for category in category_dict:
        for search_term in category_dict[category]:
            if re.search(search_term, summary, re.I):
                tags_and_match_terms.append((category, 'search terms',
                                             search_term))

    for syndrome in syndrome_dict.keys():
        if re.search(syndrome, summary, re.I):
            cats = syndrome_dict[syndrome]
            for cat in cats:
                tags_and_match_terms.append((cat, 'syndromes', syndrome))

    return tags_and_match_terms


def load_and_check_dicts(category_dict, syndrome_dict):
    if not category_dict:
        with open(CATEGORY_FILE) as file:
            category_dict = json.load(file)
    if not syndrome_dict:
        with open(SYNDROME_FILE) as file:
            syndrome_dict = json.load(file)
    categories = category_dict.keys()
    # Check that syndrome_dict only lists valid categories.
    for syndrome in syndrome_dict.keys():
        unmatched = [cat for cat in syndrome_dict[syndrome] if
                     cat not in categories]
        if unmatched:
            raise Exception("Unmatched cats {} for {}!".format(
                            unmatched, syndrome))
    return category_dict, syndrome_dict


def tags_from_summary(variant_summary, cat_dict=None, synd_dict=None):
    """
    Takes in a string (variant_summary) and returns a list of tags.
    """
    tags = []

    # If variant_summary is empty or None, return an empty list.
    if not variant_summary:
        return ['Other']

    category_dict, syndrome_dict = load_and_check_dicts(cat_dict, synd_dict)

    # Look through dictionary with categories and search terms.
    for category in category_dict.keys():

        # Skip categories with no search terms
        if not category_dict[category]:
            continue

        # Loop through search terms for each category.
        for search_term in category_dict[category]:
            if re.search(search_term, variant_summary, re.I):
                tags.append(category)

    for syndrome in syndrome_dict.keys():
        if re.search(syndrome, variant_summary, re.I):
            tags = tags + syndrome_dict[syndrome]

    if len(tags) == 0:
        tags.append('Other')

    # Converting to a 'set' removes all duplicates.
    return sorted(list(set(tags)))


if __name__ == '__main__':
    """
    The following runs when this file is run directly from the command line.
    """
    #parse all command line args
    commandList = sys.argv
    cat_file = commandList[1]
    #rep_file = commandList[2]

    #open files
    category_file = open(cat_file, "r")
    #reports_file = open(rep_file, "r")

    #globals
    category_dict = json.load(category_file)


#Testing Code
'''
summ1 = 'This variant is associated with decreased risk of type 2 diabetes. It is unclear whether this variant has additive effects, or acts in a dominant or recessive manner. Assuming diabetes has a lifetime risk of 36%, we estimate a decreased risk of around 1-2% per copy of this variant.'
summ2 = 'This common variant (HapMap 24.1% allele frequency) causes a loss of a glycosylation site (affecting the size of the protein when studied with gel electrophoresis) but does not affect enzyme activity or stability.'
tags = tags_from_summary(summ1)
tags2 = tags_from_summary(summ2)
print tags
print tags2
'''

'''
#categorizes each variant in a genome report based on the search terms in the
#dictionary created in the make_category_dict method
def categorize_variants(reports_file):
    reports_dict = json.load(reports_file)
    for report_name, report_content in reports_dict.items(): #loops through the genome reports in the dictionary
        for var_info in report_content: #loops through variants in a single genome report
            var_info_dict = {}
            var_info_dict = var_info
            var_info_dict['category'] = ''
            for category in category_dict: #loops through categories of dictionary
                if category_dict[category] != '': #makes sure category isn't empty
                    for search_term in category_dict[category]: #loops through search terms for each category
                        if search_term.lower() in var_info_dict['Summary'].lower():
                            var_info_dict['category'] = category
            if var_info_dict['category'] == '':
                var_info_dict['category'] = 'other'


'''
#categorize_variants(reports_file)
