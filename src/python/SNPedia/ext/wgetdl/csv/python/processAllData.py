#how to use:
#python processAllData.py userFile.csv pretaskFile.csv visFile.txt demFile.csv

import sys

import getquitters
import removequit
import removequitvis
import correctbyvis
import viscorrectbyuser
import preTaskAnalysis

commandList = sys.argv
user = commandList[1]
pretask = commandList[2]
vis = commandList[3]
dem = commandList[4]


#creates a new file name for the file of the data that has been analyzed
def createNewFileName(fileName, newEnding):
	filename = fileName[0:len(fileName)-4] + newEnding 
	return filename
	
	

def processAllData(userData, pretaskData, visData, demData):
	
	#produces the quit.txt file used to delete quitters from other files
	getquitters.getQuitters(userData, "quitData.csv") 
	print "1 Got here"
	
	pretaskNoQuit = createNewFileName(pretaskData, "_noQuits.csv")
	visNoQuit = createNewFileName(visData, "_noQuits.csv")
	print "2 Got here"
	
		#removes data from users who quit
	removequit.removeQuit(pretaskData, pretaskNoQuit)
	removequitvis.removeQuitVis(visData, visNoQuit)
	print "3 Got here"
	
	#analyses the data of the newly created files that do no include users who quit
	preTaskAnalysis.preTaskAnalysis(pretaskNoQuit, createNewFileName(pretaskData, "_UserAnalysis.csv"), 
			createNewFileName(pretaskData, "_QuestionAnalysis.csv"))
	    	
	correctbyvis.correctByVis(visNoQuit, createNewFileName("visNoQuit.csv", "_AnalysisByVis.csv"))
	
	viscorrectbyuser.visCorrectByUser(visNoQuit, createNewFileName("visNoQuit.csv", "_AnalysisByUser.csv"))

	
	
processAllData(user, pretask, vis, dem)
	