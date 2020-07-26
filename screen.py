from runner import Runner
from frame import Frame
from stack import frameStack
import longtext
import tkinter as tk
from tkinter import ttk


"""
Next Steps:

set all frames to my custom frame

CheckBox For choosing events (under runner)
(use a line in the middle, to properly center thigns)

advanced statistics screen (with custom measurements)

if space, a full predictor for each event in the runner page (probs going to be pretty hard)
also if space picture

!!! Once Done With Beta Release, Redo Writing Organization, To Be More Efficient!!!
Organization Should Be
-Runners (Folder)
	-<Runner Name> (Folder)
		-<Event Name> (Folder)
			-<Information Type [goal, time]> (.txt file)
going to require a lot of reworking of the runner class

throw in the .sort method in runner

work with null to decrease memory usage

make runner page set only the things that change

use stacks to go back between screens (ahhh, its such a good idea, and just have a single method that moves with two parameters, the to remove, and the to add)
	stack should remove all back methods
	also should have methods that call the anyAdd method
slelct screen, make sure something is selected

add runner screen
clean up
start with a loading screen

"""

#constants
global possiblePredictions, possibleEvents, Sprints, Distance, Other
possiblePredictions = ["100m --> 200m [Best]", "200m --> 400m [Best]"]
Sprints = ["100m", "200m", "400m"]
Distance = ["800m", "1600m", "3200m"]
Other = ["Long Jump"]
Events = Sprints + Distance + Other


def getLocalBest(eventName, runnersDict):
	best = 1000
	bestMan = "N/A"
	for runner in runnersDict:
		if runnersDict[runner].hasEvent(eventName):
			pr = runnersDict[runner].getPREvent(eventName)
			if (pr <= best):
				best = pr
				bestMan = runner
	if best == 1000:
		return("\nBest %s: N/A \nBest %s'er: N/A" % (eventName, eventName))
	else:
		return ("\nBest %s: %.2f\nBest %s'er: %s" % (eventName, best, eventName, bestMan))

def getLocalBestGroup(events, runnersDict):
	text = ""
	for event in events:
		text += getLocalBest(event, runnersDict)
		text += "\n\n"
	return text

