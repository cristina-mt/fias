import tkinter as tk
from tkinter import ttk

from menufile_an import FileLoad, FileSave, FileClose
from menuimage_an import ImageColormap, ImageContrast, ImageOverlay
from menuroi_an import ROIdraw, ROIimage
from menumass_an import RefMass, RunMass

class WindowAnalysis():

	def __init__(self):
		tk.Frame.__init__(self)
		MenuAnalysis.init_var(self)
		RefMass.init_var(self)
		MenuAnalysis.create(self)
		MainDisplay.create(self)

		WindowAnalysis.bind_shortcuts(self)
		
		self._inputdata = dict()

	def bind_shortcuts(self):

		self.bind_all('<Control-q>',
						lambda event, arg = self: WindowAnalysis.quit(arg, event))
	
		self.bind_all('<L>',
						lambda event, arg = self: WindowAnalysis.roi_line(arg, event))
		self.bind_all('<C>',
						lambda event, arg = self: WindowAnalysis.roi_circle(arg, event),
						add = '+')
		self.bind_all('<R>',
						lambda event, arg = self: WindowAnalysis.roi_rect(arg, event),
						add = '+')

		self.bind_all('<D>',
						lambda event, arg = self: WindowAnalysis.roi_delall(arg, event))
		self.bind_all('<K>',
						lambda event, arg = self: WindowAnalysis.roi_keepall(arg, event),
						add = '+')
		self.bind_all('<S>',
						lambda event, arg = self: WindowAnalysis.roi_splitall(arg, event),
						add = '+')
		self.bind_all('<M>',
						lambda event, arg = self: WindowAnalysis.roi_mergeall(arg, event),
						add = '+')
						
		self.bind_all('<Control-r>',
						lambda event, arg = self: WindowAnalysis.ref_set(arg, event),
						add = '+')
						
	def quit(self, event):
		self.quit()

	def roi_line(self, event):
		if self._roidrawline.get() == 0: self._roidrawline.set(1)
		elif self._roidrawline.get() == 1: self._roidrawline.set(0)
		ROIdraw.line(self)

	def roi_circle(self, event):
		if self._roidrawcircle.get() == 0: self._roidrawcircle.set(1)
		elif self._roidrawcircle.get() == 1: self._roidrawcircle.set(0)

		ROIdraw.circle(self)

	def roi_rect(self, event):
		if self._roidrawrect.get() == 0: self._roidrawrect.set(1)
		elif self._roidrawrect.get() == 1: self._roidrawrect.set(0)

		ROIdraw.rectangle(self)

	def roi_delall(self, event):
		ROIimage.keepdelall(self, 0)

	def roi_keepall(self, event):
		ROIimage.keepdelall(self, 1)

	def roi_splitall(self, event):
		print('s')

	def roi_mergeall(self, event):
		ROIimage.mergeall(self)
		
	def ref_set(self, event):
		if self._menucheckMS.get() == 0: self._menucheckMS.set(1)
		elif self._menucheckMS.get() == 1: self._menucheckMS.set(0)
		
		RefMass.set(self)

