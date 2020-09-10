from runner import Runner
from os import getcwd
from os import listdir
from os import path
from os import mkdir
from translateOut import translateOut
from translateOut import makeMenu
from platform import system

"""

add <section> tag 

"""

changeD = (system() == "macOS" or system() == "iOS")

def main():
	if (not path.exists("HTML Pages")):
			try:
				mkdir("HTML Pages")
			except OSError:
				print ("Error Creating Directory")
	runners = getRunnersNoTxt()
	makeMenu(runners)
	for runner in runners:
		print(runner)
		translateOut(Runner(runner))


	print("called")



def getRunnersNoTxt():
	system_ = system()
	if (not changeD):
		location = "%s\\Runners" % getcwd()
	else:
		location = "%s/Runners" % getcwd()
	runners = listdir(location)
	copy = []
	for runner in runners:
		copy.append(runner.replace(".txt", ""))
	return copy

if __name__ == "__main__":
	main()