from platform import system
changeD = (system() == "macOS" or system() == "iOS")
def writeToFile(name,  text):
	if changeD:
		myFile = open("HTML Pages/%s.html" % name, "w")
	else:
		myFile = open("HTML Pages\\%s.html" % name, "w")
	myFile.write(text)
	myFile.close()



def translateOut(runnerObj):
	text = "<h1> %s </h1>\n" % runnerObj.name
	text += "\n<h5> Total Points:%d \n Average Points: %.3f </h5>\n" %  (runnerObj.getTotalPoints(), runnerObj.getAveragePoints())
	text += "\n<h2>Events:</h2>\n"
	toAdd = "\n<h2>More Info:</h2>\n"
	for event in runnerObj.getEvents():
		text += "<h4> %s </h4>\n" % event
		text += "<p> PR: %.2f </p>\n\n" % runnerObj.getPREvent(event)
		toAdd += "<p> %s </p>\n\n" % runnerObj.toHTMLEvent(event)
	writeToFile(runnerObj.name, text + toAdd)

def makeMenu(runnersList):
	text = "<h1> Runners </h1>\n\n"
	for runner in runnersList:
		text += "<h4> <a href=%s> %s </a></h4>" % (getLink(runner), runner)
	writeToFile("main menu", text)

def getLink(runner):
	return "/runtracker/%s.html" % runner

