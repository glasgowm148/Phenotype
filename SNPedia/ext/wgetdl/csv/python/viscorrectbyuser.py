#adds an extra column to a csv file which lists the number of correct qs by user
#currently only counts the first five questions
#to run from terminal: python viscorrectbyuser.py input.csv output.csv

import sys
import string

# parse all the command line args
commandList = sys.argv
fileName = commandList[1]
outName = commandList[2]

def visCorrectByUser(inFile, outFile):
	#open the csv and read the data
	currentFile = open(inFile, "r")
	filedata = currentFile.readlines()
	currentFile.close()

	#create/open the new file
	newFile = open(outFile, "wb")

	for user in filedata: 
		userData = user.split(",")
		ans1 = userData[2][0:]
		ans2 = userData[3][0:]
		ans3 = userData[4][0:]
		ans4 = userData[5][0:]
		ans5 = userData[6][0:]
		correct = 0
		if ans1 == "3": 
			correct += 1
		if ans2 == "2":
			correct += 1
		if ans3 == "greater":
			correct += 1
		if ans4 == "greater":
			correct += 1
		if ans5 == "less":
			correct += 1
		nextLast = userData[len(userData)-1] #strips the last element in the list of its newline so that we can add a new last element
		newNextLast = string.replace(nextLast, "\n", "")
		userData[len(userData)-1] = newNextLast
		userData.append(str(correct) + "\n") #add the new last character
		for each in userData: 
			newFile.write("," + each)

	newFile.close()
	

#visCorrectByUser(fileName, outName)

