import sys, glob, os
from xml.etree.ElementTree import ParseError
sys.path.append("..")

import parsexml

def testall():
    os.chdir("../xml files")
    for f in glob.glob("*.xml"):
        try:
            print "trying file %s..." % f
            parsexml.returnSNPs(f)
        except ParseError as e:
            print "File %s has invalid xml syntax: %s" % (f,str(e))
        print '\n'

def testone(filename):
    parsexml.loadxml(filename)

if __name__ == '__main__':
    testall()
