# =================================================
# GUI program to analyse STEM images of filamentous structures: TRACKING
# -----------------------------------------------------------------------------
# Version 1.0
# Created: November 7th, 2017
# Last modification: January 8th, 2019
# author: @Cristina_MT
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


from wintrack import WindowTracking

class fiAS(tk.Frame):
	def __init__(self, master = None):
		fiAS.controlanchor = 0
		tk.Frame.__init__(self, master)
		self.grid(sticky = 'nsew')
		WindowTracking.__init__(self)

app = fiAS()
app.master.title('fiAS Tracking v1.0 (January 2019)')
if fiAS.controlanchor == 0: app.master.geometry('800x600+50+50')
elif fiAS.controlanchor == 1: app.master.geometry('900x550+50+50')
app.mainloop()
