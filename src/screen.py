from runner import Runner
from frame import Frame
from stack import frameStack
import longtext
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

#constants
global possiblePredictions, possibleEvents, Sprints, Distance, Field, NoTime
possiblePredictions = ["100m --> 200m [Best]", "200m --> 400m [Best]", "300m --> 400m [Best]", "400m --> 800m [Best]"]
NoTime = 14420133764129

Sprints = ["100m", "200m", "400m"]
Distance = ["800m", "1600m", "3200m"]
Field = ["Long Jump", "Triple Jump", "Pole Vault", "Discus", "Shotput", "High Jump"]
Events = Sprints + Distance + Field

supportedSyntaxs = ["Name - Event - Time", "Event - Name - Time", "Name Event Time", "Event Name Time"]


#return String
#param String, Dictionary<String, Runner>
def getLocalBest(eventName, runnersDict):
	bestMan = "N/A"
	if eventName not in Field:
		best = NoTime
		for runner in runnersDict:
			if runnersDict[runner].hasEvent(eventName):
				pr = runnersDict[runner].getPREvent(eventName)
				if pr < best:
					best = pr
					bestMan = runner
		if best == NoTime:
			return("\nBest %s: N/A \nBest %s'er: N/A" % (eventName, eventName))
		else:
			return("\nBest %s: %s \nBest %s'er: %s" % (eventName, format(best), eventName, bestMan))
	else:
		best = 0
		for runner in runnersDict:
			if runnersDict[runner].hasEvent(eventName):
				pr = runnersDict[runner].getPREvent(eventName)
				if pr > best:
					best = pr
					bestMan = runner
		if best == 0:
			return("\nBest %s: N/A \nBest %s'er: N/A" % (eventName, eventName))
		return("\nBest %s: %.2f \nBest %s'er: %s" % (eventName, best, eventName, bestMan))
	return "ERROR LOADING TIMES"

#return String
#param double
def format(time):
	if (time < 60):
		return "%.2f" % time
	return ("%d:%2d.%2d" % (time / 60, time % 60, (time % 1) * 100)).replace(' ', "0")

#return flaot
#param String
def unformat(inp):
	try:
		num = float(inp)
		return num
	except ValueError:
		arr = inp.split(":")
		return float(arr[0]) * 60 + float(arr[1])

#return String
#param List<String>, Dictionary<String, Runner>
def getLocalBestGroup(events, runnersDict):
	text = ""
	for event in events:
		text += getLocalBest(event, runnersDict) + "\n\n"
	return text

#return String
#param String, Dictionary<String, Runner>
def getRankingsEvent(eventName, runnersDict):
	temp = {}
	for runner in runnersDict:
		if runnersDict[runner].hasEvent(eventName):
			temp[(runnersDict[runner].getPREvent(eventName))] = runner
	count = 1
	text = ""
	for time in sorted(temp.keys()):
		if time == NoTime:
			text += "%d.  %s\tN/A\n" % (count, temp[time].ljust(32)[:32])
		else:
			text += "%d.  %s\t%s\n" % (count, temp[time].ljust(32)[:32], format(time))
		count += 1
	if text == "":
		return "n/a"
	return text

def clearEntry(entry):
	entry.delete(0, 'end')


