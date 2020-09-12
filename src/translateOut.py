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
	text = '<!DOCTYPE html> \n<head>\n\t <link rel="stylesheet" href="/css/runner.css"> \n</head>'
	text += "<h1> %s </h1>\n" % runnerObj.name
	text += '\n<section id="section"><h5> Total Points:%d \n Average Points: %.3f </h5></section>\n' %  (runnerObj.getTotalPoints(), runnerObj.getAveragePoints())
	text += '\n<section id="section">\n<h2>Events:</h2>\n'
	toAdd = '\n</section>\n<section id="section"><h2>More Info:</h2>\n'
	for event in runnerObj.getEvents():
		text += "<h4> %s </h4>\n" % event
		text += "<p> PR: %.2f </p>\n\n" % runnerObj.getPREvent(event)
		toAdd += "<p> %s </p>\n\n" % runnerObj.toHTMLEvent(event)
	writeToFile(runnerObj.name, text + toAdd + "</section>")

def makeMenu(runnersList):
	text = '<head> <link rel="stylesheet" href="/css/runner.css" type="text/css"> </head>'
	text += '<h1> Runners </h1>\n\n'
	for runner in runnersList:
		text += '<section id="section"><h3> <a href=%s> %s </a></h3></section>' % (getLink(runner), runner)
	writeToFile("main menu", text)

def getLink(runner):
	return "/runtracker/%s.html" % runner

