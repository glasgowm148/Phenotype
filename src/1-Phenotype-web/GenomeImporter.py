import argparse

from phenotype.genome_importer import PersonalData


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-f", "--filepath", help="raw genome file to import", required=False)
    args = parser.parse_args()

    if args.filepath:
        personal = PersonalData(filepath=args.filepath)
        print(len(personal.personaldata))
        print(personal.snps[:50])
        print(list(personal.yourData.keys())[:10])
        print(list(personal.yourData.values())[:10])
