from os import path
from re import match
from platform import system

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
			print("Event Already Added")
		else:
			writeToFile(self.name, "|E %s\n" % eventName)
			print("Event Added")

	def newTime(self, eventName, time):
		if (self.hasEvent(eventName)):
			writeToFile(self.name, "|R %s: %.2f\n" % (eventName, time))
			print("Time Added")
		else:
			print("No Such Event")

	def newGoal(self, eventName, goal):
		if (self.hasEvent(eventName)):
			if (("%.2f" % goal) not in self.getGoalsEvent(eventName)):
				writeToFile(self.name, "|G %s: %.2f\n" % (eventName, goal))
				print("Goal Added")
			else:
				print("Goal Already Exists")
		else:
			print("No Such Event")

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

	def printAllInfoEvent(self, eventName):
		print("------------------------------------------")
		print ("%s's %s Info\n" % (self.name, eventName))
		pr = self.getPREvent(eventName)
		if (pr != 1000):
			print ("PR: %.2f\n" % pr)
		else:
			print ("PR: N/A")
		goals = self.getGoalsEvent(eventName)
		passed = self.getGoalsPassedEvent(eventName)
		print ("Goals: %d        Passed: %d\n" % (len(goals), passed))
		for goal in goals:
			print(goal)
		times = self.getTimesEvent(eventName)
		print ("\nTimes: %d" % len(times))
		for time in times:
			print (time)
		print("------------------------------------------")

	def printAllInfo(self):
		print("----------------------------------------------------")
		print ("%s's Info\n\n\nPRs:\n" % self.name, end = '')
		events = self.getEvents()
		goalsPassed = 0
		goals = 0
		for event in events:
			pr = self.getPREvent(event)
			if (pr != 1000):
				print("%s: %.2f\t" % (event, pr))
			else:
				print ("%s: N/A\t" % event)
			goalsPassed += self.getGoalsPassedEvent(event)
			#print self.getGoalsPassedEvent(event)
			goals += len(self.getGoalsEvent(event))
		print("\n\n# of Goals: %d \n# of Goals Passed: %d\n" % (goals, goalsPassed))
		for event in events:
			self.printAllInfoEvent(event)
		print("----------------------------------------------------")






