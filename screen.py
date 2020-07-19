from runner import Runner
import longtext
import tkinter as tk
from tkinter import ttk


"""
Next Steps:

GUI

CheckBox For choosing events (under runner)
(use a line in the middle, to properly center thigns)

if space, a full predictor for each event in the runner page (probs going to be pretty hard)

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
	def __init__(self, runnersDict):
		self.runnersDict = runnersDict
		self.runnersList = []
		for runner in self.runnersDict:
			self.runnersList.append(runner)
		self.window = tk.Tk()
		self.window.resizable(False, False)
		self.window.title("something else")

		self.setMenu()
		self.setBest()
		self.setSelect()
		self.setPredictor()
		self.setHelpSelect()
		self.setHelpMenu()
		self.setHelpBest()
		self.setHelpPredictor()
		self.setRunnerHelp()

		self.frm_menu.pack()

	def test(self):
		pass

	def toDo(self):
		print("TODO")

	def setMenu(self):
		self.frm_menu = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

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
		self.frm_best = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

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
		self.frm_predictor = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		lbl_predictor_logo = tk.Label(master=self.frm_predictor, text="Predictors")
		lbl_predictor_logo.place(x=370, y=0)

		self.cbb_predictor_selector = ttk.Combobox(master=self.frm_predictor, values=possiblePredictions, state="readonly", width=40)
		self.cbb_predictor_selector.place(x=270, y=90)

		lbl_predictor_entryLabel = tk.Label(master=self.frm_predictor, text="      Time      ", borderwidth=1, relief="solid")
		lbl_predictor_entryLabel.place(x=365, y=160)

		self.predictorTime = tk.StringVar()
		vcmd = (self.window.register(self.isFloat), "%P") #research register command
		
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

		btn_predictor_back = tk.Button(master=self.frm_predictor, text="B", fg="green", command=self.predictor_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_predictor_back.place(x=5, y=415)


	def setSelect(self):
		self.frm_select = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

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
		self.frm_menuHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		lbl_menuHelp_logo = tk.Label(master=self.frm_menuHelp, text="Menu Help")
		lbl_menuHelp_logo.place(x=370, y=0)

		lbl_menuHelp_text = tk.Label(master=self.frm_menuHelp, text=longtext.menuHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_menuHelp_text.place(x=100, y=32)

		btn_menuHelp_back = tk.Button(master=self.frm_menuHelp, text="B", fg="green", command=self.menuHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_menuHelp_back.place(x=5, y=415)

	def setHelpSelect(self):
		self.frm_selectHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		lbl_selectHelp_logo = tk.Label(master=self.frm_selectHelp, text="Select Help")
		lbl_selectHelp_logo.place(x=365, y=0)

		lbl_selectHelp_text = tk.Label(master=self.frm_selectHelp, text=longtext.selectHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_selectHelp_text.place(x=100, y=32)

		btn_selectHelp_back = tk.Button(master=self.frm_selectHelp, text="B", fg="green", command=self.selectHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_selectHelp_back.place(x=5, y=415)

	def setHelpBest(self):
		self.frm_bestHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		lbl_bestHelp_logo = tk.Label(master=self.frm_bestHelp, text="Best Help")
		lbl_bestHelp_logo.place(x=365, y=0)

		lbl_bestHelp_text = tk.Label(master=self.frm_bestHelp, text=longtext.bestHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_bestHelp_text.place(x=100, y=32)

		btn_bestHelp_back = tk.Button(master=self.frm_bestHelp, text="B", fg="green", command=self.bestHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_bestHelp_back.place(x=5, y=415)

	def setHelpPredictor(self):
		self.frm_predictorHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		lbl_predictorHelp_logo = tk.Label(master=self.frm_predictorHelp, text="Predictor Help")
		lbl_predictorHelp_logo.place(x=365, y=0)

		lbl_predictorHelp_text = tk.Label(master=self.frm_predictorHelp, text=longtext.predictorHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_predictorHelp_text.place(x=100, y=32)

		btn_predictorHelp_back = tk.Button(master=self.frm_predictorHelp, text="B", fg="green", command=self.predictorHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_predictorHelp_back.place(x=5, y=415)

	def setRunnerHelp(self):
		self.frm_runnerHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		lbl_runnerHelp_logo = tk.Label(master=self.frm_runnerHelp, text="Predictor Help")
		lbl_runnerHelp_logo.place(x=365, y=0)

		lbl_runnerHelp_text = tk.Label(master=self.frm_runnerHelp, text=longtext.runnerHelp(), height=25, width=81, borderwidth=3, relief="ridge")
		lbl_runnerHelp_text.place(x=100, y=32)

		btn_runnerHelp_back = tk.Button(master=self.frm_runnerHelp, text="B", fg="green", command=self.runnerHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_runnerHelp_back.place(x=5, y=415)

	def setRunnerPage(self, runner):
		self.frm_runner = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_runner_name = tk.Label(master=self.frm_runner, text=runner)
		self.lbl_runner_name.place(x=365, y=0)

		btn_runner_help = tk.Button(master=self.frm_runner, text="Help", command=self.runner_help, width=5, height=1, borderwidth=3, relief="raised")
		btn_runner_help.place(x=745, y=5)

		btn_runner_back = tk.Button(master=self.frm_runner, text="B", fg="green", command=self.runner_back, width=2,height=1, borderwidth=3, relief="raised")
		btn_runner_back.place(x=5, y=415)


		



	"""
	Methods That Actually Do Something
	"""
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
					self.lbl_predictor_output["text"] = ("%.2f" % ((float(time) * 2.06) -1))
				if (index == 1):
					self.lbl_predictor_output["text"] = ("%.2f" % ((float(time) * 2.12) + 1.35))

	def select_go(self):
		runner = self.cbb_select_selector.current()
		self.setRunnerPage(self.runnersList[runner])
		self.frm_select.pack_forget()
		self.frm_runner.pack()

	def isFloat(self, toBe):
		if toBe == "":
			return True
		try:
			num = float(toBe)
			return True
		except ValueError:
			return False


	"""
	Method That Change Screens
	"""

	def menu_getBest(self):
		self.frm_menu.pack_forget()
		self.frm_best.pack()

	def best_back(self):
		self.frm_best.pack_forget()
		self.frm_menu.pack()

	def menu_selectRunner(self):
		self.frm_menu.pack_forget()
		self.frm_select.pack()

	def select_back(self):
		self.frm_select.pack_forget()
		self.frm_menu.pack()

	def menu_predictor(self):
		self.frm_menu.pack_forget()
		self.frm_predictor.pack()

	def predictor_back(self):
		self.frm_predictor.pack_forget()
		self.frm_menu.pack()

	def menu_help(self):
		self.frm_menu.pack_forget()
		self.frm_menuHelp.pack()

	def menuHelp_back(self):
		self.frm_menuHelp.pack_forget()
		self.frm_menu.pack()

	def select_help(self):
		self.frm_select.pack_forget()
		self.frm_selectHelp.pack()

	def selectHelp_back(self):
		self.frm_selectHelp.pack_forget()
		self.frm_select.pack()

	def best_help(self):
		self.frm_best.pack_forget()
		self.frm_bestHelp.pack()

	def bestHelp_back(self):
		self.frm_bestHelp.pack_forget()
		self.frm_best.pack()

	def predictor_help(self):
		self.frm_predictor.pack_forget()
		self.frm_predictorHelp.pack()

	def predictorHelp_back(self):
		self.frm_predictorHelp.pack_forget()
		self.frm_predictor.pack()

	def runner_back(self):
		self.frm_runner.pack_forget()
		self.frm_select.pack()

	def runner_help(self):
		self.frm_runner.pack_forget()
		self.frm_runnerHelp.pack()

	def runnerHelp_back(self):
		self.frm_runnerHelp.pack_forget()
		self.frm_runner.pack()



	def start(self):
		self.window.mainloop()
