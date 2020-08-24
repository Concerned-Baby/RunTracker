from screen import myApplicationManager
from runner import Runner
from loadingscreen import loadingScreen
from os import path
from platform import system
from os import getcwd
from os import listdir

global GlobalrunnersDict
GlobalrunnersDict = {}

def main():
	loading = None #not used for now

	if (not path.exists("Runners")):
		start()
	setUpDictionary()
	window(loading)
	print("exited")
	

def start():
	try:
		mkdir("Runners")
	except OSError:
		print ("Error Creating Directory")

def window(loading):
	screen = myApplicationManager(GlobalrunnersDict)
	screen.start()

def setUpDictionary():
	for runner in getRunnersNoTxt():
			GlobalrunnersDict[runner] = Runner(runner)

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
		copy.append(runner.replace(".txt", ""))
	return copy

if __name__ == "__main__":
	main()
