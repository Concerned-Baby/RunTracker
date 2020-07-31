from os import path
from re import match
from platform import system

#print
global changeD
changeD = (system() == "macOS" or system() == "iOS")

def writeToFile(name, text):
	if changeD:
		myFile = open("Runners/%s.txt" % name, "a")
	else:
		myFile = open("Runners\\%s.txt" % name, "a")
	myFile.write(text)
	myFile.close()

def readFileLBL(name):
	if changeD:
		myFile = open("Runners/%s.txt" % name, "r")
	else:
		myFile = open("Runners\\%s.txt" % name, "r")
	lines = myFile.readlines()
	myFile.close()
	return lines

class Runner (object):
	def __init__(self, name):
		self.name = name 
		if changeD:
			if not path.exists("Runners/%s.txt" % self.name):
				open("Runners/%s.txt" % self.name, "x").close()
		else:
			if not path.exists("Runners\\%s.txt" % self.name):
				open("Runners\\%s.txt" % self.name, "x").close()


	def newEvent(self, eventName):
		if (self.hasEvent(eventName)):
			return("Event Already Added")
		writeToFile(self.name, "\n|E %s\n" % eventName)
		return("Event Added")

	def removeEvent(self, eventName):
		lines = readFileLBL(self.name)
		#print(eventName)
		toRemove = "|E %s" % eventName
		#print (toRemove)
		if (changeD):
			f = open("Runners/%s.txt" % self.name, "w")
		else:
			f = open("Runners\\%s.txt" % self.name, "w")
		f.write("z")
		for line in lines:
			if (line.strip("\n") != toRemove):
				f.write(line)
				#print (line + "z")
			else:
				#print("skipped")
				pass

	def newTime(self, eventName, time):
		if (self.hasEvent(eventName)):
			if ("%.2f" % time) not in self.getTimesEvent(eventName):
				writeToFile(self.name, "|R %s: %.2f\n" % (eventName, time))
				return("Time Added")
			else:
				return "Time Already Exists"
		return("No Such Event")

	def newGoal(self, eventName, goal):
		if (self.hasEvent(eventName)):
			if (("%.2f" % goal) not in self.getGoalsEvent(eventName)):
				writeToFile(self.name, "|G %s: %.2f\n" % (eventName, goal))
				return("Goal Added")
			return("Goal Already Exists")
		return("No Such Event")

	def hasEvent(self, eventName):
		if (eventName not in self.getEvents()):
			return False
		return True

	def getEvents(self):
		lines = readFileLBL(self.name)
		events = []
		for line in lines:
			matchObj = match("^\|E (.*)", line)
			if (matchObj):
				events.append(matchObj.group(1))
		events.sort()
		return events

	def getGoalsEvent(self, eventName):
		lines = readFileLBL(self.name)
		goals = []
		for line in lines:
			matchObj = match("^\|G (.*): (.*)", line)
			if (matchObj and matchObj.group(1) == eventName):
				goals.append(matchObj.group(2))
		return goals

	def getTimesEvent(self, eventName):
		lines = readFileLBL(self.name)
		times = []
		for line in lines:
			matchObj = match("^\|R (.*): (.*)", line)
			if (matchObj and eventName == matchObj.group(1)):
				times.append(matchObj.group(2))
		return times

	def getPREvent(self, eventName):
		times = self.getTimesEvent(eventName)
		if (len(times) == 0):
			return 1000
		PR =  1000
		for time in times:
			PR = min(PR, float(time))
		return PR

	def getGoalsPassedEvent(self, eventName):
		PR = self.getPREvent(eventName)
		goals  = self.getGoalsEvent(eventName)
		passed = 0
		for goal in goals:
			if PR <= float(goal):
				passed += 1
		return passed

	def getAllGoalsPassed(self):
		goalsPassed = 0
		events = self.getEvents()
		print (events)
		for event in events:
			goalsPassed += self.getGoalsPassedEvent(event)
		return goalsPassed

	def getAveragePoints(self):
		points = self.getTotalPoints()
		return points / len(self.getEvents())

	def getTotalPoints(self):
		points = 0
		events = self.getEvents()
		for event in events:
			points += self.getPointsEvent(event)
		return points

	def calculatePoints(self, a, b, c, time):
		score =  (a * pow((b - time), c))
		return max(score, 0)

	def getPointsEvent(self, event):
		if (event == "100m"):
			return self.calculatePoints(25.43471, 18, 1.81, self.getPREvent("100m"))
		elif (event == "200m"):
			return self.calculatePoints(3.32725, 42.5, 1.81, self.getPREvent("200m"))
		elif (event == "300m"):
			return self.calculatePoints(2.34152, 61, 1.81, self.getPREvent("300m"))
		elif (event == "400m"):
			return self.calculatePoints(1.53775, 82, 1.81, self.getPREvent("400m"))
		elif (event == "800m"):
			return self.calculatePoints(0.07462, 254, 1.88, self.getPREvent("800m"))
		elif (event == "1600m"):
			return self.calculatePoints(0.029828, 512, 1.85, self.getPREvent("1600m"))
		return 0

	def getAllPoints(self):
		events = self.getEvents()
		text = ""
		for event in events:
			text += "%s: %d\n" % (event, self.getPointsEvent(event))
		return text




	def getAllInfoEvent(self, eventName):
		toPrint = ""
		pr = self.getPREvent(eventName)
		if (pr != 1000):
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
			toPrint += time + "\n"
		return toPrint







