import tkinter as tk
from tkinter import ttk
import threading
import os
import pathlib


def start():
	print("start")
	window = tk.Tk()
	window.resizable(False, False)
	window.title("Uninstall")

	frm_main = tk.Frame(master=window, height=200, width=500, borderwidth=2, relief="groove")
	confirmBoxLabel = tk.Label(master=frm_main, text='Type "confirm" to Uninstall')
	confirmBoxLabel.place(x=200, y=100)
	text = tk.StringVar()
	entry = tk.Entry(master=frm_main, width=15, textvariable=text)
	entry.place(x=200, y=120)
	def check():
		if (entry.get() == "confirm"):
			print ("happened")
			window.destroy()
			#print(pathlib.Path(__file__).parent.parent.absolute())
			os.rmdir(pathlib.Path(__file__).parent.parent.absolute()) #works, but has to be somewhere else
			#TODO something that causes the destruction of everything
			#subprocess.call(['unin.bat'])
	go = tk.Button(master=frm_main, text="Go", command=check, borderwidth=3, relief="raised", width=10, height=1)
	go.place(x=200, y=150)
	frm_main.pack()
	window.mainloop()