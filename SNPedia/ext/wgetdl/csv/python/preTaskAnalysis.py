#Analysis of the pre-task results
#How to run:  
#python preTaskAnalysis.py oldFileName newFileName_UserAnalysis newFileName2_QuestionAnalysis

import sys
commandList = sys.argv
oldFileName = commandList[1]
newFileName = commandList[2]
newFileName2 = commandList[3]

numUsers = 0 #set when reading in the file
perfectScore = 0 #keeps track of the num of users with a perfect score
perfectScorers = [] #keeps track of all userIDs of users with a perfect score
qIncorrect = [0,0,0,0,0,0]  #keeps track of the num of users who got a specific question
		#incorrect. each place in the array corresponds to a question



# reads in a file, creates an array of users. each user is also an array of their ID 
# and quiz answers
def processFile(file):
	file = open(file, "r").read()
	allData = [] 
	for line in file.splitlines():
		firstArray = line.split(",")
		firstArray[len(firstArray)-1] = firstArray[len(firstArray)-1].strip("\n")
		allData.append(firstArray)
		#print firstArray
	numUsers = len(allData)
	#print numUsers
	return allData

# returns a 1 if the question is answered incorrectly, returns 0 if it is not
def processQuestion(user, question, answer):
	print (user[question + 1].lower())
	print answer
	print (user[question + 1].lower() != answer and (user[question + 1].lower()) != '"'+ answer + '"')
	if (user[question + 1].lower()) != answer and (user[question + 1].lower()) != '"'+ answer + '"':
		qIncorrect[question-1] = qIncorrect[question-1] + 1
		return 1
	else : 
		return 0
	
	
#adds up the number of incorrect answers of a user, calls on the helper method above
def processOneUser(user):
	numIncorrect = 0
	numIncorrect += processQuestion(user, 1, "false") #calls helper method above
	numIncorrect += processQuestion(user, 2, "99")
	numIncorrect += processQuestion(user, 3, "false")
	numIncorrect += processQuestion(user, 4, "true")
	numIncorrect += processQuestion(user, 5, "true")
	numIncorrect += processQuestion(user, 6, "true")
	print numIncorrect
	if numIncorrect == 0: 
		global perfectScore
		perfectScore = perfectScore + 1
		perfectScorers.append(user[1])
	percentIncorrect = round(((float(numIncorrect)/6)*100), 2) 
		   		#to calculate and round the percent to 2 decimals
	user.append(str(numIncorrect))
	user.append(str(percentIncorrect))


#writes the results in two files
#@params: allData takes in the user data that has been read in and will be processed
	#file is the name of the file that all of the analysed data will be written into, if the
	#file already exists, it will be overwritten, otherwise a new file is created
	#file2 is the name of the file that all of the analysed data will be written into, if the
	#file already exists, it will be overwritten, otherwise a new file is created
def writeResults(allData, file, file2):
	newFile = open(file, "w") #creates file to write the results of each user
	newFile.write(" , UserID, Q1, Q2, Q3, Q4, Q5, Q6, time, #Incorrect, %Incorrect, \n")
	for user in allData:
		processOneUser(user) #calls on helper method to process their data
		temp = ""
		for item in user:
			temp = temp + item + ", "
		temp = temp[0:len(temp)-2]
		newFile.write(temp)
		newFile.write("\n")
	newFile.close()
	#writing num of ppl who got each question incorrect
	newFile2 = open(file2, "w") #creates file to write the analysis of the questions, etc
	newFile2.write("Q1, Q2, Q3, Q4, Q5, Q6, \n")
	temp2 = ""
	for datapoint in qIncorrect:
		temp2 = temp2 + str(datapoint) + ", "
	temp2 = temp2[0:len(temp2)-2]
	newFile2.write(temp2)
	newFile2.write("\n")
	newFile2.write("#Users with Perfect Score: ," + str(perfectScore))
	newFile2.write("\nUsers with Perfect Score:\n")
	for userID in perfectScorers:
		newFile2.write(userID)
		newFile2.write("\n")
	newFile2.close()

def preTaskAnalysis(inFile, outFile1, outFile2):
	allUserData = processFile(inFile)
	writeResults(allUserData,outFile1, outFile2)



# TESTING USER DATA	
#preTaskAnalysis(oldFileName, newFileName, newFileName2)
#allUserData = processFile(oldFileName)
#writeResults(allUserData, newFileName, newFileName2)

#allUserData = processFile("pretask_4.csv")
#writeResults(allUserData, "pretask_4_Analysis.csv", "pretask_4_QuestionAnalysis.csv")
