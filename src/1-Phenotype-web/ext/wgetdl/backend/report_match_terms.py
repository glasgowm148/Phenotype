import csv
import json
import os
import sys

from categorize_variant import tags_and_match_terms_from_summary

VARIANTS_DIR = 'variants_final'


if __name__ == '__main__':
    outfilepath = sys.argv[1]

    # Be safe, don't overwrite an existing file.
    if os.path.exists(outfilepath):
        raise ("Error: Output file target {}".format(outfilepath) +
               "already exists! Move or remove this first.")

    # Set up CSV output.
    csv_outfile = open(outfilepath, 'w')
    csv_out = csv.writer(csv_outfile)
    header = ['Variant', 'Variant URL', 'Summary', 'Matched tags',
              'Tags and match terms']
    csv_out.writerow(header)

    for filename in os.listdir(VARIANTS_DIR):
        if not filename.endswith(".json"):
            continue
        with open(os.path.join(VARIANTS_DIR, filename)) as f:
            jsondata = json.load(f)
        matched = tags_and_match_terms_from_summary(jsondata['Summary'])

        # Python has historically sucked at Unicode.
        # If this is run with Python 2.7 it needs to catch Unicode.
        # Python 3.x runs this without error, but this supports 2.7 because
        # many people continue running things with 2.7.
        try:
            csv_out.writerow([jsondata['Variant'],
                              jsondata['URL'],
                              jsondata['Summary'],
                              str([m[0] for m in matched]),
                              str([str(m) for m in matched])])
        except UnicodeEncodeError:
            csv_out.writerow([jsondata['Variant'],
                              jsondata['URL'],
                              jsondata['Summary'].encode('utf-8'),
                              str([m[0] for m in matched]),
                              str([str(m) for m in matched])])

    csv_outfile.close()
