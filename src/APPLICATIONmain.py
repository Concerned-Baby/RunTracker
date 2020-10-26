from screen import myApplicationManager
from runner import Runner
from loadingscreen import loadingScreen
from os import path
from platform import system
from os import getcwd
from os import listdir
from os import mkdir

global GlobalrunnersDict
GlobalrunnersDict = {}

"""
fix everything for field events

add formating for enterting times

add units

update help menus

create delete times option using scrollbar and 

clean up remove option (trashed)

"""


def main():

	if not path.exists("Runners"):
		try:
			mkdir("Runners")
		except OSError:
			print ("Error Creating Directory")
	setUpDictionary()
	window()
	print("exited")
	

def window():
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
