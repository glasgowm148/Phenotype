#removes quitters from a tab deliminated file
#MUST have correct input file format or will fail spectacularly 
#to run: 
#python removequit.py oldFile.txt newFile.csv
#this is for vis.csv BECAUSE THAT FILE IS STUPID

import sys
import string

# parse all the command line args
commandList = sys.argv
oldFileName = commandList[1]
newFileName = commandList[2]


def removeQuitVis(inFile, outFile):
	#create/open new file
	newFile = open(outFile, "wb")
	#get quitters 
	quitFile = open("quit.txt", "r")
	quitData = quitFile.readlines()
	quitFile.close()

	#create a dictionary of quitters
	quitDict = dict()
	us = "" 
	for entry in quitData: 
		us = entry.strip()
	quitDict[str(us)] = [str(us)]
	

	#get the complete list of users
	oldFile = open(inFile, "r")
	allLines = oldFile.read()
	#strips file of weird characters to make life easier
	middle = string.replace(allLines, "\n", "")
	newThing = string.replace(middle, "\r", "")
	newnewThing = string.replace(newThing, ",", "") 
	eachPiece = newnewThing.split("\t")
	#vars for for loop to help sep by user
	writing = False
	count = 0
	for piece in eachPiece:
		if count == 1: #new user! Yay!
			if str('"' + piece + '"') not in quitDict: #not a quitter
				writing = True
				newFile.write(piece + ",")
			else : #quitter 
				writing = False
			count = count + 1
		elif count < 28: 
			if writing: 
				newFile.write(piece + ",")
			count = count + 1
		else: #timestamp and numeric ordering for next one 
			pieces = piece.split(" ")
			if writing: 
				newFile.write(pieces[0][0:] + "\n") #writes out time stamp, ignores numeric ordering 
			count = 1 

	oldFile.close()
	newFile.close()


#removeQuitVis(oldFileName, newFileName)
