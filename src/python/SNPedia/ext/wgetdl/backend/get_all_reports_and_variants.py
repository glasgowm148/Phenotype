import json
import os

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

    report_ids = pgp_parse_genome_reports.reports()
    for person_id in report_ids.keys():
        # Check filepath, skip if already exists.
        genome_json_filepath = os.path.join(
            GENOME_OUT_DIR, person_id + "_report.json")
        if os.path.exists(genome_json_filepath):
            continue

        # Get data from genome report page.
        genome_data = pgp_parse_genome_reports.get_genome_report_data(
            person_id, report_ids[person_id])

        # Get data from variant pages - or load it, if this was already done.
        for variant_data in genome_data['Variants']:

            # Expected filepath for storing Variant data.
            variant_json_filepath = os.path.join(
                VARIANT_OUT_DIR, variant_data['Variant Name'] + '_report.json')

            if os.path.exists(variant_json_filepath):
                # Load this data if it already exists
                with open(variant_json_filepath, 'r') as file:
                    variant_page_data = json.load(file)
                if 'Variant' in variant_page_data:
                    del variant_page_data['Variant']

                # Update variant data anyway, we've updated a report parsing
                # bug and improved the condition tags script.
                variant_data['Condition Tags'] = tags_from_summary(
                    variant_data['Summary'])
                variant_page_data.update({
                    k: variant_data[k] for k in variant_data if k != 'Status'
                    and k != 'Participant'})

                variant_data.update(variant_page_data)

                with open(variant_json_filepath, 'w') as file:
                    json.dump(variant_page_data, file, indent=4,
                              sort_keys=True)
            else:
                # Otherwise, generate it and save it.
                variant_page_data = variant_parsing.parse_data(
                    variant_data['Variant Name'], variant_data['Variant Page'])
                variant_data.update(variant_page_data)
                variant_data['Condition Tags'] = tags_from_summary(
                    variant_data['Summary'])

                # Update variant data with all but 'Status' and 'Participant',
                # which are genome specific.
                variant_page_data.update({
                    k: variant_data[k] for k in variant_data if k != 'Status'
                    and k != 'Participant'})

                with open(variant_json_filepath, 'w') as file:
                    json.dump(variant_page_data, file, indent=4,
                              sort_keys=True)

        with open(genome_json_filepath, 'w') as file:
            json.dump(genome_data, file, indent=4, sort_keys=True)


if __name__ == "__main__":
    get_all_reports_and_variants()