class myApplicationManager(object):
	"""
	Section: Basic Class Composition
	"""

	#return None
	#param Dictionary<String, Runner>
	def __init__(self, runnersDict):
		self.runnersDict = runnersDict
		self.runnersList = [runner for runner in self.runnersDict]
		self.window = tk.Tk()
		self.window.resizable(False, False)
		self.window.title("Run Tracker")

		self.setScreens()
		self.stack = frameStack()

		self.stack.push(self.frm_menu)
		self.frm_menu.pack()

	"""
	Section: Methods That Actually Do Something
	"""

	#return None
	#param None
	def updateRunner(self):
		events = self.runnersDict[self.runner].getEvents()
		self.lbl_runner_prs["text"] = self.getAllPrs(self.runner)
		self.cbb_runner_events["values"] = events
		self.cbb_deleteTimes_events["values"] = events
		self.cbb_deleteGoals_events["values"] = events
		self.cbb_editTimes_events["values"] = events
		self.cbb_editGoals_events["values"] = events
		self.lbl_runner_name["text"] = self.runner
		self.cbb_runner_events["values"] = events
		self.lbl_runner_goalsPassed["text"] = "Total Candy Owed: %d" % self.runnersDict[self.runner].getAllGoalsPassed()
		self.myList.delete(0, tk.END)
		for line in self.getAllGoals(self.runner).split("\n"):
			self.myList.insert(tk.END, line + "\n")
		self.myList.place(x=630, y=60)
		self.scr_runner_goals.config(command=self.myList.yview)
		self.lbl_runner_eventInfo["text"] = self.runnersDict[self.runner].getAllInfoEvent(event)


	#return None
	#param None
	def start(self):
		self.window.mainloop()

	#return None
	#param None
	def out(self):
		self.window.destroy()

	#return None
	#param None
	def predictor_go(self):
		index = self.cbb_predictor_selector.current()
		if (index == -1):
			self.lbl_predictor_output["text"] = "Select"
		else:
			time = self.predictorGivenTime
			if (time == ""):
				self.lbl_predictor_output["text"] = "Enter"
			else:
				if (index == 0): #100 --> 200
					self.lbl_predictor_output["text"] = ("%.2f" % ((float(time) * 2.06) - 0.98))
				elif (index == 1): #200 --> 400
					self.lbl_predictor_output["text"] = ("%.2f" % ((float(time) * 2.12) + 1.35))
				elif (index == 2): #300 --> 400
					self.lbl_predictor_output["text"] = ("%.2f" % ((float(time) * 1.37) + 1.23))
				elif (index == 3): #400 --> 800
					self.lbl_predictor_output["text"] = ("%.2f" % ((float(time) * 2.33) + 6.3))

	#return None
	#param None
	def editGoals_go(self):
		index = self.cbb_editGoals_events.get()
		if (index == ""):
			self.lbl_editGoals_output["text"] = "Select A Event"
		else:
			time = self.goalTime
			if (time == -1):
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
		self.updateRunner()
		#clear entry

	#return None
	#param Runner, String
	def cbb_runner_event(self, event):
		self.lbl_runner_eventInfo["text"] = self.runnersDict[self.runner].getAllInfoEvent(event)

	#return boolean
	#param String
	def isFloatTime(self, toBe):
		if toBe == "":
			self.ranTime = -1
			return True
		try:
			num = float(toBe)
			self.ranTime = num
			return True
		except ValueError:
			return False

	#return boolean
	#param String
	def isFloatGoal(self, toBe):
		if toBe == "":
			self.goalTime = -1
			return True
		try:
			num = float(toBe)
			self.goalTime = num
			return True
		except ValueError:
			return False

	#return boolean
	#param String
	def isValidRunnerName(self, toBe):
		if toBe == "":
			self.newRunnerName = ""
			return True
		if toBe.isalpha():
			self.newRunnerName = toBe
			return True
		return False		
		
	def isFloatPredictor(self, toBe):
		if toBe == "":
			self.predictorGivenTime = -1
			return True
		try:
			num = float(toBe)
			self.predictorGivenTime = num
			return True
		except ValueError:
			return False
			#clear entry

	#return String
	#param String
	def getAllPrs(self, runner):
		print(runner)
		print(self.runnersDict)
		runnerObj = self.runnersDict[runner]
		events = runnerObj.getEvents()
		text = ""
		for event in events:
			PR = runnerObj.getPREvent(event)
			if PR == NoTime:
				text += "%s:  N/A\n\n" % (event)
			else:
				text += "%s:  %s\n\n" % (event, format(PR))
		return text

	#return String
	#param String
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
					text += ("-%s\n" % (format(goal)))
		return text

	#return None
	#param None
	def editTimes_go(self):
		index = self.cbb_editTimes_events.get()
		if index == "":
			self.lbl_editTimes_output["text"] = "Select A Event"
		else:
			time = self.ranTime
			if (time == -1):
				self.lbl_editTimes_output["text"] = "Enter A Time"
			else:
				if (self.reasonableTimeTrack(index, float(time)) and index not in Field) or (self.reasonableTimeEvent(index, float(time)) and index in Field):
					result = self.runnersDict[self.runner].newTime(index, float(time))
					if (result == "Time Added"):
						text = self.lbl_editTimes_output["text"]
						if (text[0:5] == "Added"):
							self.lbl_editTimes_output["text"] = text + "!"
						else:
							self.lbl_editTimes_output["text"] = "Added"
					else:
						self.lbl_editTimes_output["text"] = result
				else:
					if self.lbl_editTimes_output["text"] == "Time is extreme, click 'GO!' again to confirm":
						result = self.runnersDict[self.runner].newTime(index, float(time))
						if (result == "Time Added"):
							text = self.lbl_editTimes_output["text"]
							if (text[0:5] == "Added"):
								self.lbl_editTimes_output["text"] = text + "!"
							else:
								self.lbl_editTimes_output["text"] = "Added"
						else:
							self.lbl_editTimes_output["text"] = result
					else:
						self.lbl_editTimes_output["text"] = "Time is extreme, click 'GO!' again to confirm"
		self.updateRunner()

	#return boolean
	#param String, double
	def reasonableTimeTrack(self, event, time):
		wrld = 0
		if event == "100m":
			wrld = 9.58
		elif event == "200m":
			wrld = 19.19
		elif event == "300m":
			wrld = 30.91
		elif event == "400m":
			wrld = 43.03
		elif event == "800m":
			wrld = 101.91
		elif event == "1600m":
			wrld = 223.13
		elif event == "3200m":
			wrld = 478.61
		return (not wrld == 0) and (time > wrld and time < (pow(wrld, 13/11) * 1.3))

	#return boolean
	#param String, double
	def reasonableTimeEvent(self, event, dist):
		wrld = 0
		if event == "Pole Vault":
			wrld = 20.18
		elif event == "Long Jump":
			wrld = 29.35
		return (not wrld == 0) and (dist < wrld and time > wrld * 0.05)
	
	#return None
	#param None
	def editEvents_save(self):
		runnerObj = self.runnersDict[self.runner]
		events = runnerObj.getEvents()
		for checkBox in self.checkList:
			event = checkBox["text"]
			if (checkBox.instate(["selected"])):
				if event not in events:
					runnerObj.newEvent(event)
			elif (checkBox.instate(["!selected"])):
				if event in events:
					runnerObj.removeEvent(event)
		self.updateRunner()

	#return None
	#param None
	def runner_addTime(self):
		self.updateRunner()
		self.goToScreen(self.frm_editTimes)

	#return None
	#param None
	def runner_addGoal(self):
		self.cbb_editGoals_events["values"] = self.runnersDict[self.runner].getEvents()
		self.goToScreen(self.frm_editGoals)

	#return None
	#param None
	def editGoals_back(self):
		self.updateRunner()
		self.back()

	#return None
	#param None
	def editTimes_back(self):
		self.updateRunner()
		self.back()

	#return None
	#param None
	def editEvents_back(self):
		self.updateRunner()
		self.back()

	#return None
	#param None
	def select_go(self):
		self.runner = self.runnersList[self.cbb_select_selector.current()] #may not be fixed
		print(self.runner)
		self.updateRunner()
		self.goToScreen(self.frm_runner)

	#return None
	#param None
	def runner_advanced(self):
		self.updateAdvanced()
		self.goToScreen(self.frm_runnerAdvanced)

	#return None
	#param None
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

	#return None
	#param None
	def updateAdvanced(self):
		self.lbl_runnerAdvanced_name["text"] = self.runner
		runnerObj = self.runnersDict[self.runner]
		self.lbl_runnerAdvanced_points["text"] = "Total Points: %d \n\n Point Efficiency: %.3f points per event" % (runnerObj.getTotalPoints(), runnerObj.getAveragePoints())
		self.lbl_runnerAdvanced_pointSEvent["text"] = runnerObj.getAllPoints()

	#return None
	#param None
	def selectNew_go(self):
		name = self.newRunnerName
		runnerObj = Runner(self.newRunnerName)
		if name not in self.runnersList:
			self.runnersList.append(name)
			self.runnersDict[name] = runnerObj
			self.cbb_select_selector["values"] = self.runnersList
		#clear entry

	#return None
	#param String
	def localRank_update(self, event):
		self.lbl_localRank_info["text"] = getRankingsEvent(Events[event], self.runnersDict)

	#return None
	#param None
	def import_update(self):
		text = self.txt_import_file.get("1.0",'end-1c')
		lines = text.split("\n")
		index = self.cbb_import_syntaxs.current()
		if index == 0: #Name - Event - Time
			for line in lines:
				arr = line.split('-')
				name = arr[0].strip()
				event = arr[1].strip()
				time = arr[2].strip()
				self.parseRunner(name, event, time)
		elif index == 1: #Event - Name - Time
			for line in lines:
				arr = line.split('-')
				event = arr[0].strip()
				name = arr[1].strip()
				time = arr[2].strip()
				self.parseRunner(name, event, time)
		elif index == 2: #Name Event Time
			for line in lines:
				arr = line.split(" ")
				name = arr[0].strip()
				event = arr[1].strip()
				time = arr[2].strip()
				self.parseRunner(name, event, time)
		elif index == 3: #Event Name Time
			for line in lines:
				arr = line.split(" ")
				event = arr[0].strip()
				name = arr[1].strip()
				time = arr[2].strip()
				self.parseRunner(name, event, time)

		self.cbb_select_selector["values"] = self.runnersList

	#return None
	#param String, String, double
	def parseRunner(self, name, event, time):
		runnerObj = Runner(name)
		if name not in self.runnersList:
			self.runnersList.append(name)
			self.runnersDict[name] = runnerObj
			runnerObj.newEvent(event)
		else:
			if event not in runnerObj.getEvents():
				runnerObj.newEvent(event)
		runnerObj.newTime(event, float(time))

	#return None
	#param String
	def cbb_deleteTimes_go(self, event):
		self.runnerTimes = self.runnersDict[self.runner].getTimesEvent(event)
		print("Runner times are: " + str(self.runnerTimes))
		x = 100
		y = 120
		Ystep = 15
		Xstep = 45
		yMax = y + Ystep * 25
		xMax = x + Xstep * 15
		for toRemove in self.deleteTimes_currentOn:
			toRemove.place_forget()
		self.deleteTimes_currentOn = []
		for time in self.runnerTimes:
			chk = ttk.Checkbutton(master=self.frm_deleteTimes, text=str(time))
			chk.state(["!alternate"])
			chk.place(x=x, y=y)
			y += Ystep
			if y >= yMax:
				y = 120
				x += Xstep
				if x >= xMax:
					print("OVERFLOW ERROR [TOO MANY TIMES]")
			self.deleteTimes_currentOn.append(chk)

	#return None
	#param String
	def cbb_deleteGoals_go(self, event):
		self.runnerGoals = self.runnersDict[self.runner].getGoalsEvent(event)
		print("Runner goals are: " + str(self.runnerGoals))
		x = 100
		y = 120
		Ystep = 15
		Xstep = 50
		yMax = y + Ystep * 20
		xMax = x + Xstep * 10
		for toRemove in self.deleteGoals_currentOn:
			toRemove.place_forget()
		self.deleteGoals_currentOn = []
		for goal in self.runnerGoals:
			chk = ttk.Checkbutton(master=self.frm_deleteGoals, text=str(goal))
			chk.state(["!alternate"])
			chk.place(x=x, y=y)
			y += Ystep
			if y >= yMax:
				y = 120
				x += Xstep
				if x >= xMax:
					print("OVERFLOW ERROR [TOO MANY TIMES]")
			self.deleteGoals_currentOn.append(chk)

	#return None
	#param None
	def deleteTimes_go(self):
		toDelete = []
		print("start " + str(toDelete))
		for chk in self.deleteTimes_currentOn:
			try:
				if str(chk.state()).index("selected") > -1:
					toDelete.append(chk)
			except ValueError:
				print("pass")
		print("end " + str(toDelete))
		for chk in toDelete:
			print(chk["text"])
			self.runnersDict[self.runner].removeTime(self.cbb_deleteTimes_events.get(), float(chk["text"]))

	#return None
	#param None
	def deleteGoal_go(self):
		print("deleting goals")
		toDelete = []
		print("start " + str(toDelete))
		for chk in self.deleteGoals_currentOn:
			try:
				if (str(chk.state()).index("selected") > -1):
					toDelete.append(chk)
			except ValueError:
				print("pass")
		print("end " + str(toDelete))
		for chk in toDelete:
			print("removing goal " + chk["text"] + " from " + self.cbb_deleteGoals_events.get())
			self.runnersDict[self.runner].removeGoal(self.cbb_deleteGoals_events.get(), float(chk["text"]))

	#return None
	#param None
	def import_fileSelect(self):
		file = filedialog.askopenfilename()
		print(file)
		try:
			fileObject = open(file, "r")
			self.txt_import_file.delete("1.0","end-1c")
			self.txt_import_file.insert("end-1c", str(fileObject.readlines())) #not decoding properly
			fileObject.close()
		except FileNotFoundError:
			print("FileNotFound")

	"""
	Section: Methods That Change Screens
	"""

	#return None
	#param Frame
	def goToScreen(self, frame):
		self.stack.getTop().pack_forget()
		self.stack.push(frame).pack()

	#return None
	#param None
	def back(self):
		self.stack.pop().pack_forget()
		self.stack.getTop().pack()

	#return None
	#param None
	def menu_getBest(self):
		self.goToScreen(self.frm_best)

	#return None
	#param None
	def menu_selectRunner(self):
		self.goToScreen(self.frm_select)

	#return None
	#param None
	def menu_predictor(self):
		self.goToScreen(self.frm_predictor)

	#return None
	#param None
	def menu_help(self):
		self.goToScreen(self.frm_menuHelp)

	#return None
	#param None
	def select_help(self):
		self.goToScreen(self.frm_selectHelp)

	#return None
	#param None
	def best_help(self):
		self.goToScreen(self.frm_bestHelp)

	#return None
	#param None
	def predictor_help(self):
		self.goToScreen(self.frm_predictorHelp)

	#return None
	#param None
	def runner_help(self):
		self.goToScreen(self.frm_runnerHelp)

	#return None
	#param None
	def editGoals_help(self):
		self.goToScreen(self.frm_editGoalsHelp)

	#return None
	#param None
	def editTimes_help(self):
		self.goToScreen(self.frm_editTimesHelp)

	#return None
	#param None
	def editEvents_help(self):
		self.goToScreen(self.frm_editEventsHelp)

	#return None
	#param None
	def runnerAdvanced_help(self):
		self.goToScreen(self.frm_advancedHelp)

	#return None
	#param None
	def select_new(self):
		self.goToScreen(self.frm_selectNew)

	#return None
	#param None
	def selectNew_help(self):
		self.goToScreen(self.frm_selectNewHelp)

	#return None
	#param None
	def menu_aboutUs(self):
		self.goToScreen(self.frm_aboutUs)

	#return None
	#param None
	def menu_localRank(self):
		self.goToScreen(self.frm_localRank)

	#return None
	#param None
	def localRank_help(self):
		self.goToScreen(self.frm_localRankHelp)

	#return None
	#param None
	def select_import(self):
		self.goToScreen(self.frm_import)

	#return None
	#param None
	def runner_deleteTime(self):
		self.goToScreen(self.frm_deleteTimes)

	#return None
	#param None
	def import_help(self):
		self.goToScreen(self.frm_importHelp)

	#return None
	#param None
	def deleteTimes_help(self):
		self.goToScreen(self.frm_deleteTimesHelp)

	#return None
	#param None
	def runner_deleteGoal(self):
		self.goToScreen(self.frm_deleteGoals)

	#return None
	#param None
	def deleteGoals_help(self):
		self.goToScreen(self.frm_deleteGoalsHelp)

	"""
	Section: Setting Graphics
	"""

	#return None
	#param None
	def setScreens(self):

		"""MENU SCREEN"""

		self.frm_menu = Frame(self.window, "Menu")

		lbl_menu_logo = tk.Label(master=self.frm_menu, text="Menu")
		lbl_menu_logo.place(x=370, y=0)

		btn_menu_help = tk.Button(master=self.frm_menu, text="Help", command=self.menu_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_menu_help.place(x=745, y=5)

		btn_menu_getBest = tk.Button(master=self.frm_menu, text="View Local Bests", command=self.menu_getBest, width=24, height=4, borderwidth=4, relief="raised")
		btn_menu_getBest.place(x=300, y=160)

		btn_menu_selectRunner = tk.Button(master=self.frm_menu, text="Select Runner", command=self.menu_selectRunner, width=24, height=4, borderwidth=4, relief="raised")
		btn_menu_selectRunner.place(x=300,y=80)

		btn_menu_predictors = tk.Button(master=self.frm_menu, text="Predictor (Beta)", command=self.menu_predictor, width=24, height=4, borderwidth=4, relief="raised")
		btn_menu_predictors.place(x=300, y=240)

		btn_menu_aboutUs = tk.Button(master=self.frm_menu, text="About Us", command=self.menu_aboutUs, width=8, height=1, borderwidth=4, relief="raised")
		btn_menu_aboutUs.place(x=5, y=5)

		btn_menu_localRank = tk.Button(master=self.frm_menu, text="Local Ranks", command=self.menu_localRank, width=24, height=4, borderwidth=4, relief="raised")
		btn_menu_localRank.place(x=300, y=320)

		btn_menu_quit = tk.Button(master=self.frm_menu, text="X", fg="red", command=self.out, width=2,height=1, borderwidth=3, relief="raised")
		btn_menu_quit.place(x=5, y=415)

		"""BEST SCREEN"""

		self.frm_best = Frame(self.window, "Best")

		lbl_best_logo = tk.Label(master=self.frm_best, text="Local Bests")
		lbl_best_logo.place(x=360, y=0)

		btn_best_help = tk.Button(master=self.frm_best, text="Help", command=self.best_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_best_help.place(x=745, y=5)

		lbl_best_bestDistance = tk.Label(master=self.frm_best, text=getLocalBestGroup(Distance, self.runnersDict), width=30, height=27, borderwidth=4, relief="groove")
		lbl_best_bestDistance.place(x=36, y=20)

		lbl_best_bestSprints = tk.Label(master=self.frm_best, text=getLocalBestGroup(Sprints, self.runnersDict), width=30, height=27, borderwidth=4, relief="groove")
		lbl_best_bestSprints.place(x=280, y=20)

		lbl_best_bestField = tk.Label(master=self.frm_best, text=getLocalBestGroup(Field, self.runnersDict), width=30, height=27, borderwidth=4, relief="groove")
		lbl_best_bestField.place(x=524, y=20)

		btn_best_back = tk.Button(master=self.frm_best, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_best_back.place(x=5, y=415)

		"""PREDICTOR SCREEN"""

		self.frm_predictor = Frame(self.window, "Predictor")

		lbl_predictor_logo = tk.Label(master=self.frm_predictor, text="Predictors")
		lbl_predictor_logo.place(x=370, y=0)

		self.cbb_predictor_selector = ttk.Combobox(master=self.frm_predictor, values=possiblePredictions, state="readonly", width=40)
		self.cbb_predictor_selector.place(x=270, y=90)

		lbl_predictor_entryLabel = tk.Label(master=self.frm_predictor, text="      Time      ", borderwidth=1, relief="solid")
		lbl_predictor_entryLabel.place(x=365, y=160)

		self.predictorTime = tk.StringVar()
		vcmd = self.window.register(self.isFloatPredictor), "%P"
		
		self.ent_predictor_entry = tk.Entry(master=self.frm_predictor, width=15, textvariable=self.predictorTime, validate="all", validatecommand=vcmd)
		self.ent_predictor_entry.place(x=350, y=190)

		lbl_predictor_arrow = tk.Label(master=self.frm_predictor, text="⬇️")
		lbl_predictor_arrow.place(x=390, y=220)

		self.lbl_predictor_output = tk.Label(master=self.frm_predictor, text="0.0", borderwidth=3, relief="sunken", width=10, height=1)
		self.lbl_predictor_output.place(x=360, y=250)

		btn_predictor_go = tk.Button(master=self.frm_predictor, text="GO!", command=self.predictor_go, borderwidth=3, relief="raised", width=10, height=1)
		btn_predictor_go.place(x=357, y=290)

		btn_best_help = tk.Button(master=self.frm_predictor, text="Help", command=self.predictor_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_best_help.place(x=745, y=5)

		btn_predictor_back = tk.Button(master=self.frm_predictor, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_predictor_back.place(x=5, y=415)

		"""RUNNER SELECT SCREEN"""

		self.frm_select = Frame(self.window, "Select")

		lbl_select_logo = tk.Label(master=self.frm_select, text="Select Runner")
		lbl_select_logo.place(x=360, y=0)
		
		self.cbb_select_selector = ttk.Combobox(master=self.frm_select, values=self.runnersList, state="readonly", width=40)
		self.cbb_select_selector.place(x=275, y=120)

		btn_select_help = tk.Button(master=self.frm_select, text="Help", command=self.select_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_select_help.place(x=745, y=5)

		btn_select_import = tk.Button(master=self.frm_select, text="Import", command=self.select_import, width=5, height=1, borderwidth=3, relief="raised")
		btn_select_import.place(x=5, y=5)

		btn_select_go = tk.Button(master=self.frm_select, text="GO!", command=self.select_go, borderwidth=3, relief="raised", width=20, height=2)
		btn_select_go.place(x=330, y=200)

		btn_select_new = tk.Button(master=self.frm_select, text="New Runner", command=self.select_new, borderwidth=3, relief="raised", width=20, height=2)
		btn_select_new.place(x=330, y=380)

		btn_select_back = tk.Button(master=self.frm_select, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_select_back.place(x=5, y=415)

		"""CREATE RUNNER SCREEN"""

		self.frm_selectNew = Frame(self.window, "Select New")

		lbl_selectNew_logo = tk.Label(master=self.frm_selectNew, text="New Runner")
		lbl_selectNew_logo.place(x=360, y=0)

		self.runnerName = tk.StringVar()
		vcmd = self.window.register(self.isValidRunnerName), "%P"
		
		self.ent_selectNew_entry = tk.Entry(master=self.frm_selectNew, width=15, textvariable=self.runnerName, validate="all", validatecommand=vcmd)
		self.ent_selectNew_entry.place(x=340, y=190)

		btn_selectNew_back = tk.Button(master=self.frm_selectNew, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_selectNew_back.place(x=5, y=415)

		btn_selectNew_go = tk.Button(master=self.frm_selectNew, text="GO!", command=self.selectNew_go, borderwidth=3, relief="raised", width=10, height=1)
		btn_selectNew_go.place(x=345, y=240)

		btn_selectNew_help = tk.Button(master=self.frm_selectNew, text="Help", command=self.selectNew_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_selectNew_help.place(x=745, y=5)

		"""SELECT NEW RUNNER HELP SCREEN"""

		self.frm_selectNewHelp = Frame(self.window, "Select New Help")

		lbl_selectNewHelp_logo = tk.Label(master=self.frm_selectNewHelp, text="Select New Help")
		lbl_selectNewHelp_logo.place(x=360, y=0)

		lbl_selectNewHelp_text = tk.Label(master=self.frm_selectNewHelp, text=longtext.selectNewHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_selectNewHelp_text.place(x=100, y=32)

		btn_selectNewHelp_back = tk.Button(master=self.frm_selectNewHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_selectNewHelp_back.place(x=5, y=415)

		"""MENU HELP SCREEN"""

		self.frm_menuHelp = Frame(self.window, "Menu Help")

		lbl_menuHelp_logo = tk.Label(master=self.frm_menuHelp, text="Menu Help")
		lbl_menuHelp_logo.place(x=370, y=0)

		lbl_menuHelp_text = tk.Label(master=self.frm_menuHelp, text=longtext.menuHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_menuHelp_text.place(x=100, y=32)

		btn_menuHelp_back = tk.Button(master=self.frm_menuHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_menuHelp_back.place(x=5, y=415)

		"""SELECT RUNNER HELP SCREEN"""

		self.frm_selectHelp= Frame(self.window, "Select Help")

		lbl_selectHelp_logo = tk.Label(master=self.frm_selectHelp, text="Select Help")
		lbl_selectHelp_logo.place(x=365, y=0)

		lbl_selectHelp_text = tk.Label(master=self.frm_selectHelp, text=longtext.selectHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_selectHelp_text.place(x=100, y=32)

		btn_selectHelp_back = tk.Button(master=self.frm_selectHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_selectHelp_back.place(x=5, y=415)

		"""BEST HELP SCREEN"""

		self.frm_bestHelp = Frame(self.window, "Best Help")

		lbl_bestHelp_logo = tk.Label(master=self.frm_bestHelp, text="Best Help")
		lbl_bestHelp_logo.place(x=365, y=0)

		lbl_bestHelp_text = tk.Label(master=self.frm_bestHelp, text=longtext.bestHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_bestHelp_text.place(x=100, y=32)

		btn_bestHelp_back = tk.Button(master=self.frm_bestHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_bestHelp_back.place(x=5, y=415)

		"""PREDICTOR HELP SCREEN"""

		self.frm_predictorHelp = Frame(self.window, "Predictor Help")

		lbl_predictorHelp_logo = tk.Label(master=self.frm_predictorHelp, text="Predictor Help")
		lbl_predictorHelp_logo.place(x=365, y=0)

		lbl_predictorHelp_text = tk.Label(master=self.frm_predictorHelp, text=longtext.predictorHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_predictorHelp_text.place(x=100, y=32)

		btn_predictorHelp_back = tk.Button(master=self.frm_predictorHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_predictorHelp_back.place(x=5, y=415)

		"""RUNNER HELP SCREEN"""

		self.frm_runnerHelp = Frame(self.window, "Runner Help")

		lbl_runnerHelp_logo = tk.Label(master=self.frm_runnerHelp, text="Predictor Help")
		lbl_runnerHelp_logo.place(x=365, y=0)

		lbl_runnerHelp_text = tk.Label(master=self.frm_runnerHelp, text=longtext.runnerHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_runnerHelp_text.place(x=100, y=32)

		btn_runnerHelp_back = tk.Button(master=self.frm_runnerHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_runnerHelp_back.place(x=5, y=415)

		"""EDIT GOALS SCREEN"""

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

		vcmd = self.window.register(self.isFloatGoal), "%P"

		self.goalSetTime = tk.StringVar()
		self.ent_editGoals_entry = tk.Entry(master=self.frm_editGoals, width=15, textvariable=self.goalSetTime, validate="all", validatecommand=vcmd)
		self.ent_editGoals_entry.place(x=350, y=220)

		btn_editGoals_go = tk.Button(master=self.frm_editGoals, text="GO!", command=self.editGoals_go, width=8, height=1, borderwidth=3, relief="raised")
		btn_editGoals_go.place(x=360, y=270)


		self.lbl_editGoals_output = tk.Label(master=self.frm_editGoals, text="Click GO!", width=15, height=1, borderwidth=1, relief="solid")
		self.lbl_editGoals_output.place(x=340, y=320)

		btn_editGoals_help = tk.Button(master=self.frm_editGoals, text="Help", command=self.editGoals_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_editGoals_help.place(x=745, y=5)

		"""EDIT EVENTS SCREEN"""

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
			elif event in Field:
				chk.place(x=550, y=OCount)
				OCount += 30

		btn_editEvents_save = tk.Button(master=self.frm_editEvents, text="Save", command=self.editEvents_save, width=8, height=1, borderwidth=3, relief="raised")
		btn_editEvents_save.place(x=360, y=370)

		"""EDIT TIMES SCREEN"""

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

		vcmd = self.window.register(self.isFloatTime), "%P"

		self.timeThatWasRan = tk.StringVar()
		self.ent_editTimes_entry = tk.Entry(master=self.frm_editTimes, width=15, textvariable=self.timeThatWasRan, validate="all", validatecommand=vcmd)
		self.ent_editTimes_entry.place(x=350, y=220)

		btn_editTimes_go = tk.Button(master=self.frm_editTimes, text="Add", command=self.editTimes_go, width=8, height=1, borderwidth=3, relief="raised")
		btn_editTimes_go.place(x=360, y=270)

		self.lbl_editTimes_output = tk.Label(master=self.frm_editTimes, text="Click GO!", width=40, height=1, borderwidth=1, relief="solid")
		self.lbl_editTimes_output.place(x=300, y=320)

		"""EDIT GOALS HELP SCREEN"""

		self.frm_editGoalsHelp = Frame(self.window, "Edit Goals Help")

		lbl_editGoalsHelp_logo = tk.Label(master=self.frm_editGoalsHelp, text="Edit Goals Help")
		lbl_editGoalsHelp_logo.place(x=365, y=0)

		lbl_editGoalsHelp_text = tk.Label(master=self.frm_editGoalsHelp, text=longtext.editGoalsHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_editGoalsHelp_text.place(x=100, y=32)

		btn_editGoalsHelp_back = tk.Button(master=self.frm_editGoalsHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_editGoalsHelp_back.place(x=5, y=415)

		"""EDIT EVENT HELP SCREEN"""

		self.frm_editEventsHelp = Frame(self.window, "Edit Events Help")

		lbl_editEventsHelp_logo = tk.Label(master=self.frm_editEventsHelp, text="Edit Events Help")
		lbl_editEventsHelp_logo.place(x=365, y=0)

		lbl_editEventsHelp_text = tk.Label(master=self.frm_editEventsHelp, text=longtext.editEventsHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_editEventsHelp_text.place(x=100, y=32)

		btn_editEventsHelp_back = tk.Button(master=self.frm_editEventsHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_editEventsHelp_back.place(x=5, y=415)

		"""EDIT TIMES HELP SCREEN"""

		self.frm_editTimesHelp = Frame(self.window, "Edit Times Help")

		lbl_editTimesHelp_logo = tk.Label(master=self.frm_editTimesHelp, text="Edit Time Help")
		lbl_editTimesHelp_logo.place(x=365, y=0)

		lbl_editTimesHelp_text = tk.Label(master=self.frm_editTimesHelp, text=longtext.editTimesHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_editTimesHelp_text.place(x=100, y=32)

		btn_editTimesHelp_back = tk.Button(master=self.frm_editTimesHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_editTimesHelp_back.place(x=5, y=415)

		"""ABOUT US SCREEN"""

		self.frm_aboutUs = Frame(self.window, "About Us")

		lbl_aboutUs_logo = tk.Label(master=self.frm_aboutUs, text="About Us")
		lbl_aboutUs_logo.place(x=370, y=0)

		lbl_aboutUs_text = tk.Label(master=self.frm_aboutUs, text=longtext.aboutus(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_aboutUs_text.place(x=100, y=32)

		btn_aboutUs_back = tk.Button(master=self.frm_aboutUs, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_aboutUs_back.place(x=5,y=415)

		"""LOCAL RANK SCREEN"""

		self.frm_localRank = Frame(self.window, "Local Rank")

		lbl_localRank_logo = tk.Label(master=self.frm_localRank, text="Local Ranks")
		lbl_localRank_logo.place(x=370, y=0)

		btn_localrank_help = tk.Button(master=self.frm_localRank, text="Help", command=self.localRank_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_localrank_help.place(x=745, y=5)

		self.cbb_localRank_events = ttk.Combobox(master=self.frm_localRank, state="readonly", values=Events)
		self.cbb_localRank_events.place(x=330, y=60)

		"""IMPORT HELP SCREEN"""

		self.frm_importHelp = Frame(self.window, "Import Help")

		lbl_importHelp_logo = tk.Label(master=self.frm_importHelp, text="Import Help")
		lbl_importHelp_logo.place(x=370, y=0)

		lbl_importHelp_text = tk.Label(master=self.frm_importHelp, text=longtext.importHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_importHelp_text.place(x=100, y=32)

		btn_importHelp_back = tk.Button(master=self.frm_importHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_importHelp_back.place(x=5, y=415)
		
		def callback(eventObject):
			self.localRank_update(self.cbb_localRank_events.current())
		self.cbb_localRank_events.bind("<<ComboboxSelected>>", callback)

		self.lbl_localRank_info = tk.Label(master=self.frm_localRank, text="Select An Event", height=20, width=40, borderwidth=3, relief="ridge")
		self.lbl_localRank_info.place(x=260, y=100)

		btn_localRank_back = tk.Button(master=self.frm_localRank, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_localRank_back.place(x=5,y=415)

		"""LOCAL RANK HELP SCREEN"""

		self.frm_localRankHelp = Frame(self.window, "Local Rank Help")

		lbl_localRankHelp_logo = tk.Label(master=self.frm_localRankHelp, text="Local Ranks Help")
		lbl_localRankHelp_logo.place(x=350, y=0)

		btn_localRankHelp_back = tk.Button(master=self.frm_localRankHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_localRankHelp_back.place(x=5,y=415)

		"""IMPORT SCREEN"""

		self.frm_import = Frame(self.window, "Import")

		btn_import_back = tk.Button(master=self.frm_import, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_import_back.place(x=5,y=415)

		self.cbb_import_syntaxs = ttk.Combobox(master=self.frm_import, values=supportedSyntaxs, state="readonly", width=40)
		self.cbb_import_syntaxs.place(x=275, y=120)

		btn_import_go = tk.Button(master=self.frm_import, text="IMPORT", command=self.import_update, width=10, height=1, borderwidth=3, relief="raised")
		btn_import_go.place(x=385, y=200)

		self.txt_import_file = tk.Text(self.frm_import, height=2, width=30)
		self.txt_import_file.place(x=300, y=300)

		btn_fileSelect_go = tk.Button(master=self.frm_import, text="Select File", command=self.import_fileSelect, width=10, height=1, borderwidth=3, relief="raised")
		btn_fileSelect_go.place(x=385, y=240)

		lbl_import_logo = tk.Label(master=self.frm_import, text="Import")
		lbl_import_logo.place(x=375, y=0)

		btn_import_help = tk.Button(master=self.frm_import, text="Help", command=self.import_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_import_help.place(x=745, y=5)

		"""DELETE TIMES SCREEN"""

		self.frm_deleteTimes = Frame(self.window, "Delete Times")

		lbl_deleteTimes_logo = tk.Label(master=self.frm_deleteTimes, text="Delete Times")
		lbl_deleteTimes_logo.place(x=370, y=0)

		btn_deleteTimes_back = tk.Button(master=self.frm_deleteTimes, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_deleteTimes_back.place(x=5,y=415)

		self.cbb_deleteTimes_events = ttk.Combobox(master=self.frm_deleteTimes, state="readonly", values=["Loading Error"])
		self.cbb_deleteTimes_events.place(x=370, y=100)

		def callback(eventObject):
			self.cbb_deleteTimes_go(self.cbb_deleteTimes_events.get())
		self.cbb_deleteTimes_events.bind("<<ComboboxSelected>>", callback)

		self.runnerTimes = []
		self.deleteTimes_currentOn = []

		btn_deleteTimes_save = tk.Button(master=self.frm_deleteTimes, text="remove", command=self.deleteTimes_go, width=10, height=1, borderwidth=3, relief="raised")
		btn_deleteTimes_save.place(x=385, y=200)

		btn_deleteTimes_help = tk.Button(master=self.frm_deleteTimes, text="Help", command=self.deleteTimes_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_deleteTimes_help.place(x=745, y=5)

		"""DELETE GOALS SCREEN"""

		self.frm_deleteGoals = Frame(self.window, "Delete Goals")

		lbl_deleteGoals_logo = tk.Label(master=self.frm_deleteGoals, text="Delete Goals")
		lbl_deleteGoals_logo.place(x=370, y=0)

		btn_deleteGoals_back = tk.Button(master=self.frm_deleteGoals, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_deleteGoals_back.place(x=5,y=415)

		self.cbb_deleteGoals_events = ttk.Combobox(master=self.frm_deleteGoals, state="readonly", values=["Loading Error"])
		self.cbb_deleteGoals_events.place(x=370, y=100)

		def callback(eventObject):
			self.cbb_deleteGoals_go(self.cbb_deleteGoals_events.get())
		self.cbb_deleteGoals_events.bind("<<ComboboxSelected>>", callback)

		self.runnerGoals = []
		self.deleteGoals_currentOn = []

		btn_deleteGoals_save = tk.Button(master=self.frm_deleteGoals, text="remove", command=self.deleteGoal_go, width=10, height=1, borderwidth=3, relief="raised")
		btn_deleteGoals_save.place(x=385, y=200)

		btn_deleteGoals_help = tk.Button(master=self.frm_deleteGoals, text="Help", command=self.deleteGoals_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_deleteGoals_help.place(x=745, y=5)

		"""DELETE TIMES HELP SCREEN"""

		self.frm_deleteGoalsHelp = Frame(self.window, "Delete Goals Help")

		lbl_deleteGoalsHelp_logo = tk.Label(master=self.frm_deleteGoalsHelp, text="Delete Goals Help")
		lbl_deleteGoalsHelp_logo.place(x=365, y=0)

		lbl_deleteGoalsHelp_text = tk.Label(master=self.frm_deleteGoalsHelp, text=longtext.deleteGoalsHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_deleteGoalsHelp_text.place(x=100, y=32)

		btn_deleteGoalsHelp_back = tk.Button(master=self.frm_deleteGoalsHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_deleteGoalsHelp_back.place(x=5, y=415)

		"""ADVANCED RUNNER HELP SCREEN"""

		self.frm_advancedHelp = Frame(self.window, "Advanced Help")

		lbl_advancedHelp_logo = tk.Label(master=self.frm_advancedHelp, text="Advanced Help")
		lbl_advancedHelp_logo.place(x=365, y=0)

		lbl_advancedHelp_text = tk.Label(master=self.frm_advancedHelp, text=longtext.advancedHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_advancedHelp_text.place(x=100, y=32)

		btn_advancedHelp_back = tk.Button(master=self.frm_advancedHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_advancedHelp_back.place(x=5, y=415)

		"""DELETE TIME HELP SCREEN"""

		self.frm_deleteTimesHelp = Frame(self.window, "Delete Times Help")

		lbl_deleteTimesHelp_logo = tk.Label(master=self.frm_deleteTimesHelp, text="Delete Times Help")
		lbl_deleteTimesHelp_logo.place(x=365, y=0)

		lbl_deleteTimesHelp_text = tk.Label(master=self.frm_deleteTimesHelp, text=longtext.deleteTimesHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_deleteTimesHelp_text.place(x=100, y=32)

		btn_deleteTimesHelp_back = tk.Button(master=self.frm_deleteTimesHelp, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_deleteTimesHelp_back.place(x=5, y=415)

		"""ADVANCED RUNNER SCREEN"""

		self.frm_runnerAdvanced = Frame(self.window, "Advanced")

		lbl_runnerAdvanced_logo = tk.Label(master=self.frm_runnerAdvanced, text="Advanced Stats")
		lbl_runnerAdvanced_logo.place(x=355, y=0)

		self.lbl_runnerAdvanced_name = tk.Label(master=self.frm_runnerAdvanced, text="TDB")
		self.lbl_runnerAdvanced_name.place(x=365, y=20)

		btn_runnerAdvanced_help = tk.Button(master=self.frm_runnerAdvanced, text="Help", command=self.runnerAdvanced_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_runnerAdvanced_help.place(x=745, y=5)

		btn_runnerAdvanced_back = tk.Button(master=self.frm_runnerAdvanced, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		btn_runnerAdvanced_back.place(x=5, y=415)

		self.lbl_runnerAdvanced_points = tk.Label(master=self.frm_runnerAdvanced, text="Points", width=30, height=5, borderwidth=1, relief="solid")
		self.lbl_runnerAdvanced_points.place(x=20, y=20)

		self.lbl_runnerAdvanced_pointSEvent = tk.Label(master=self.frm_runnerAdvanced, text="Points", width=30, height=20, borderwidth=1, relief="solid")
		self.lbl_runnerAdvanced_pointSEvent.place(x=20, y=98)

		"""RUNNER SCREEN"""

		self.frm_runner = Frame(self.window, "Runner")

		self.lbl_runner_name = tk.Label(master=self.frm_runner, text="ERROR LOADING")
		self.lbl_runner_name.place(x=365, y=0)

		self.lbl_runner_goalsPassed = tk.Label(master=self.frm_runner, text="ERROR LOADING")
		self.lbl_runner_goalsPassed.place(x=450, y=40)

		self.scr_runner_goals = tk.Scrollbar(master=self.frm_runner, background="green", width=100)

		self.myList = tk.Listbox(master=self.frm_runner, yscrollcommand=self.scr_runner_goals.set, width=24, height=23) 
		self.myList.insert(tk.END, "ERROR LOADING INFO")
		self.myList.place(x=630, y=60)

		self.scr_runner_goals.config(command=self.myList.yview)


		self.btn_runner_advanced = tk.Button(master=self.frm_runner, text="Advanced Stats", command=self.runner_advanced, width=15, height=1, borderwidth=3, relief="raised")
		self.btn_runner_advanced.place(x=600, y=5)
		self.btn_runner_help = tk.Button(master=self.frm_runner, text="Help", command=self.runner_help, width=5, height=1, borderwidth=3, relief="raised")
		self.btn_runner_help.place(x=745, y=5)

		self.btn_runner_back = tk.Button(master=self.frm_runner, text="B", fg="green", command=self.back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_runner_back.place(x=5, y=415)

		self.lbl_runner_prLabel = tk.Label(master=self.frm_runner, text="PRs", width=20, height=1, borderwidth=2, relief="ridge")
		self.lbl_runner_prLabel.place(x=40, y=40)

		self.lbl_runner_prs = tk.Label(master=self.frm_runner, text="ERROR LOADING", width=20, height=24, borderwidth=2, relief="ridge")
		self.lbl_runner_prs.place(x=40, y=60)

		self.lbl_runner_goalLabel = tk.Label(master=self.frm_runner, text="Goals", width=20, height=1, borderwidth=2, relief="ridge")
		self.lbl_runner_goalLabel.place(x=630, y=40)

		self.btn_runner_editEvents = tk.Button(master=self.frm_runner,command=self.runner_addEvent, text="edit events", width=10, height=1, borderwidth=3, relief="raised")
		self.btn_runner_editEvents.place(x=200, y=415)

		self.btn_runner_addTime = tk.Button(master=self.frm_runner, command=self.runner_addTime, text="add time", width=10, height=1, borderwidth=3, relief="raised")
		self.btn_runner_addTime.place(x=285, y=415)
 
		self.btn_runner_addGoal = tk.Button(master=self.frm_runner, command=self.runner_addGoal, text="add goal", width=10, height=1, borderwidth=3, relief="raised")
		self.btn_runner_addGoal.place(x=370, y=415)

		self.btn_runner_deleteTime = tk.Button(master=self.frm_runner, command=self.runner_deleteTime, text="delete time", width=10, height=1, borderwidth=3, relief="raised")
		self.btn_runner_deleteTime.place(x=455, y=415)

		self.btn_runner_deleteTime = tk.Button(master=self.frm_runner, command=self.runner_deleteGoal, text="delete goal", width=10, height=1, borderwidth=3, relief="raised")
		self.btn_runner_deleteTime.place(x=540, y=415)

		self.cbb_runner_events = ttk.Combobox(master=self.frm_runner, state="readonly", values="ERROR LOADING")
		self.cbb_runner_events.place(x=290, y=40)

		def callback(eventObject):
			self.cbb_runner_event(self.cbb_runner_events.get())
		self.cbb_runner_events.bind("<<ComboboxSelected>>", callback)

		self.lbl_runner_eventInfo = tk.Label(master=self.frm_runner, text="Select A Event", width=58, height=20, borderwidth=3, relief="ridge")
		self.lbl_runner_eventInfo.place(x=200, y=80)