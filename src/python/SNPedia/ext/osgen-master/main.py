import loadgenome as lg
import parse as prs
import makepdf as mpdf
import sys, getopt

#print lg.loadgen("sample genomes/23andme_sample.txt")

#
def main(argv):
    input_file = ''
    output_file = ''
    usage = 'Usage: python main.py -i <input_file> -o <output_file>'
    try:
        opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
    except getopt.GetoptError:
        print(usage)
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print(usage)
            sys.exit()
        elif opt in ("-i", "--ifile"):
            input_file = arg
        elif opt in ("-o", "--ofile"):
            output_file = arg
    if not input_file:
        print(usage)
        sys.exit(2)
    elif not output_file:
        output_file = 'my_results'

    mpdf.go(input_file, output_file)

if  __name__ =='__main__':
    main(sys.argv[1:])
