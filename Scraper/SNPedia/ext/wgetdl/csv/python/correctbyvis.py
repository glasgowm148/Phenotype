#spits out a text file with data about visualizations
#to run from terminal:
#python correctbyvis.py input.csv output.txt 

import sys
import string

# parse all the command line args
commandList = sys.argv
oldFileName = commandList[1]
newFileName = commandList[2]


def correctByVis(inFile, outFile):
	#open the files
	oldFile = open(inFile, "r")
	oldData = oldFile.readlines()
	oldFile.close()
	newFile = open(outFile, "wb")

	#vars to track num correct by vis
	treemap = 0
	bar = 0
	bubble = 0 
	table = 0 
	for line in oldData: 
		user = line.split(",")
		visType = user[2]
		userLen = len(user) 
		correct = user[userLen -1]
		if visType == "bar":
			bar += 1
		if visType == "bubble":
			bubble += 1
		if visType == "treemap":
			treemap += 1
		if visType == "table":
			table += 1
	newFile.write("***STATISTICS***")
	newFile.write("Bar: " + str(bar))
	newFile.write("Bubble: " + str(bubble))
	newFile.write("Treemap: " + str(treemap))
	newFile.write("Table: " + str(table))

	
#correctByVis(oldFileName, newFileName)