import json
import os
import re
import shutil

from categorize_variant import tags_from_summary
import pgp_parse_genome_reports
import variant_parsing

VARIANT_OUT_DIR = 'variants_final'
GENOME_OUT_DIR = 'genomes_final'


def get_all_reports_and_variants():

    # Make sure the output directories exist.
    if not os.path.isdir(VARIANT_OUT_DIR):
        os.mkdir(VARIANT_OUT_DIR)
    if not os.path.isdir(GENOME_OUT_DIR):
        os.mkdir(GENOME_OUT_DIR)

    print "Getting report IDs"
    report_ids = pgp_parse_genome_reports.reports()
    for person_id in report_ids.keys():
        print "Looking at {}".format(person_id)
        # Check filepath, skip if already exists.
        genome_json_filepath = os.path.join(
            GENOME_OUT_DIR, person_id + "_GenomeReport.json")
        if os.path.exists(genome_json_filepath):
            with open(genome_json_filepath) as f:
                genome_data = json.load(f)
        else:
            continue

        # Get data from variant pages - or load it, if this was already done.
        i = -1
        for variant_data in genome_data['Variants']:
            print "Working on variant {}".format(variant_data['Variant Name'])
            i += 1

            # Expected filepath for storing Variant data.
            variant_json_filepath = os.path.join(
                VARIANT_OUT_DIR, variant_data['Variant Name'] + '_report.json')

            if os.path.exists(variant_json_filepath):
                # Load this data if it already exists
                with open(variant_json_filepath, 'r') as file:
                    variant_page_data = json.load(file)
            else:
                # Otherwise, generate it and save it.
                variant_page_data = variant_parsing.parse_data(
                    variant_data['Variant Name'], variant_data['Variant Page'])
                variant_data.update(variant_page_data)

            variant_data['Condition Tags'] = tags_from_summary(
                variant_data['Summary'])

            # Update variant data with all but 'Status' and 'Participant',
            # which are genome specific.
            updating_data = {
                k: variant_data[k] for k in variant_data.keys() if
                k != 'Status' and k != 'Participant'}
            variant_page_data.update(updating_data)
            with open(variant_json_filepath, 'w') as file:
                json.dump(variant_page_data, file, indent=4,
                          sort_keys=True)

            # Update the genome report with updated variant data.
            genome_data['Variants'][i].update(variant_page_data)

        # Note from April 2016: New genome reports were generated with
        # pgp_parse_genome_reports. Those were then updated with the following
        # lines, and moved to a name consistent with past naming.
        with open(genome_json_filepath, 'w') as file:
            json.dump(genome_data, file, indent=4, sort_keys=True)
        new_name = re.sub('GenomeReport', 'report', genome_json_filepath)
        shutil.move(genome_json_filepath, new_name)

if __name__ == "__main__":
    get_all_reports_and_variants()
