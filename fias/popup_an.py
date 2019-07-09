import tkinter as tk
from tkinter import ttk

class ErrorMass():

	def needcal(self):
	
		try: self.emnc_Window.destroy()
		except AttributeError: pass
		
		self.emnc_Window = tk.Toplevel(self)
		self.emnc_Window.title('Error Message')
		self.emnc_Window.resizable(0,0)
		
		self.emnc_Window.rowconfigure(0, weight = 1)
		self.emnc_Window.columnconfigure(0, weight = 1)
		
		text_error = 'Error: \n There is no reference for calibration\n '
		text_fix = '\n Go to menu Mass Mapping -> Set Reference'
		
		self.emnc_textLabel = ttk.Label(self.emnc_Window,
								text = text_error + text_fix,
								width = 40,
								justify = 'center')
		self.emnc_closeButton = ttk.Button(self.emnc_Window,
								text = 'Close',
								command = lambda: self.emnc_Window.destroy())
		
		self.emnc_textLabel.grid(row = 0, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.emnc_closeButton.grid(row = 1, column = 0,
											padx = 5, pady = 5)