class MenuAnalysis():

	def init_var(self):
		self._colormap_options = dict()
		self._menucheckOI = tk.IntVar() # Show Original Image
		self._menucheckCI = tk.IntVar() # Inverse Colormap
		self._menucheckCO = tk.IntVar() # Colormap Options
		self._menucheckCC = tk.IntVar() # Adjust Contrast
		self._menucheckOO = tk.IntVar() # Show Overlay Options
		self._menucheckRI = tk.IntVar() # ROI source options
		self._menucheckRD = tk.IntVar() # Draw ROI
		self._menucheckRM = tk.IntVar() # Show ROI manager
		self._menucheckRF = tk.IntVar() # Show Fiber Inspector
		self._menucheckMS  = tk.IntVar() # Mass Set Reference
		self._menucheckMR = tk.IntVar()  # Show Reference Manager
		self._menucheckMC = tk.IntVar() # Show Mass Calibration
	
		self._menucheckOI.set(0)
		self._menucheckCI.set(0)
		self._menucheckCO.set(0)
		self._menucheckCC.set(0)
		self._menucheckOO.set(0)
		self._menucheckRI.set(0)
		self._menucheckRD.set(0)
		self._menucheckRM.set(0)
		self._menucheckRF.set(0)
		self._menucheckMS.set(0)
		self._menucheckMR.set(0)
		self._menucheckMC.set(0)
		
		ImageOverlay.init_var(self)
		ROIdraw.init_var(self)

	def create(self):
		self.menubar = tk.Menu(self.master)
		MenuAnalysis.create_file(self)
		MenuAnalysis.create_image(self)
		MenuAnalysis.create_roi(self)
		MenuAnalysis.create_massmap(self)
		MenuAnalysis.create_stats(self)
		MenuAnalysis.create_plot(self)
		MenuAnalysis.create_advanced(self)

		self.master.config(menu = self.menubar)

		MenuAnalysis.setstate_init(self)

	def create_file(self):

		self.menufile = tk.Menu(self.menubar, tearoff = 0)
		self.menufile.add_command(label = 'Load',
										command = lambda: MenuAnalysis.menufile_load(self))
		self.menufile.add_command(label = 'Save As...',
										command = lambda: FileSave.saveas(self))
		self.menufile.add_command(label = 'Export')
		self.menufile.add_command(label = 'Close',
										command = lambda: MenuAnalysis.menufile_close(self))
		self.menufile.add_command(label = 'Restart')
		self.menufile.add_separator()
		self.menufile.add_command(label = 'Quit',
										underline = 0,
										accelerator = 'Ctrl+Q',
										command = self.quit)

		self.menubar.add_cascade(label = 'File',
										menu = self.menufile)

	def create_image(self):

		self.menuimg = tk.Menu(self.menubar, tearoff = 0)

		self.menucmap = tk.Menu(self.menuimg, tearoff = 0)
		self.menucmap.add_checkbutton(label = 'Invert Colormap',
									variable = self._menucheckCI,
									command = lambda: ImageColormap.invert(self))
		self.menucmap.add_separator()
		self.menucmap.add_radiobutton(label = 'Gray',
									variable = self._menucheckCO,
									value = 0,
									command = lambda: ImageColormap.change(self))
		self.menucmap.add_radiobutton(label = 'Bone',
									variable = self._menucheckCO,
									value = 1,
									command = lambda: ImageColormap.change(self))
		self.menucmap.add_radiobutton(label = 'Hot',
									variable = self._menucheckCO,
									value = 2,
									command = lambda: ImageColormap.change(self))
		self.menucmap.add_radiobutton(label = 'Magma',
									variable = self._menucheckCO,
									value = 3,
									command = lambda: ImageColormap.change(self))
		self.menucmap.add_radiobutton(label = 'Inferno',
									variable = self._menucheckCO,
									value = 4,
									command = lambda: ImageColormap.change(self))
		self.menucmap.add_separator()
		self.menucmap.add_radiobutton(label = 'Other',
									variable = self._menucheckCO,
									value = 5,
									command = lambda: ImageColormap.other(self))

		self.menuimg.add_checkbutton(label = 'Show Original Image',
									variable = self._menucheckOI)
		self.menuimg.add_cascade(label = 'Colormap', menu = self.menucmap)
		self.menuimg.add_checkbutton(label = 'Adjust Contrast',
									variable = self._menucheckCC,
									command = lambda: ImageContrast.show(self))
		self.menuimg.add_checkbutton(label = 'Show Overlay Options',
									variable = self._menucheckOO,
									command = lambda: ImageOverlay.show(self))

		self.menubar.add_cascade(label = 'Image',
										menu = self.menuimg)

	def create_roi(self):

		self.menuroi = tk.Menu(self.menubar, tearoff = 0)

		self.menuroi.add_radiobutton(label = 'ROI Image',
									variable = self._menucheckRI,
									value = 0,
									command = lambda: ROIdraw.source(self))
		self.menuroi.add_radiobutton(label = 'ROI Plot',
									variable = self._menucheckRI,
									value = 1,
									command = lambda: ROIdraw.source(self))
		self.menuroi.add_radiobutton(label = 'ROI Filaments',
									variable = self._menucheckRI,
									value = 2,
									command = lambda: ROIdraw.source(self))
		self.menuroi.add_separator()
		self.menuroi.add_checkbutton(label = 'Draw Line',
									underline = 5,
									accelerator = 'Shift+l',
									variable = self._roidrawline,
									command = lambda: ROIdraw.line(self))
		self.menuroi.add_checkbutton(label = 'Draw Circle',
									underline = 5,
									accelerator = 'Shift+c',
									variable = self._roidrawcircle,
									command = lambda: ROIdraw.circle(self))
		self.menuroi.add_checkbutton(label = 'Draw Rectangle',
									underline = 5,
									accelerator = 'Shift+r',
									variable = self._roidrawrect,
									command = lambda: ROIdraw.rectangle(self))
		self.menuroi.add_separator()
		self.menuroi.add_command(label = 'Delete',
								underline = 0,
								accelerator = 'Shift+d',
								command = lambda: ROIimage.keepdelall(self, 0),
								)
		self.menuroi.add_command(label = 'Keep',
								underline = 0,
								accelerator = 'Shift+k',
								command = lambda: ROIimage.keepdelall(self, 1))
		self.menuroi.add_command(label = 'Split',
								underline = 0,
								accelerator = 'Shift+s')
		self.menuroi.add_command(label = 'Merge',
								underline = 0,
								accelerator = 'Shift+m',
								command = lambda: ROIimage.mergeall(self))
		self.menuroi.add_separator()
		self.menuroi.add_checkbutton(label = 'Show ROI Manager',
									variable = self._menucheckRM)
		self.menuroi.add_checkbutton(label = 'Show Fiber Inspector',
									variable = self._menucheckRF)

		self.menubar.add_cascade(label = 'ROI manager',
										menu = self.menuroi)

	def create_massmap(self):

		self.menumass = tk.Menu(self.menubar, tearoff = 0)

		self.menumass.add_checkbutton(label = 'Set Reference',
											variable = self._menucheckMS,
											accelerator = 'Ctrl+r',
											command = lambda: RefMass.set(self))
		self.menumass.add_command(label = 'Reference Manager')
		self.menumass.add_separator()
		self.menumass.add_command(label = 'Calibration',
											command = lambda: RefMass.create_cal(self))
		self.menumass.add_command(label = 'Save Calibration')
		self.menumass.add_separator()
		self.menumass.add_command(label = 'Run',
											command = lambda: RunMass.create(self))

		self.menubar.add_cascade(label = 'Mass Mapping',
									menu = self.menumass)

	def create_stats(self):

		self.menustats = tk.Menu(self.menubar, tearoff = 0)

		self.menubar.add_cascade(label = 'Statistics',
									menu = self.menustats)

	def create_plot(self):

		self.menuplot = tk.Menu(self.menubar, tearoff = 0)

		self.menuplot.add_command(label = 'Line')
		self.menuplot.add_command(label = 'Scatter')
		self.menuplot.add_command(label = 'Bars')
		self.menuplot.add_command(label = '2D map')

		self.menubar.add_cascade(label = 'Plot',
										menu = self.menuplot)

	def create_advanced(self):

		self.menuadvanced = tk.Menu(self.menubar, tearoff = 0)
	
		self.menuadvanced.add_command(label = 'Average MPL over width')
		self.menuadvanced.add_command(label = 'Filament internal packing')
		self.menuadvanced.add_command(label = 'Subunit estimation')

		self.menubar.add_cascade(label = 'Advanced',
										menu = self.menuadvanced)

	def setstate_all(self, menu, set_status):
		nitems = menu.index('end')
		for index in range(nitems+1):
			try:
				menu.entryconfig(menu.entrycget(index, 'label'),
											state = set_status)
			except: pass

	def setstate_init(self):

		MenuAnalysis.setstate_all(self, self.menufile, 'disabled')
		MenuAnalysis.setstate_all(self, self.menuimg, 'disabled')
		MenuAnalysis.setstate_all(self, self.menuroi, 'disabled')
		MenuAnalysis.setstate_all(self, self.menumass, 'disabled')
		#MenuAnalysis.setstate_all(self, self.menustats, 'disabled')
		MenuAnalysis.setstate_all(self, self.menuplot, 'disabled')
		MenuAnalysis.setstate_all(self, self.menuadvanced, 'disabled')

		self.menufile.entryconfig('Load', state = 'normal')
		self.menufile.entryconfig('Quit', state = 'normal')

	def setstate_afterload(self):

		MenuAnalysis.setstate_all(self, self.menufile, 'normal')
		MenuAnalysis.setstate_all(self, self.menuimg, 'normal')
		MenuAnalysis.setstate_all(self, self.menuroi, 'normal')
		MenuAnalysis.setstate_all(self, self.menumass, 'normal')
		MenuAnalysis.setstate_all(self, self.menuplot, 'normal')
		MenuAnalysis.setstate_all(self, self.menuadvanced, 'normal')
		
		self.menuimage.entryconfig('Plot', state = 'disabled')

	def menufile_load(self):

		try:
			FileLoad.load_file(self)
			self._inputdata
			MenuAnalysis.setstate_afterload(self)
		except AttributeError: pass

	def menufile_close(self):

		FileClose.delete_variables(self)
		MenuAnalysis.setstate_init(self)
		MainDisplay.create(self)

class MainDisplay():

	def create(self):

		top = self.winfo_toplevel()
		self.frameMainDisplay = ttk.Frame(top)

		top.columnconfigure(0, weight = 1)
		top.rowconfigure(0, weight = 1)
		self.frameMainDisplay.grid(row = 0, column  = 0,
									sticky = 'nsew', padx = 10, pady = 10)
		self.frameMainDisplay.rowconfigure(1, weight = 1)
		self.frameMainDisplay.columnconfigure(0, weight = 1)