class myApplicationManager(object):
	def __init__(self, runnersDict, loading):
		self.runnersDict = runnersDict
		self.runnersList = []
		for runner in self.runnersDict:
			self.runnersList.append(runner)
		self.window = tk.Tk()
		self.window.resizable(False, False)
		self.window.title("something else")

		self.setScreens()

		self.stack = frameStack()
		self.stack.push(self.frm_menu)
		print (self.stack.toString())

		

		loading.close()

		self.frm_menu.pack()

	def test(self):
		pass

	def toDo(self):
		print("TODO")

	def setScreens(self):
		self.setMenu()
		self.setBest()
		self.setSelect()
		self.setPredictor()
		self.setHelpSelect()
		self.setHelpMenu()
		self.setHelpBest()
		self.setHelpPredictor()
		self.setRunnerHelp()
		self.setEditGoals()
		self.setEditEvents()
		self.setEditTimes()
		self.setEditGoalsHelp()
		self.setEditEventsHelp()
		self.setEditTimesHelp()
		


	"""
	Methods That Actually Do Something
	"""

	def start(self):
		self.window.mainloop()

		
	def out(self):
		self.window.destroy()

	def predictor_go(self):
		index = self.cbb_predictor_selector.current()
		if (index == -1):
			self.lbl_predictor_output["text"] = "Select"
		else:
			time = self.predictorTime.get()
			if (time == ""):
				self.lbl_predictor_output["text"] = "Enter"
			else:
				if (index == 0): #100 --> 200
					self.lbl_predictor_output["text"] = ("%.2f" % ((float(time) * 2.06) - 0.98))
				if (index == 1): #200 --> 400
					self.lbl_predictor_output["text"] = ("%.2f" % ((float(time) * 2.12) + 1.35))

	def editGoals_go(self):
		index = self.cbb_editGoals_events.get()
		print(index)
		if (index == ""):
			self.lbl_editGoals_output["text"] = "Select A Event"
		else:
			time = self.goalTime.get()
			if (time == ""):
				self.lbl_editGoals_output["text"] = "Enter A Time"
			else:
				result = self.runnersDict[self.runner].newGoal(index, float(time))
				if result == "Goal Added":
					if (self.lbl_editGoals_output["text"][0:5] == "Added"):
						self.lbl_editGoals_output["text"] = self.lbl_editGoals_output["text"] + "!"
					else:
						self.lbl_editGoals_output["text"] = "Added"
				else:
					self.lbl_editGoals_output["text"] = result

	def editTimes_go(self):
		index = self.cbb_editTimes_events.get()
		if (index == ""):
			self.lbl_editTimes_output["text"] = "Select A Event"
		else:
			time = self.ranTime.get()
			if (time == ""):
				self.lbl_editGoals_output["text"] = "Enter A Time"
			else:
				result = self.runnersDict[self.runner].newTime(index, float(time))
				if (result == "Time Added"):
					text = self.lbl_editTimes_output["text"]
					if (text[0:5] == "Added"):
						self.lbl_editTimes_output["text"] = text + "!"
					else:
						self.lbl_editTimes_output["text"] = "Added"
				else:
					self.lbl_editTimes_output["text"]  = result
		print("GO")



	def cbb_runner_event(self, runner, event):
		print (str(runner))
		self.lbl_runner_eventInfo["text"] = self.runnersDict[runner].getAllInfoEvent(event)
		print("event picked")

	def isFloat(self, toBe):
		if toBe == "":
			return True
		try:
			num = float(toBe)
			return True
		except ValueError:
			return False

	def getAllPrs(self, runner):
		runnerObj = self.runnersDict[runner]
		events = runnerObj.getEvents()
		text = ""
		for event in events:
			PR = runnerObj.getPREvent(event)
			if PR == 1000:
				text += ("%s:  N/A\n\n" % (event))
			else:
				text += ("%s:  %.2f\n\n" % (event, PR))
		return text

	def getAllGoals(self, runner):
		runnerObj = self.runnersDict[runner]
		events = runnerObj.getEvents()

		text = ""
		for event in events:
			text += ("\n%s: \n" % (event))
			goals = runnerObj.getGoalsEvent(event)
			if goals == []:
				text += "N/A\n"
			else:
				goals.sort()
				for goal in goals:
					text += ("-%s\n" % (goal))
		return text

	

	def editEvents_save(self):
		print("save")
		runnerObj = self.runnersDict[self.runner]
		events = runnerObj.getEvents()
		for checkBox in self.checkList:
			event = checkBox["text"]
			if (checkBox.instate(["selected"])):
				if event not in events:
					print ("added")
					runnerObj.newEvent(event)
			elif (checkBox.instate(["!selected"])):
				print ("not selected")
				if event in events:
					print ("removed")
					runnerObj.removeEvent(event)

	def runner_addTime(self):
		self.cbb_editTimes_events["values"] = self.runnersDict[self.runner].getEvents()
		self.goToScreen(self.frm_editTimes)

	def runner_addGoal(self):
		self.cbb_editGoals_events["values"] = self.runnersDict[self.runner].getEvents()
		self.goToScreen(self.frm_editGoals)


	def editGoals_back(self):
		#self.setRunnerPage(self.runner)
		self.updateRunner()
		self.back()

	def editTimes_back(self):
		#self.setRunnerPage(self.runner)
		self.updateRunner()
		self.back()

	def editEvents_back(self):
		#self.setRunnerPage(self.runner)
		self.updateRunner()
		self.back()

	def select_go(self):
		runner = self.cbb_select_selector.current()
		self.setRunnerPage(self.runnersList[runner])
		self.goToScreen(self.frm_runner)

	def runner_addEvent(self):
		events = self.runnersDict[self.runner].getEvents()
		for checkBox in self.checkList:
			event = checkBox["text"]
			if (event in events):
				if (not checkBox.instate(["selected"])):
					checkBox.state(["selected"])
			else:
				checkBox.state(['!selected'])

		self.goToScreen(self.frm_editEvents)
		





	"""
	Method That Change Screens (Also Updates A Few)
	"""

	def goToScreen(self, frame):
		self.stack.getTop().pack_forget()
		self.stack.push(frame).pack()
		print(self.stack.toString())

	def back(self):
		self.stack.pop().pack_forget()
		self.stack.getTop().pack()
		print(self.stack.toString())

	def menu_getBest(self):
		self.goToScreen(self.frm_best)

	def best_back(self):
		self.back()

	def menu_selectRunner(self):
		self.goToScreen(self.frm_select)

	def select_back(self):
		self.back()

	def menu_predictor(self):
		self.goToScreen(self.frm_predictor)

	def predictor_back(self):
		self.back()

	def menu_help(self):
		self.goToScreen(self.menu_help)

	def menuHelp_back(self):
		self.back()

	def select_help(self):
		self.goToScreen(self.frm_selectHelp)

	def selectHelp_back(self):
		self.back()

	def best_help(self):
		self.goToScreen(self.frm_bestHelp)

	def bestHelp_back(self):
		self.back()

	def predictor_help(self):
		self.goToScreen(self.frm_predictorHelp)

	def predictorHelp_back(self):
		self.back()

	def runner_back(self):
		self.back()

	def runner_help(self):
		self.goToScreen(self.frm_runnerHelp)

	def runnerHelp_back(self):
		self.back()

	def editGoals_help(self):
		self.goToScreen(self.frm_editGoalsHelp)

	def editTimes_help(self):
		self.goToScreen(self.frm_editTimesHelp)

	def editEvents_help(self):
		self.goToScreen(self.frm_editEventsHelp)

	def editEventsHelp_back(self): #its not updating after going back, need to fix it
		self.back()

	def editTimesHelp_back(self):
		self.back()

	def editGoalsHelp_back(self):
		self.back()



	"""
	Setting Screens
	"""

	def setMenu(self):
		self.frm_menu = Frame(self.window, "Menu")

		lbl_menu_logo = tk.Label(master=self.frm_menu, text="Menu")
		lbl_menu_logo.place(x=370, y=0)

		btn_menu_help = tk.Button(master=self.frm_menu, text="Help", command=self.menu_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_menu_help.place(x=745, y=5)

		btn_menu_getBest = tk.Button(master=self.frm_menu, text="View Local Bests", command=self.menu_getBest, width=24, height=4, borderwidth=4, relief="raised")
		btn_menu_getBest.place(x=300, y=210)

		btn_menu_selectRunner = tk.Button(master=self.frm_menu, text="Select Runner", command=self.menu_selectRunner, width=24, height=4, borderwidth=4, relief="raised")
		btn_menu_selectRunner.place(x=300,y=130)

		btn_menu_predictors = tk.Button(master=self.frm_menu, text="Predictor (Beta)", command=self.menu_predictor, width=24, height=4, borderwidth=4, relief="raised")
		btn_menu_predictors.place(x=300, y=290)

		btn_menu_quit = tk.Button(master=self.frm_menu, text="X", fg="red", command=self.out, width=2,height=1, borderwidth=3, relief="raised")
		btn_menu_quit.place(x=5, y=415)

	def setBest(self):
		self.frm_best = Frame(self.window, "Best")

		lbl_best_logo = tk.Label(master=self.frm_best, text="Local Bests")
		lbl_best_logo.place(x=360, y=0)

		btn_best_help = tk.Button(master=self.frm_best, text="Help", command=self.best_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_best_help.place(x=745, y=5)

		lbl_best_bestDistance = tk.Label(master=self.frm_best, text=getLocalBestGroup(Distance, self.runnersDict), width=30, height=27, borderwidth=4, relief="groove")
		lbl_best_bestDistance.place(x=36, y=20)

		lbl_best_bestSprints = tk.Label(master=self.frm_best, text=getLocalBestGroup(Sprints, self.runnersDict), width=30, height=27, borderwidth=4, relief="groove")
		lbl_best_bestSprints.place(x=280, y=20)

		lbl_best_bestField = tk.Label(master=self.frm_best, text=getLocalBestGroup(Other, self.runnersDict), width=30, height=27, borderwidth=4, relief="groove")
		lbl_best_bestField.place(x=524, y=20)

		btn_best_back = tk.Button(master=self.frm_best, text="B", fg="green", command=self.best_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_best_back.place(x=5, y=415)

	def setPredictor(self):
		self.frm_predictor = Frame(self.window, "Predictor")

		lbl_predictor_logo = tk.Label(master=self.frm_predictor, text="Predictors")
		lbl_predictor_logo.place(x=370, y=0)

		self.cbb_predictor_selector = ttk.Combobox(master=self.frm_predictor, values=possiblePredictions, state="readonly", width=40)
		self.cbb_predictor_selector.place(x=270, y=90)

		lbl_predictor_entryLabel = tk.Label(master=self.frm_predictor, text="      Time      ", borderwidth=1, relief="solid")
		lbl_predictor_entryLabel.place(x=365, y=160)

		self.predictorTime = tk.StringVar()
		self.vcmd = (self.window.register(self.isFloat), "%P") #research register command
		
		self.ent_predictor_entry = tk.Entry(master=self.frm_predictor, width=15, textvariable=self.predictorTime, validate="all", validatecommand=self.vcmd)
		self.ent_predictor_entry.place(x=350, y=190)

		lbl_predictor_arrow = tk.Label(master=self.frm_predictor, text="⬇️")
		lbl_predictor_arrow.place(x=390, y=220)

		self.lbl_predictor_output = tk.Label(master=self.frm_predictor, text="0.0", borderwidth=3, relief="sunken", width=10, height=1)
		self.lbl_predictor_output.place(x=360, y=250)

		btn_predictor_go = tk.Button(master=self.frm_predictor, text="GO!", command=self.predictor_go, borderwidth=3, relief="raised", width=10, height=1)
		btn_predictor_go.place(x=357, y=290)

		btn_best_help = tk.Button(master=self.frm_predictor, text="Help", command=self.predictor_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_best_help.place(x=745, y=5)

		btn_predictor_back = tk.Button(master=self.frm_predictor, text="B", fg="green", command=self.predictor_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_predictor_back.place(x=5, y=415)

	def setSelect(self):
		self.frm_select = Frame(self.window, "Select")

		lbl_select_logo = tk.Label(master=self.frm_select, text="Select Runner")
		lbl_select_logo.place(x=360, y=0)
		
		self.cbb_select_selector = ttk.Combobox(master=self.frm_select, values=self.runnersList, state="readonly", width=40)
		self.cbb_select_selector.place(x=275, y=120)

		btn_select_help = tk.Button(master=self.frm_select, text="Help", command=self.select_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_select_help.place(x=745, y=5)

		btn_select_go = tk.Button(master=self.frm_select, text="GO!", command=self.select_go, borderwidth=3, relief="raised", width=20, height=2)
		btn_select_go.place(x=330, y=200)


		btn_select_back = tk.Button(master=self.frm_select, text="B", fg="green", command=self.select_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_select_back.place(x=5, y=415)

	def setHelpMenu(self):
		self.frm_menuHelp = Frame(self.window, "Menu Help")

		lbl_menuHelp_logo = tk.Label(master=self.frm_menuHelp, text="Menu Help")
		lbl_menuHelp_logo.place(x=370, y=0)

		lbl_menuHelp_text = tk.Label(master=self.frm_menuHelp, text=longtext.menuHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_menuHelp_text.place(x=100, y=32)

		btn_menuHelp_back = tk.Button(master=self.frm_menuHelp, text="B", fg="green", command=self.menuHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_menuHelp_back.place(x=5, y=415)

	def setHelpSelect(self):
		self.frm_selectHelp= Frame(self.window, "Select Help")

		lbl_selectHelp_logo = tk.Label(master=self.frm_selectHelp, text="Select Help")
		lbl_selectHelp_logo.place(x=365, y=0)

		lbl_selectHelp_text = tk.Label(master=self.frm_selectHelp, text=longtext.selectHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_selectHelp_text.place(x=100, y=32)

		btn_selectHelp_back = tk.Button(master=self.frm_selectHelp, text="B", fg="green", command=self.selectHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_selectHelp_back.place(x=5, y=415)

	def setHelpBest(self):
		self.frm_bestHelp = Frame(self.window, "Best Help")

		lbl_bestHelp_logo = tk.Label(master=self.frm_bestHelp, text="Best Help")
		lbl_bestHelp_logo.place(x=365, y=0)

		lbl_bestHelp_text = tk.Label(master=self.frm_bestHelp, text=longtext.bestHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_bestHelp_text.place(x=100, y=32)

		btn_bestHelp_back = tk.Button(master=self.frm_bestHelp, text="B", fg="green", command=self.bestHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_bestHelp_back.place(x=5, y=415)

	def setHelpPredictor(self):
		self.frm_predictorHelp = Frame(self.window, "Predictor Help")

		lbl_predictorHelp_logo = tk.Label(master=self.frm_predictorHelp, text="Predictor Help")
		lbl_predictorHelp_logo.place(x=365, y=0)

		lbl_predictorHelp_text = tk.Label(master=self.frm_predictorHelp, text=longtext.predictorHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_predictorHelp_text.place(x=100, y=32)

		btn_predictorHelp_back = tk.Button(master=self.frm_predictorHelp, text="B", fg="green", command=self.predictorHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_predictorHelp_back.place(x=5, y=415)

	def setRunnerHelp(self):
		self.frm_runnerHelp = Frame(self.window, "Runner Help")

		lbl_runnerHelp_logo = tk.Label(master=self.frm_runnerHelp, text="Predictor Help")
		lbl_runnerHelp_logo.place(x=365, y=0)

		lbl_runnerHelp_text = tk.Label(master=self.frm_runnerHelp, text=longtext.runnerHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_runnerHelp_text.place(x=100, y=32)

		btn_runnerHelp_back = tk.Button(master=self.frm_runnerHelp, text="B", fg="green", command=self.runnerHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_runnerHelp_back.place(x=5, y=415)

	def setEditGoals(self):
		self.frm_editGoals = Frame(self.window, "Edit Goals")

		lbl_editGoals_logo = tk.Label(master=self.frm_editGoals, text="Add Goals")
		lbl_editGoals_logo.place(x=365, y=0)

		btn_editGoals_back = tk.Button(master=self.frm_editGoals, text="B", fg="green", command=self.editGoals_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_editGoals_back.place(x=5, y=415)

		lbl_editGoals_cbbLabel = tk.Label(master=self.frm_editGoals, text="Select Event")
		lbl_editGoals_cbbLabel.place(x=360, y=120)

		self.cbb_editGoals_events = ttk.Combobox(master=self.frm_editGoals, values=[], state="readonly")
		self.cbb_editGoals_events.place(x=330, y=140)

		lbl_editGoals_entryLabel = tk.Label(master=self.frm_editGoals, text="Enter Goal")
		lbl_editGoals_entryLabel.place(x=362, y=200)

		self.goalTime = tk.StringVar()
		self.ent_editGoals_entry = tk.Entry(master=self.frm_editGoals, width=15, textvariable=self.goalTime, validate="all", validatecommand=self.vcmd)
		self.ent_editGoals_entry.place(x=350, y=220)

		btn_editGoals_go = tk.Button(master=self.frm_editGoals, text="GO!", command=self.editGoals_go, width=8, height=1, borderwidth=3, relief="raised")
		btn_editGoals_go.place(x=360, y=270)

		self.lbl_editGoals_output = tk.Label(master=self.frm_editGoals, text="Click GO!", width=15, height=1, borderwidth=1, relief="solid")
		self.lbl_editGoals_output.place(x=340, y=320)

		btn_editGoals_help = tk.Button(master=self.frm_editGoals, text="Help", command=self.editGoals_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_editGoals_help.place(x=745, y=5)

	def setEditEvents(self):
		self.frm_editEvents = Frame(self.window, "Edit Events")

		lbl_editEvents_logo = tk.Label(master=self.frm_editEvents, text="Add Events")
		lbl_editEvents_logo.place(x=365, y=0)

		btn_editEvents_back = tk.Button(master=self.frm_editEvents, text="B", fg="green", command=self.editEvents_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_editEvents_back.place(x=5, y=415)

		btn_editEvents_help = tk.Button(master=self.frm_editEvents, text="Help", command=self.editEvents_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_editEvents_help.place(x=745, y=5)

		lbl_editEvents_sprintLogo = tk.Label(master=self.frm_editEvents, text="Sprints")
		lbl_editEvents_sprintLogo.place(x=150, y=100)

		lbl_editEvents_distanceLogo = tk.Label(master=self.frm_editEvents, text="Distance")
		lbl_editEvents_distanceLogo.place(x=350, y=100)

		lbl_editEvents_distanceLogo = tk.Label(master=self.frm_editEvents, text="Other")
		lbl_editEvents_distanceLogo.place(x=550, y=100)

		self.checkList = []
		SCount = 120
		DCount = 120
		OCount = 120
		for event in Events:
			bVar = tk.BooleanVar()
			chk = ttk.Checkbutton(master=self.frm_editEvents, text=event)
			chk.state(["!alternate"])
			self.checkList.append(chk)
			
			if event in Sprints:
				chk.place(x=150, y=SCount)
				SCount += 30
			elif event in Distance:
				chk.place(x=350, y=DCount)
				DCount += 30
			elif event in Other:
				chk.place(x=550, y=OCount)
				OCount += 30

		btn_editEvents_save = tk.Button(master=self.frm_editEvents, text="Save", command=self.editEvents_save, width=8, height=1, borderwidth=3, relief="raised")
		btn_editEvents_save.place(x=360, y=370)

	def setEditTimes(self):
		self.frm_editTimes = Frame(self.window, "Edit Times")

		lbl_editTimes_logo = tk.Label(master=self.frm_editTimes, text="Add Times")
		lbl_editTimes_logo.place(x=365, y=0)

		btn_editTimes_back = tk.Button(master=self.frm_editTimes, text="B", fg="green", command=self.editTimes_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_editTimes_back.place(x=5, y=415)

		btn_editTimes_help = tk.Button(master=self.frm_editTimes, text="Help", command=self.editTimes_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_editTimes_help.place(x=745, y=5)

		lbl_editTimes_cbbLabel = tk.Label(master=self.frm_editTimes, text="Select Event")
		lbl_editTimes_cbbLabel.place(x=360, y=120)

		self.cbb_editTimes_events = ttk.Combobox(master=self.frm_editTimes, values=[], state="readonly")
		self.cbb_editTimes_events.place(x=330, y=140)

		lbl_editTimes_entryLabel = tk.Label(master=self.frm_editTimes, text="Enter Time")
		lbl_editTimes_entryLabel.place(x=362, y=200)

		self.ranTime = tk.StringVar()
		self.ent_editTimes_entry = tk.Entry(master=self.frm_editTimes, width=15, textvariable=self.ranTime, validate="all", validatecommand=self.vcmd)
		self.ent_editTimes_entry.place(x=350, y=220)

		btn_editTimes_go = tk.Button(master=self.frm_editTimes, text="GO!", command=self.editTimes_go, width=8, height=1, borderwidth=3, relief="raised")
		btn_editTimes_go.place(x=360, y=270)

		self.lbl_editTimes_output = tk.Label(master=self.frm_editTimes, text="Click GO!", width=15, height=1, borderwidth=1, relief="solid")
		self.lbl_editTimes_output.place(x=340, y=320)

	def setEditGoalsHelp(self):
		self.frm_editGoalsHelp = Frame(self.window, "Edit Goals Help")

		lbl_editGoalsHelp_logo = tk.Label(master=self.frm_editGoalsHelp, text="Edit Goals Help")
		lbl_editGoalsHelp_logo.place(x=365, y=0)

		lbl_editGoalsHelp_text = tk.Label(master=self.frm_editGoalsHelp, text=longtext.editGoalsHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_editGoalsHelp_text.place(x=100, y=32)

		btn_editGoalsHelp_back = tk.Button(master=self.frm_editGoalsHelp, text="B", fg="green", command=self.editGoalsHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_editGoalsHelp_back.place(x=5, y=415)

	def setEditEventsHelp(self):
		self.frm_editEventsHelp = Frame(self.window, "Edit Events Help")

		lbl_editEventsHelp_logo = tk.Label(master=self.frm_editEventsHelp, text="Edit Events Help")
		lbl_editEventsHelp_logo.place(x=365, y=0)

		lbl_editEventsHelp_text = tk.Label(master=self.frm_editEventsHelp, text=longtext.editEventsHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_editEventsHelp_text.place(x=100, y=32)

		btn_editEventsHelp_back = tk.Button(master=self.frm_editEventsHelp, text="B", fg="green", command=self.editEventsHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_editEventsHelp_back.place(x=5, y=415)

	def setEditTimesHelp(self):
		self.frm_editTimesHelp = Frame(self.window, "Edit Times Help")

		lbl_editTimesHelp_logo = tk.Label(master=self.frm_editTimesHelp, text="Edit Time Help")
		lbl_editTimesHelp_logo.place(x=365, y=0)

		lbl_editTimesHelp_text = tk.Label(master=self.frm_editTimesHelp, text=longtext.editTimesHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_editTimesHelp_text.place(x=100, y=32)

		btn_editTimesHelp_back = tk.Button(master=self.frm_editTimesHelp, text="B", fg="green", command=self.editTimesHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_editTimesHelp_back.place(x=5, y=415)

	def setRunnerPage(self, runner): #might not need to have self. (if we just refresh on entry)
		self.runner = runner
		self.frm_runner = Frame(self.window, "Runner")

		self.lbl_runner_name = tk.Label(master=self.frm_runner, text=runner)
		self.lbl_runner_name.place(x=365, y=0)

		self.lbl_runner_goalsPassed = tk.Label(master=self.frm_runner, text="Total Candy Owed: %d" % self.runnersDict[runner].getAllGoalsPassed())
		self.lbl_runner_goalsPassed.place(x=450, y=40)

		btn_runner_help = tk.Button(master=self.frm_runner, text="Help", command=self.runner_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_runner_help.place(x=745, y=5)

		btn_runner_back = tk.Button(master=self.frm_runner, text="B", fg="green", command=self.runner_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_runner_back.place(x=5, y=415)

		lbl_runner_prLabel = tk.Label(master=self.frm_runner, text="PRs", width=20, height=1, borderwidth=2, relief="ridge")
		lbl_runner_prLabel.place(x=40, y=40)

		self.lbl_runner_prs = tk.Label(master=self.frm_runner, text=self.getAllPrs(runner), width=20, height=24, borderwidth=2, relief="ridge")
		self.lbl_runner_prs.place(x=40, y=60)

		lbl_runner_goalLabel = tk.Label(master=self.frm_runner, text="Goals", width=20, height=1, borderwidth=2, relief="ridge")
		lbl_runner_goalLabel.place(x=630, y=40)

		self.lbl_runner_goals = tk.Label(master=self.frm_runner, text=self.getAllGoals(runner), width=20, height=24, borderwidth=2, relief="ridge")
		self.lbl_runner_goals.place(x=630, y=60)

		btn_runner_editEvents = tk.Button(master=self.frm_runner,command=self.runner_addEvent, text="edit events", width=12, height=1, borderwidth=3, relief="raised")
		btn_runner_editEvents.place(x=210, y=415)

		btn_runner_addTime = tk.Button(master=self.frm_runner, command=self.runner_addTime, text="add time", width=12, height=1, borderwidth=3, relief="raised")
		btn_runner_addTime.place(x=360, y=415)
 
		btn_runner_addGoal = tk.Button(master=self.frm_runner, command=self.runner_addGoal, text="add goal", width=12, height=1, borderwidth=3, relief="raised")
		btn_runner_addGoal.place(x=510, y=415)

		self.cbb_runner_events = ttk.Combobox(master=self.frm_runner, state="readonly", values=self.runnersDict[runner].getEvents())#, postcommand=self.cbb_runner_event)
		self.cbb_runner_events.place(x=290, y=40)
		
		def callback(eventObject):
			self.cbb_runner_event(runner, self.cbb_runner_events.get())
		self.cbb_runner_events.bind("<<ComboboxSelected>>", callback)#lambda _ : print("Selected!"))

		self.lbl_runner_eventInfo = tk.Label(master=self.frm_runner, text="Select A Event", width=58, height=20, borderwidth=3, relief="ridge")
		self.lbl_runner_eventInfo.place(x=200, y=80)


	def updateRunner(self):
		print ("updated")
		self.lbl_runner_prs["text"] = self.getAllPrs(self.runner)
		self.lbl_runner_goals["text"] = self.getAllGoals(self.runner)
		self.lbl_runner_goalsPassed["text"] = "Total Candy Owed: %d" % self.runnersDict[self.runner].getAllGoalsPassed()
		self.cbb_runner_events["values"] = self.runnersDict[self.runner].getEvents()



