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
TODO:

add needed help menues

update help menus

remove goals option

need to update runner after deletions + additions

need to account for both string + int inputs for time/goal managing
	-use things like time = int(time)

upadte getters to allow proper typign

"""

"""
ERRORS:

"""

def main():
	if not path.exists("Runners"):
		try:
			mkdir("Runners")
		except OSError:
			print ("Error Creating Runner Directory")
	setUpDictionary()
	window()

def window():
	myApplicationManager(GlobalrunnersDict).start()

def setUpDictionary():	
	for runner in getRunnersNoTxt():		
		GlobalrunnersDict[runner] = Runner(runner)

def getRunnersNoTxt():
	system_ = system()
	if system_ == "Windows" or system_ == "Android" or system_ == "Linux":
		location = "%s\\Runners" % getcwd()
	elif system_ == "macOS" or system_ == "iOS":
		location = "%s/Runners" % getcwd()
	else:
		print("Error: Platform Not Supported")
		exit()
	return listdir(location)

if __name__ == "__main__":
	main()
