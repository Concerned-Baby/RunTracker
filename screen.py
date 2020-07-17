from runner import Runner
import tkinter as tk
from tkinter import ttk


"""
Next Steps:

GUI
redo the few get() methods in main, so that they return, not print
Make a global list of all events, and make sure no strange events are added
CheckBox For choosing events (under runner)
(use a line in the middle, to properly center thigns)

"""


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


def getAllEvents(runnersDict):
	events = []
	for runner in runnersDict:
		rEvents = runnersDict[runner].getEvents()
		for event in rEvents:
			if event not in events:
				events.append(event)
	return events

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
		print("\nBest %s Run: N/A" % eventName)
		print("Best %s Runner: N/A" % eventName)
	else:
		print ("\nBest %s Run: %.2f" % (eventName, best))
		print ("Best %s Runner: %s" % (eventName, bestMan))

def getAllLocalBests():
	pass


class myApplicationManager(object):
	def __init__(self, runnersDict):
		self.runnersDict = runnersDict
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
		self.btn_menu_getBest.place(x=300, y=210)

		self.btn_menu_selectRunner = tk.Button(master=self.frm_menu, text="Select Runner", command=self.menu_selectRunner, width=24, height=4, borderwidth=4, relief="raised")
		self.btn_menu_selectRunner.place(x=300,y=130)

		self.btn_menu_predictors = tk.Button(master=self.frm_menu, text="Predictor (Beta)", command=self.menu_predictor, width=24, height=4, borderwidth=4, relief="raised")
		self.btn_menu_predictors.place(x=300, y=290)

		self.btn_menu_quit = tk.Button(master=self.frm_menu, text="X", fg="red", command=self.out, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_menu_quit.place(x=5, y=415)

	def setBest(self):
		self.frm_best = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_best_logo = tk.Label(master=self.frm_best, text="Local Bests")
		self.lbl_best_logo.place(x=360, y=0)

		self.btn_best_help = tk.Button(master=self.frm_best, text="Help", command=self.best_help, width=5, height=1, borderwidth=3, relief="raised")
		self.btn_best_help.place(x=745, y=5)

		self.lbl_best_bestDistance = tk.Label(master=self.frm_best, text="ToDo", width=30, height=27, borderwidth=4, relief="groove")
		self.lbl_best_bestDistance.place(x=36, y=20)

		self.lbl_best_bestSprints = tk.Label(master=self.frm_best, text="ToDo", width=30, height=27, borderwidth=4, relief="groove")
		self.lbl_best_bestSprints.place(x=280, y=20)

		self.lbl_best_bestField = tk.Label(master=self.frm_best, text="ToDo", width=30, height=27, borderwidth=4, relief="groove")
		self.lbl_best_bestField.place(x=524, y=20)

		self.btn_best_back = tk.Button(master=self.frm_best, text="B", fg="green", command=self.best_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_best_back.place(x=5, y=415)

	def setPredictor(self):
		self.frm_predictor = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_predictor_logo = tk.Label(master=self.frm_predictor, text="Predictors")
		self.lbl_predictor_logo.place(x=370, y=0)

		self.cbb_predictor_selector = ttk.Combobox(master=self.frm_predictor, values=["ToDo"], state="readonly", width=40)
		self.cbb_predictor_selector.place(x=270, y=90)

		self.lbl_predictor_entryLabel = tk.Label(master=self.frm_predictor, text="      Time      ", borderwidth=1, relief="solid")
		self.lbl_predictor_entryLabel.place(x=365, y=160)

		self.predictorTime = tk.StringVar()
		self.ent_predictor_entry = tk.Entry(master=self.frm_predictor, width=15, textvariable=self.predictorTime)
		self.ent_predictor_entry.place(x=350, y=190)

		self.lbl_predictor_arrow = tk.Label(master=self.frm_predictor, text="⬇️")
		self.lbl_predictor_arrow.place(x=390, y=220)

		self.lbl_predictor_output = tk.Label(master=self.frm_predictor, text="0.0", borderwidth=3, relief="sunken", width=10, height=1)
		self.lbl_predictor_output.place(x=360, y=250)

		self.btn_predictor_go = tk.Button(master=self.frm_predictor, text="GO!", command=self.toDo, borderwidth=3, relief="raised", width=10, height=1)
		self.btn_predictor_go.place(x=357, y=290)

		self.btn_best_help = tk.Button(master=self.frm_predictor, text="Help", command=self.predictor_help, width=5, height=1, borderwidth=3, relief="raised")
		self.btn_best_help.place(x=745, y=5)

		self.btn_predictor_back = tk.Button(master=self.frm_predictor, text="B", fg="green", command=self.predictor_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_predictor_back.place(x=5, y=415)


	def setSelect(self):
		self.frm_select = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_select_logo = tk.Label(master=self.frm_select, text="Select Runner")
		self.lbl_select_logo.place(x=360, y=0)


		"""
		instead of having two separate frames filled with buttons,
		use a combo box, and acess the dictionary using the .current()
		"""
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

		self.lbl_menuHelp_text = tk.Label(master=self.frm_menuHelp, text="ToDo", height=25, width=81, borderwidth=3, relief="ridge")
		self.lbl_menuHelp_text.place(x=100, y=32)

		self.btn_menuHelp_back = tk.Button(master=self.frm_menuHelp, text="B", fg="green", command=self.menuHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_menuHelp_back.place(x=5, y=415)

	def setHelpSelect(self):
		self.frm_selectHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_selectHelp_logo = tk.Label(master=self.frm_selectHelp, text="Select Help")
		self.lbl_selectHelp_logo.place(x=365, y=0)

		self.lbl_selectHelp_text = tk.Label(master=self.frm_selectHelp, text="ToDo", height=25, width=81, borderwidth=3, relief="ridge")
		self.lbl_selectHelp_text.place(x=100, y=32)

		self.btn_selectHelp_back = tk.Button(master=self.frm_selectHelp, text="B", fg="green", command=self.selectHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_selectHelp_back.place(x=5, y=415)

	def setHelpBest(self):
		self.frm_bestHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_bestHelp_logo = tk.Label(master=self.frm_bestHelp, text="Best Help")
		self.lbl_bestHelp_logo.place(x=365, y=0)

		self.lbl_bestHelp_text = tk.Label(master=self.frm_bestHelp, text="ToDo", height=25, width=81, borderwidth=3, relief="ridge")
		self.lbl_bestHelp_text.place(x=100, y=32)

		self.btn_bestHelp_back = tk.Button(master=self.frm_bestHelp, text="B", fg="green", command=self.bestHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_bestHelp_back.place(x=5, y=415)

	def setHelpPredictor(self):
		self.frm_predictorHelp = tk.Frame(master=self.window, height=450, width=800, borderwidth=2, relief="groove")

		self.lbl_predictorHelp_logo = tk.Label(master=self.frm_predictorHelp, text="Predictor Help")
		self.lbl_predictorHelp_logo.place(x=365, y=0)

		self.lbl_predictorHelp_text = tk.Label(master=self.frm_predictorHelp, text="ToDo", height=25, width=81, borderwidth=3, relief="ridge")
		self.lbl_predictorHelp_text.place(x=100, y=32)

		self.btn_predictorHelp_back = tk.Button(master=self.frm_predictorHelp, text="B", fg="green", command=self.predictorHelp_back, width=2,height=1, borderwidth=3, relief="raised")
		self.btn_predictorHelp_back.place(x=5, y=415)


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
	def addPredictor(self):
		self.frm_predictor.pack()
	def removePredictor(self):
		self.frm_predictor.pack_forget()
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
	def addPredictorHelp(self):
		self.frm_predictorHelp.pack()
	def removePredictorHelp(self):
		self.frm_predictorHelp.pack_forget()

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

	def menu_predictor(self):
		self.removeMenu()
		self.addPredictor()

	def predictor_back(self):
		self.removePredictor()
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

	def predictor_help(self):
		self.removePredictor()
		self.addPredictorHelp()

	def predictorHelp_back(self):
		self.removePredictorHelp()
		self.addPredictor()




	def start(self):
		self.window.mainloop()
