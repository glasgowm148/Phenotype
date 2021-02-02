from collections import OrderedDict
import csv
import json
import os

JSON_REPORTS_DIR = 'genomes_final'
CSV_REPORTS_DIR = 'csv_genome_reports'

# CSV_MAP: an OrderedDict defining CSV header and corresponding JSON data.
# The values in this OrderedDict are functions that generate the needed value,
# given a Variant dict from the JSON-formatted report's 'Variants' array.
CSV_MAP = OrderedDict([
    ('variant', lambda v: v['Variant Name']),
    ('gene_symbol', lambda v:
        v['Gene Symbol'] if 'Gene Symbol' in v else ''),
    ('summary', lambda v: v['Summary'] if v['Summary'] else ''),
    ('clinical_importance', lambda v: v['Clinical Importance']),
    ('evidence', lambda v: v['Evidence']),
    ('impact', lambda v: v['Impact']),
    ('frequency', lambda v:
        v['Allele Frequency'] if v['Allele Frequency'] != '?' else ''),
    ('category', lambda v: ';'.join(v['Condition Tags'])),
    ('inheritance', lambda v: v['Inheritance']),
    ('zygosity', lambda v: v['Status']),
    ('PMIDs', lambda v:
        ';'.join(v['PMID List']) if 'PMID List' in v else ''),
    # AFAICT there always - or almost always - only one dbSNP. -mpball
    ('dbSNP_ID', lambda v:
        v['dbSNP IDs'][0] if 'dbSNP IDs' in v else ''),
    ('penetrance_score', lambda v:
        v['Scores']['Penetrance'] if v['Scores']['Penetrance'] else ''),
    ('build_37_chromosome', lambda v:
        v['Build 37 Chromosome'] if 'Build 37 Chromosome' in v else ''),
    ('build_37_position', lambda v:
        v['Build 37 Position'] if 'Build 37 Position' in v else ''),
    ('build_37_variant_allele', lambda v:
        v['Build 37 Variant Allele'] if 'Build 37 Variant Allele' in v
        else ''),
    ('getev_report_url', lambda v: v['GET-Evidence Report URL']),
])


def write_csv_reports(json_report_dir, csv_output_dir):
    for filename in os.listdir(json_report_dir):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(json_report_dir, filename)) as fp:
            report_data = json.load(fp)
        outfile = open(os.path.join(csv_output_dir,
                                    report_data['Participant'] + '.csv'), 'w')
        csvout = csv.writer(outfile)
        csvout.writerow(CSV_MAP.keys())
        for variant in report_data['Variants']:
            # Hack to put participant-level report info on each variant row
            variant['GET-Evidence Report URL'] = report_data['Report URL']

            csvout.writerow([CSV_MAP[k](variant).encode('utf-8') for k in
                             CSV_MAP.keys()])

        outfile.close()

if __name__ == '__main__':
    if not os.path.isdir(CSV_REPORTS_DIR):
        os.mkdir(CSV_REPORTS_DIR)
    write_csv_reports(JSON_REPORTS_DIR, CSV_REPORTS_DIR)
