from os import path
from os import rename
from os import mkdir
from os import listdir
from re import match
from platform import system

FIELDEVENTS = ["Long Jump", "Triple Jump", "Pole Vault", "Discus", "Shotput", "High Jump"] #list of field events

global NoneType
NoneType = 14420133764129

#return None
#param String, String, String, String
def writeToFile(name, event, eType, text):
	myFile = open("Runners\\%s\\%s\\%s.txt" % (name,event, eType), "a")
	myFile.write(text)
	myFile.close()

#return List<String>
#param String, String, String
def readFileLBL(name, event, eType):
	myFile = open("Runners\\%s\\%s\\%s.txt" % (name, event, eType), "r")
	lines = myFile.readlines()
	myFile.close()
	return lines

#return boolean
#param String
def fileExists(directs):
	return path.exists(getFileName(directs))

#return String
#param String
def getFileName(directs):
	fileName = "Runners"
	for direct in directs:
		fileName += "\\%s" % direct
	return fileName

#return String
#param String
def getNotVersion(fileName):
	ind = fileName.rindex("\\") + 1
	return fileName[:ind] + "!" + fileName[ind:]

class Runner (object):
	#return None
	#param String
	def __init__(self, name):
		self.name = name 
		if not fileExists([self.name]):
			mkdir(getFileName([self.name]))
	def __str__(self):
		return self.name + " does the events " + str(self.getEvents())
	def __repr__(self):
		return self.__str__()

	#return String
	#param String
	def newEvent(self, eventName):
		fileName = getFileName([self.name, eventName])
		notV = getNotVersion(fileName)
		if self.hasEvent(eventName):
			return "Event Already Exists"
		elif path.exists(notV):
			rename(notV, fileName)
		else:
			mkdir(fileName)
			open(getFileName([self.name, eventName, "goal.txt"]), "x").close()
			open(getFileName([self.name, eventName, "time.txt"]), "x").close()
		return "Event Added"

	#return String
	#param String
	def removeEvent(self, eventName):
		fileName = getFileName([self.name, eventName])
		if not self.hasEvent(eventName):
			return "Event Already Gone"
		rename(fileName, getNotVersion(fileName))
		return "Event Removed"

	#return List<String>
	#param None
	def getEvents(self):
		return [event for event in listdir(getFileName([self.name])) if "!" not in event]

	#return boolean
	#param String
	def hasEvent(self, eventName):
		return eventName in self.getEvents()
	
	#return String
	#param String, double
	def newTime(self, eventName, time):
		if self.hasEvent(eventName):
			if ("%.2f" % time) not in self.getTimesEvent(eventName):
				writeToFile(self.name, eventName, "time", "%.2f\n" % time)
				return "Time Added"
			return "Time Already Exists"
		return "No Such Event"

	#return None
	#param String, double
	def removeTime(self, eventName, time):
		oldTimes = self.getTimesEvent(eventName)
		self.clearEvent(eventName, "time")
		for oldTime in oldTimes:
			print(str(oldTime + 1) + " : " + str(time))
			if not oldTime == time:
				self.newTime(eventName, oldTime)
	#return None
	#param String, String 
	def clearEvent(self, eventName, portion):
		myFile = open("Runners\\%s\\%s\\%s.txt" % (self.name, eventName, portion), "w")
		myFile.close()

	#return String
	#param String, double
	def newGoal(self, eventName, goal):
		if self.hasEvent(eventName):
			if goal not in self.getGoalsEvent(eventName):
				writeToFile(self.name, eventName, "goal",  "%.2f\n" % goal)
				return "Goal Added"
			return "Goal Already Exists"
		return "No Such Event"

	#return None
	#param String, double
	def removeGoal(self, eventName, goal):
		goals = self.getGoalsEvent(eventName)
		self.clearEvent(eventName, "goal")
		for oldGoal in goals:
			if oldGoal != goal:
				writeToFile(self.name, eventName, "goal",  "%.2f\n" % goal)

	#return List<double>
	#param String
	def getGoalsEvent(self, eventName):
		return [float(goal.strip()) for goal in readFileLBL(self.name, eventName, "goal")]
	
	#return List<double>
	#param String
	def getTimesEvent(self, eventName):
		return [float(time.strip()) for time in readFileLBL(self.name, eventName, "time")]
	
	#return double	
	#param String
	def getPRFieldEvent(self, eventName):
		times = self.getTimesEvent(eventName)
		return NoneType if len(times) == 0 else max(times)

	#return double
	#param String
	def getPREvent(self, eventName):
		times = self.getTimesEvent(eventName)
		if eventName in FIELDEVENTS:
			return self.getPRFieldEvent(eventName)
		return NoneType if len(times) == 0 else min(times)

	#return int
	#param String
	def getGoalsPassedEvent(self, eventName):
		return len([goal for goal in self.getGoalsEvent(eventName) if self.getPREvent(eventName) <= goal])

	#return int
	#param None
	def getAllGoalsPassed(self):
		return sum(self.getGoalsPassedEvent(event) for event in self.getEvents())

	#return double
	#param None
	def getAveragePoints(self):
		try:
			return self.getTotalPoints() / len([event for event in self.getEvents() if self.getPREvent(event) != NoneType])
		except ZeroDivisionError:
			return 0

	#return int
	#param None
	def getTotalPoints(self):
		return sum([self.getPointsEvent(event) for event in self.getEvents()])

	#return double
	#param double, double, double, double
	def calculatePoints(self, a, b, c, time):
		if time == NoneType:
			score = 0
		else:
			score = a * pow((b - time), c)
		try:
			return max(score, 0)
		except TypeError:
			return 0

	#return double
	#param String
	def getPointsEvent(self, event):
		if event == "100m":
			return self.calculatePoints(25.43471, 18, 1.81, self.getPREvent("100m"))
		elif event == "200m":
			return self.calculatePoints(3.32725, 42.5, 1.81, self.getPREvent("200m"))
		elif event == "300m":
			return self.calculatePoints(2.21152, 61, 1.81, self.getPREvent("300m"))
		elif event == "400m":
			return self.calculatePoints(1.53775, 82, 1.81, self.getPREvent("400m"))
		elif event == "800m":
			return self.calculatePoints(0.07462, 254, 1.88, self.getPREvent("800m"))
		elif event == "1600m":
			return self.calculatePoints(0.029828, 512, 1.85, self.getPREvent("1600m"))
		return 0

	#return String
	#param None
	def getAllPoints(self):
		text = ""
		for event in self.getEvents():
			text += "%s: %d\n" % (event, self.getPointsEvent(event))
		return text

	#return String
	#param String
	def getAllInfoEvent(self, eventName):
		toPrint = ""
		pr = self.getPREvent(eventName)
		if pr != NoneType:
			toPrint += "PR: %.2f\n\n" % pr
		else:
			toPrint += "PR: N/A\n\n"
		toPrint += "Points: %d\n\n" % self.getPointsEvent(eventName)
		goals = self.getGoalsEvent(eventName)
		goals.sort()
		passed = self.getGoalsPassedEvent(eventName)
		toPrint += "Goals: %d        Passed: %d\n\n" % (len(goals), passed)
		
		times = self.getTimesEvent(eventName)
		times.sort()
		toPrint += "\nTimes: %d\n" % len(times)
		for time in times:
			toPrint += "%.2f\n" % time
		return toPrint

	#return String
	#param String
	def toHTMLEvent(self, eventName):
		text =  "<h3> %s </h3>\n\n" % eventName

		pr = self.getPREvent(eventName)
		if pr != NoneType:
			text += "<h5> PR: %s </h5>\n\n" % pr
		else:
			text += "<h5> PR: N/A </h5>\n\n"

		goals = self.getGoalsEvent(eventName)
		goals.sort()
		text += "<h4> Goals: %d        Passed: %d</h4>\n\n" % (len(goals), self.getGoalsPassedEvent(eventName))
		for goal in goals:
			text += "<p> %.2f </p>\n" % goal

		text += "<h4> Times </h4>\n\n"
		times = self.getTimesEvent(eventName)
		times.sort()
		for time in times:
			text += "<p> %.2f </p>\n" % time
			
		return text