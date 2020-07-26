import tkinter as tk

class loadingScreen(tk.Tk):
	def __init__(self):
		super().__init__()
		lbl_loading = tk.Label(master=self, text="Loading . . . ", height=3, width=15)
		lbl_loading.pack()
		#self.mainloop()

	def close(self):
		self.destroy()
