from screen import myApplicationManager
from runner import Runner
from os import path
from os import getcwd
from os import listdir
from os import mkdir

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
Stretch:

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
	runnersDict = {}
	for runner in listdir("%s/Runners" % getcwd()):	
		GlobalrunnersDict[runner] = Runner(runner)
	myApplicationManager(GlobalrunnersDict).start()

if __name__ == "__main__":
	main()