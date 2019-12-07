#takes in a file (inFile), and finds users who either don't have a pretask, vis, or dem id 
#spits those users out in a text file (outFile) 
#to run from terminal: python getquitters.py inFileName outFileName 

import sys

# parse all the command line args
commandList = sys.argv
inputFileName = commandList[1]
outputFileName = commandList[2]

def getQuitters(inputFile, outputFile):
	outFile = open(outputFile, "wb") #will write into this file, or create it if it doesn't exist
	quitFile = open("quit.txt", "wb")  #creates a file of all userIDs who quit
	#opens the infile
	inFile = open(inputFile, "r")
	fileData2 = inFile.read()
	fileData = fileData2.split("\r")
	inFile.close()

	#goes through inFile line by line and writes out the quitters to a textfile
	print (len(fileData))
	for line in fileData:
		lineList = line.split(",")
		userID = lineList[0][0:]
		pretask = lineList[1][0:]
		if pretask == "\N": #if they didn't submit the pretask
			outFile.write(userID + " no pretask " + "\n")
			quitFile.write(userID + "\n")
		else: #if they didn't submit a visualization 
			vis1 = lineList[2][0:]
			vis2 = lineList[3][0:]
			vis3 = lineList[4][0:]
			vis4 = lineList[5][0:]
			if vis1 == "\N" and vis2 == "\N" and vis3 == "\N" and vis4 == "\N": 
				outFile.write(userID + " no vis " + "\n")
				quitFile.write(userID + "\n")
			else: #if they didn't submit the dem questions
				demID = lineList[6][0:]
				if demID == "\N": 
					outFile.write(userID + " no dem " + "\n")
					quitFile.write(userID + "\n")

	outFile.close()
	quitFile.close()

#getQuitters(inputFileName, outputFileName)
