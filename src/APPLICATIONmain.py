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
add formating for enterting times

add needed help menues

update help menus

remove goals option

"""


def main():

	if not path.exists("Runners"):
		try:
			mkdir("Runners")
		except OSError:
			print ("Error Creating Directory")
	setUpDictionary()
	window()

def window():
	myApplicationManager(GlobalrunnersDict).start()

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
	print(listdir(location))
	return [runner for runner in listdir(location)]

if __name__ == "__main__":
	main()
