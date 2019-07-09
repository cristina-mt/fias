# =================================================
# GUI program to analyse STEM images of filamentous structures: ANALYSIS
# -----------------------------------------------------------------------------
# Version 1.0
# Created: January 15th, 2018
# Last modification: January 12th, 2019
# author: @Cristina_MT
#
# =================================================

from sys import platform as sys_pf

import tkinter as tk
from tkinter import ttk, filedialog

import time
import numpy as np
from PIL import Image

if sys_pf == 'darwin':
	import matplotlib
	matplotlib.use('TkAgg')


from winan import WindowAnalysis

class fiAS(tk.Frame):
	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.grid(sticky = 'nsew')
		WindowAnalysis.__init__(self)


app = fiAS()
app.master.title('fiAS Analysis v1.0 (January 2019)')
app.master.geometry('800x600+50+50')
app.mainloop()
