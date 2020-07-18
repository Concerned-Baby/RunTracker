from os import path
from os import mkdir
from os import getcwd
from os import listdir
from runner import Runner
from platform import system
import re
import tkinter

global GlobalrunnersDict
global Globalrunners
Globalrunners = []
GlobalrunnersDict = {}

"""
Next Steps:

GUI

"""

def main():
	setUpDictionary()
	menu()
	

def start():
	try:
		mkdir("Runners")
	except OSError:
		print ("Error Creating Directory")

		
def menu():
	work = givenInput("Pick A Operation", ["get info", "write info", "get local best"])

	if (work == "get info"):
		person = givenInput("Who: ", getRunnersWithBack())
		if person != "(Back)":
			what = givenInput("What: ", ["get all info", "get info event", "(Back)"]) #need back
			if what == "(Back)":
				menu()
			elif what == "get all info":
				GlobalrunnersDict[person].printAllInfo()
			elif what == "get info event":
				event = givenInput("What Event: ", GlobalrunnersDict[person].getEvents())
				GlobalrunnersDict[person].printAllInfoEvent(event)
			else:
				print ("Error Occured, Press \Crtl + C to Exit")
		else:
			menu()
		
	elif (work == "write info"):
		person = givenInput("Who: ", getRunnersWithNew())
		if (person == "(new)"):
			name = anyInput("What's Their Name: ")
			anon = Runner(name)
			setUpDictionary()
		elif (person != "(Back)"):
			what = givenInput("What: ", ["new goal", "new time", "new event", "(Back)"]) #need bak
			if what == "(Back)":
				menu()
			elif what == "new goal":
				event = givenInput("What Event: ", GlobalrunnersDict[person].getEvents())
				time = anyTimeInput("What Time: ")
				GlobalrunnersDict[person].newGoal(event, time)
			elif what == "new time":
				event = givenInput("What Event: ", GlobalrunnersDict[person].getEvents())
				time = anyTimeInput("What Time: ")
				GlobalrunnersDict[person].newTime(event, time)
			elif what == "new event":
				event = anyInput("What Event: ")
				GlobalrunnersDict[person].newEvent(event)
			else:
				print ("Error Occured, Press \Crtl + C to Exit")
		elif (person == "(Back)"):
			menu()
		else:
			print ("Error Occured, Press \Crtl + C to Exit")

	elif (work == "get local best"):
		event = givenInput("What Event", getAllEvents(GlobalrunnersDict))
		getLocalBest(event, GlobalrunnersDict)

	else:
		print ("Error Occured, Press \Crtl + C to Exit")


def getRunnersNoTxt():
	system_ = system()
	if (system_ == "Windows" or system_ == "Android" or system_ == "Linux"):
		location = "%s\\Runners" % getcwd()
	elif (system_ == "macOS" or system_ == "iOS"):
		location = "%s/Runners" % getcwd()
	else:
		print ("Error: Platform Not Supported")
		exit()
	runners = listdir(location)
	copy = []
	for runner in runners:
		if (runner != "(Back)"):
			copy.append(runner.replace(".txt", ""))
	return copy

def getRunnersWithBack():
	runners = getRunnersNoTxt()
	runners.append("(Back)")
	return runners

def getRunnersWithNew():
	runners = getRunnersWithBack()
	runners.append("(new)")
	return runners

def anyInput(text):
	answer = input(text)
	return answer

def anyTimeInput(text):
	answer = input(text)
	return float(answer)

def givenInput(text, answers):
	question = text + " |" + str(answers).replace("[", "(").replace("]", ")").replace(",", " ") + ": "
	answer = input(question)
	answer = closest(answer, answers)
	while (not answer in answers):
		answer = input("Input Not Understood, Please Try Again\n % s" % question)
		answer = closest(answer, answers)
	return answer

def closest(text, answers):
	checkText = removeWSC(text)
	for answer in answers:
		if removeWSC(answer) == checkText:
			return answer
	return text

def removeWSC(text):
	pattern = re.compile("\s+")
	text = re.sub(pattern, "", text).lower()
	return text

def setUpDictionary():
	Globalrunners = getRunnersNoTxt()
	for runner in Globalrunners:
			GlobalrunnersDict[runner] = Runner(runner)

def getAllEvents(runnersDict=GlobalrunnersDict):
	events = []
	for runner in runnersDict:
		rEvents = runnersDict[runner].getEvents()
		for event in rEvents:
			if event not in events:
				events.append(event)
	return events

def getLocalBest(eventName, runnersDict=GlobalrunnersDict):
	best = 1000
	bestMan = "N/A"
	for runner in runnersDict:
		if runnersDict[runner].hasEvent(eventName):
			pr = runnersDict[runner].getPREvent(eventName)
			if (pr <= best):
				best = pr
				bestMan = runner
	if best == 1000:
		print("\nBest %s Run: N/A" % eventName)
		print("Best %s Runner: N/A" % eventName)
	else:
		print ("\nBest %s Run: %.2f" % (eventName, best))
		print ("Best %s Runner: %s" % (eventName, bestMan))

if __name__ == "__main__":
	if (not path.exists("Runners")):
		start()
	main()