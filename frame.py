import tkinter as tk

class Frame(tk.Frame):
	def __init__ (self, window, name):
		super().__init__(master=window, height=450, width=800, borderwidth=2, relief="groove")
		self.name = name
	def toString(self):
		return self.name