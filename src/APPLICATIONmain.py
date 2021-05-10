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
ERRORS:

need to update checkboxes for delete times and goals after deletion
deleting times not working

"""

"""
TODO:

make to delete and times in order

update help menus

clear input boxes after use

change screens after saving events

"""

"""
IDEAS:

make it connected to a website

allow for pushing and requesting from a client

better format everything

have the predictions page be based of machine learning

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
		print("Error: Your Computer Is Not Supported")
		exit()
	return listdir(location)

if __name__ == "__main__":
	main()