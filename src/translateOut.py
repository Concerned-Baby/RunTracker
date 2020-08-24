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
	writeToFile(runnerObj.name, "<h1> %s </h1>" % runnerObj.name)

