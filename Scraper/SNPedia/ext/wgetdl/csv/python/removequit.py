#removes quitters from a csv file
#to run: 
#python removequit.py oldFile.csv newFile.csv

import sys

# parse all the command line args
commandList = sys.argv
oldFileName = commandList[1]
newFileName = commandList[2]

#get the complete list of users
def removeQuit(inFile, outFile): 
	oldFile = open(inFile, "r")
	oldData = oldFile.readlines()
	oldFile.close()
	#create/open new file
	newFile = open(outFile, "wb")
	#get quitters 
	quitFile = open("quit.txt", "r")
	quitData = quitFile.readlines()
	quitFile.close()

	#create a dictionary of quitters
	quitDict = dict() 
	for line in quitData: 
		us = line.strip()
		quitDict[us] = [us]

	#check each user in the old file to see if they are a quitter
	for user in oldData: 
		userLine = user.split(",", 2)
		userID = userLine[1][0:]
		if userID not in quitDict: 
			newFile.write(user)

	newFile.close()


#removeQuit(oldFileName, newFileName)

