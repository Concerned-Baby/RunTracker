from os import path
from os import mkdir
from os import getcwd
from os import listdir
from runner import Runner
from platform import system

import re
import tkinter as tk

global GlobalrunnersDict
GlobalrunnersDict = {}

"""
Next Steps:

GUI
redo the few get() methods in main, so that they return, not print
Make a global list of all events, and make sure no strange events are added

"""


def main():
	if (not path.exists("Runners")):
		start()
	setUpDictionary()
	window()
	

def start():
	try:
		mkdir("Runners")
	except OSError:
		print ("Error Creating Directory")

def window():
	screen = myApplicationManager()
	screen.start()


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
	for runner in getRunnersNoTxt():
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

def getAllLocalBests():
	pass


class myApplicationManager(object):
	def __init__(self):
		self.window = tk.Tk()
		self.window.resizable(False, False)
		self.window.title("something else")

		self.setMenu()
		self.setBest()
		self.setSelect()
		self.setHelpSelect()
		self.setHelpMenu()
		self.setHelpBest()
		self.addMenu()

	def test(self):
		pass

	def toDo(self):
		print("TODO")

	def setMenu(self):
		self.frm_menu = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_menu_logo = tk.Label(master=self.frm_menu, text="Menu")
		self.lbl_menu_logo.place(x=370, y=0)

		self.btn_menu_help = tk.Button(master=self.frm_menu, text="Help", command=self.menu_help, width=5, height=1, borderwidth=3, relief="raised")
		self.btn_menu_help.place(x=745, y=5)

		self.btn_menu_getBest = tk.Button(master=self.frm_menu, text="View Local Bests", command=self.menu_getBest, width=24, height=4, borderwidth=4, relief="raised")
		self.btn_menu_getBest.place(x=300, y=230)

		self.btn_menu_selectRunner = tk.Button(master=self.frm_menu, text="Select Runner", command=self.menu_selectRunner, width=24, height=4, borderwidth=4, relief="raised")
		self.btn_menu_selectRunner.place(x=300,y=150)

		self.btn_menu_quit = tk.Button(master=self.frm_menu, text="X", fg="red", command=self.out, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_menu_quit.place(x=5, y=415)

	def setBest(self):
		self.frm_best = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_best_logo = tk.Label(master=self.frm_best, text="Local Bests")
		self.lbl_best_logo.place(x=360, y=0)

		self.btn_best_help = tk.Button(master=self.frm_best, text="Help", command=self.best_help, width=5, height=1, borderwidth=3, relief="raised")
		self.btn_best_help.place(x=745, y=5)

		self.lbl_best_bestDistance = tk.Label(master=self.frm_best, text=getAllLocalBests(), width=30, height=27, borderwidth=4, relief="groove")
		self.lbl_best_bestDistance.place(x=36, y=20)

		self.lbl_best_bestSprints = tk.Label(master=self.frm_best, text=getAllLocalBests(), width=30, height=27, borderwidth=4, relief="groove")
		self.lbl_best_bestSprints.place(x=280, y=20)

		self.lbl_best_bestField = tk.Label(master=self.frm_best, text=getAllLocalBests(), width=30, height=27, borderwidth=4, relief="groove")
		self.lbl_best_bestField.place(x=524, y=20)



		self.btn_best_back = tk.Button(master=self.frm_best, text="B", fg="green", command=self.best_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_best_back.place(x=5, y=415)


	def setSelect(self):
		self.frm_select = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_select_logo = tk.Label(master=self.frm_select, text="Select Runner")
		self.lbl_select_logo.place(x=360, y=0)

		self.frm_select_boxOne = tk.Frame(master=self.frm_select, height=360, width=300,  borderwidth=4, relief="sunken")
		self.frm_select_boxOne.place(x=60, y=42)

		self.frm_select_boxTwo = tk.Frame(master=self.frm_select, height=360, width=300,  borderwidth=4, relief="sunken")
		self.frm_select_boxTwo.place(x=440, y=42)

		self.btn_select_help = tk.Button(master=self.frm_select, text="Help", command=self.select_help, width=5, height=1, borderwidth=3, relief="raised")
		self.btn_select_help.place(x=745, y=5)

		self.btn_select_back = tk.Button(master=self.frm_select, text="B", fg="green", command=self.select_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_select_back.place(x=5, y=415)

	def setHelpMenu(self):
		self.frm_menuHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_menuHelp_logo = tk.Label(master=self.frm_menuHelp, text="Menu Help")
		self.lbl_menuHelp_logo.place(x=370, y=0)

		self.lbl_menuHelp_text = tk.Label(master=self.frm_menuHelp, text="Here's Some Help", height=25, width=81, borderwidth=3, relief="ridge")
		self.lbl_menuHelp_text.place(x=100, y=32)

		self.btn_menuHelp_back = tk.Button(master=self.frm_menuHelp, text="B", fg="green", command=self.menuHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_menuHelp_back.place(x=5, y=415)

	def setHelpSelect(self):
		self.frm_selectHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_selectHelp_logo = tk.Label(master=self.frm_selectHelp, text="Select Help")
		self.lbl_selectHelp_logo.place(x=365, y=0)

		self.lbl_selectHelp_text = tk.Label(master=self.frm_selectHelp, text="Here's Some Help", height=25, width=81, borderwidth=3, relief="ridge")
		self.lbl_selectHelp_text.place(x=100, y=32)

		self.btn_selectHelp_back = tk.Button(master=self.frm_selectHelp, text="B", fg="green", command=self.selectHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_selectHelp_back.place(x=5, y=415)

	def setHelpBest(self):
		self.frm_bestHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_bestHelp_logo = tk.Label(master=self.frm_bestHelp, text="Best Help")
		self.lbl_bestHelp_logo.place(x=365, y=0)

		self.lbl_bestHelp_text = tk.Label(master=self.frm_bestHelp, text="Here's Some Help", height=25, width=81, borderwidth=3, relief="ridge")
		self.lbl_bestHelp_text.place(x=100, y=32)

		self.btn_bestHelp_back = tk.Button(master=self.frm_bestHelp, text="B", fg="green", command=self.bestHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_bestHelp_back.place(x=5, y=415)


	def out(self):
		self.window.destroy()

	def removeMenu(self):
		self.frm_menu.pack_forget()
	def addMenu(self):
		self.frm_menu.pack()
	def addBest(self):
		self.frm_best.pack()
	def removeBest(self):
		self.frm_best.pack_forget()
	def addSelect(self):
		self.frm_select.pack()
	def removeSelect(self):
		self.frm_select.pack_forget()
	def addMenuHelp(self):
		self.frm_menuHelp.pack()
	def removeMenuHelp(self):
		self.frm_menuHelp.pack_forget()
	def addBestHelp(self):
		self.frm_bestHelp.pack()
	def removeBestHelp(self):
		self.frm_bestHelp.pack_forget()
	def addSelectHelp(self):
		self.frm_selectHelp.pack()
	def removeSelectHelp(self):
		self.frm_selectHelp.pack_forget()

	def menu_getBest(self):
		self.removeMenu()
		self.addBest()

	def best_back(self):
		self.removeBest()
		self.addMenu()

	def menu_selectRunner(self):
		self.removeMenu()
		self.addSelect()

	def select_back(self):
		self.removeSelect()
		self.addMenu()

	def menu_help(self):
		self.removeMenu()
		self.addMenuHelp()

	def menuHelp_back(self):
		self.removeMenuHelp()
		self.addMenu()

	def select_help(self):
		self.removeSelect()
		self.addSelectHelp()

	def selectHelp_back(self):
		self.removeSelectHelp()
		self.addSelect()

	def best_help(self):
		self.removeBest()
		self.addBestHelp()

	def bestHelp_back(self):
		self.removeBestHelp()
		self.addBest()


	def start(self):
		self.window.mainloop()


if __name__ == "__main__":
	main()
