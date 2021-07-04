from screen import myApplicationManager
from runner import Runner
from os import path
from os import getcwd
from os import listdir
from os import mkdir

global GlobalrunnersDict
GlobalrunnersDict = {}


"""
Must:

need to update checkboxes for delete times and goals after deletion
deleting times not working

"""

"""
May:

make to delete and times in order

update help menus

clear input boxes after use

change screens after saving events

"""

"""
Stetch:

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
	for runner in getRunners():		
		GlobalrunnersDict[runner] = Runner(runner)

def getRunners():
	return listdir("%s/Runners" % getcwd())

if __name__ == "__main__":
	main()