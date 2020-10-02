import tkinter as tk
from tkinter import ttk
import threading

def check():
	print("hi")

def start():
	print("start")
	window = tk.Tk()
	#window.resizable(False, False)
	window.title("Uninstall")

	frm_main = tk.Frame(master=window, height=200, width=500, borderwidth=2, relief="groove")
	confirmBoxLabel = tk.Label(master=frm_main, text='Type "Confirm" to Uninstall')
	confirmBoxLabel.place(x=200, y=100)
	text = tk.StringVar()
	vcmd = check()
	entry = tk.Entry(master=frm_main, width=15, textvariable=text, validate="all", validatecommand=vcmd)
	entry.place(x=200, y=120)
	entry.get()

	threading.Thread.start_new_thread(check, "thread")

	#window.add(frm_main)
	frm_main.pack()



	window.mainloop()