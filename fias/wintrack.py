import tkinter as tk
from tkinter import ttk

import numpy as np

from menufile_track import FileOpen, FileClose, FileOutput, FileSave
from menusettings_track import SaveParameters, LoadParameters, AdvancedSettings
from menuimage_track import ImageOriginal, ImageInfo, ImageColormap, ImageContrast, ImageOverlay, ROImanager
from controlpanel_track import CImageOptions, CEdgeOptions, CSkeletonDetection, CFilamentTracking, CProfiles

class WindowTracking():

	def __init__(self):
		tk.Frame.__init__(self)
		MenuTracking.init_var(self)
		MenuTracking.create(self)
		MainDisplay.create(self)

		AdvancedSettings.init_var(self)
		ControlPanel.__init__(self)

		WindowTracking.bind_shortcuts(self)

	def bind_shortcuts(self):

		self.bind_all('<Control-q>',
						lambda event, arg = self: WindowTracking.quit(arg, event))

	def restart(self):
		print('to do, wintrack_v1p0,  line 21')
		# to do

	def quit(self, event):

		self.quit()

class MenuTracking():

	def init_var(self):
		self._saving_info = dict()
		self._colormap_options = dict()
		self._menucheckOI = tk.IntVar()
		self._menucheckII = tk.IntVar()
		self._menucheckCI = tk.IntVar()
		self._menucheckCO = tk.IntVar()
		self._menucheckCC = tk.IntVar()
		self._menucheckOO = tk.IntVar()
		self._menucheckROI = tk.IntVar()

		self._menucheckOI.set(0)
		self._menucheckII.set(0)
		self._menucheckCI.set(0)
		self._menucheckCO.set(0)
		self._menucheckCC.set(0)
		self._menucheckCC.set(0)
		self._menucheckOO.set(0)
		self._menucheckROI.set(0)

		ROImanager.init_var(self)
		ImageOverlay.init_var(self)

	def create(self):
		self.menubar = tk.Menu(self.master)
		MenuTracking.create_file(self)
		MenuTracking.create_settings(self)
		MenuTracking.create_image(self)
		MenuTracking.create_export(self)
		MenuTracking.create_window(self)
		MenuTracking.create_help(self)

		self.master.config(menu = self.menubar)

		MenuTracking.setstate_init(self)

	def create_file(self):
		self.menufile = tk.Menu(self.menubar, tearoff = 0)
		self.menufile.add_command(label = 'Open',
												command = lambda: MenuTracking.menufile_open(self))
		self.menufile.add_command(label = 'Close',
												command = lambda: MenuTracking.menufile_close(self))
		self.menufile.add_command(label = 'Output Folder',
												command = lambda: FileOutput.selec_folder(self))
		self.menufilesaving = tk.Menu(self.menufile, tearoff = 0)
		self.menufilesaving.add_radiobutton(label = 'Manual saving')
		self.menufilesaving.add_separator()
		self.menufilesaving.add_radiobutton(label = 'Final Output Only')
		self.menufilesaving.add_radiobutton(label = 'All Tracking Steps')
		self.menufilesaving.add_radiobutton(label = 'Custom')
		self.menufile.add_cascade(label = 'Saving Mode',
												menu = self.menufilesaving)
		self.menufile.add_command(label = 'Save As',
											command = lambda: FileSave.saveas(self))
		self.menufile.add_command(label = 'Restart')
		self.menufile.add_separator()
		self.menufile.add_command(label = 'Quit',
												underline = 0,
												accelerator = 'Ctrl+Q',
												command = self.quit)

		self.menubar.add_cascade(label = 'File',
												menu = self.menufile)

	def create_settings(self):
		self.menusettings = tk.Menu(self.menubar, tearoff  = 0)

		self.menusettings.add_command(label = 'Save Parameters',
									command = lambda: SaveParameters.save_to(self))
		self.menusettings.add_command(label = 'Load Parameters',
									command = lambda: LoadParameters.load(self))
		self.menusettings.add_command(label = 'Advanced Settings',
									command = lambda: AdvancedSettings.create_window(self))
		self.menusettings.add_separator()
		self.menusettings.add_command(label = 'Restore Settings',
									command = lambda: AdvancedSettings.set_initvar(self))

		self.menubar.add_cascade(label = 'Settings',
												menu = self.menusettings)

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
							variable = self._menucheckOI,
							command = lambda: ImageOriginal.show(self))
		self.menuimg.add_checkbutton(label = 'Show Image Information',
							variable = self._menucheckII,
							command = lambda: ImageInfo.show(self))
		self.menuimg.add_cascade(label = 'Colormap', menu = self.menucmap)
		self.menuimg.add_checkbutton(label = 'Adjust Contrast',
							variable = self._menucheckCC,
							command = lambda: ImageContrast.show(self))
		self.menuimg.add_checkbutton(label = 'Overlay Options',
							variable = self._menucheckOO,
							command = lambda: ImageOverlay.show(self))
		self.menuimg.add_checkbutton(label = 'ROI Manager',
							variable = self._menucheckROI,
							command = lambda: MenuTracking.menuimg_roi(self))
		self.menubar.add_cascade(label = 'Image',
												menu = self.menuimg)

	def create_export(self):
		self.menuexport = tk.Menu(self.menubar, tearoff = 0)

	def create_window(self):
		self.menuwin = tk.Menu(self.menubar, tearoff = 0)

	def create_help(self):
		self.menuhelp = tk.Menu(self.menubar, tearoff = 0)

	def setstate_all(self, menu, set_status):
		nitems = menu.index('end')
		for index in range(nitems+1):
			try:
				menu.entryconfig(menu.entrycget(index, 'label'),
											state = set_status)
			except: pass

	def setstate_init(self):

		MenuTracking.setstate_all(self, self.menufile, 'disabled')
		MenuTracking.setstate_all(self, self.menuimg, 'disabled')

		self.menufile.entryconfig('Open', state = 'normal')
		self.menufile.entryconfig('Quit', state = 'normal')

	def setstate_afterload(self):

		MenuTracking.setstate_all(self, self.menufile, 'normal')
		MenuTracking.setstate_all(self, self.menuimg, 'normal')

	def menufile_open(self):
		FileOpen.load_file(self)
		try:
			self._mat_img
			MenuTracking.setstate_afterload(self)
			ControlPanel.setstate_afterload(self)
		except AttributeError: pass

	def menufile_close(self):
		FileClose.delete_info(self)
		FileClose.delete_variables(self)
		MenuTracking.setstate_init(self)
		MainDisplay.create(self)

	def menuimg_roi(self):

		if self._menucheckROI.get() == 1:
			ROImanager.create_window(self)
		else: ROImanager.close(self)


class MainDisplay():

	def create(self):

		top = self.winfo_toplevel()
		self.frameMainDisplay = ttk.Frame(top)

		if self.controlanchor == 1:
			self.frameMainDisplay.grid(row = 0, column = 1,
													sticky = 'nsew', padx = 10, pady = 10)

		elif self.controlanchor == 0:
			top.columnconfigure(0, weight = 1)
			top.rowconfigure(0, weight = 1)
			self.frameMainDisplay.grid(row = 0, column = 0,
													sticky = 'nsew', padx = 10, pady = 10)

		self.frameMainDisplay.rowconfigure(1, weight = 1)
		self.frameMainDisplay.columnconfigure(0, weight = 1)

class ControlPanel():

	def __init__(self):
		ControlPanel.create(self)
		ControlPanel.setstate_init(self)

	def create(self):
		if self.controlanchor == 1: ControlPanel.create_anchor(self)
		elif self.controlanchor == 0: ControlPanel.create_detached(self)

		self.frameControlpanel.grid(row = 0, column = 0,
										sticky ='nsew', padx = 10, pady = 10)

		ControlPanel.createCgeneral(self)
		ControlPanel.createCimg(self)
		ControlPanel.createCedge(self)
		ControlPanel.createCskeleton(self)
		ControlPanel.createCtrack(self)

	def create_anchor(self):
		top = self.winfo_toplevel()
		self.frameControlpanel = ttk.Frame(top)

	def create_detached(self):

		self.wincontrol = tk.Toplevel(self)
		self.wincontrol.title('Control Panel Tracking')
#		self.wincontrol.geometry('300x500-100+50')
		self.wincontrol.resizable(0,0)
		self.wincontrol.protocol('WM_DELETE_WINDOW', self.wincontrol.iconify)
		self.frameControlpanel = ttk.Frame(self.wincontrol)

	def createCgeneral(self):

		self.frameCgeneral = ttk.Frame(self.frameControlpanel)
		self.frameCgeneral.grid(row = 0, column = 0, sticky = 'nsew',
									padx = 5, pady = 5)
		self.frameCgeneral.columnconfigure(0, weight = 1)


		self.progressBar = ttk.Progressbar(self.frameCgeneral,
								orient = 'horizontal')
		self.exprofilesButton = ttk.Button(self.frameCgeneral,
								text = 'Extract Profiles',
								command = lambda:
												ControlPanel.profiles(self))
		self.inspectsegButton = ttk.Button(self.frameCgeneral,
								text = 'Inspect Profiles')
								# command = lambda:
												# ProfilesInspect.create(self))


		self.progressBar.grid(row = 0, column = 0, sticky = 'nsew',
								pady = 2)
		self.exprofilesButton.grid(row = 1, column = 0, sticky = 'nsew',
								pady = 2)
		self.inspectsegButton.grid(row = 2, column = 0, sticky = 'nsew',
								pady = 2)

	def createCimg(self):

		self.frameCimg = ttk.LabelFrame(self.frameControlpanel,
								text = 'Image options')
		self.frameCimg.grid(row = 1, column = 0, sticky = 'nsew',
								padx = 5, pady = 5)
		self.frameCimg.columnconfigure([0,1,2], weight = 1)

		self.imgsizeLabel = ttk.Label(self.frameCimg,
								  text = 'Size (nm) : ')
		self.imgsizeEntry = ttk.Entry(self.frameCimg,
								  width = 6)
		self.imgsizeEntry.bind('<Return>',
								 lambda event, arg = self:
												ControlPanel.update_cal(arg, event))
		self.imgresetButton = ttk.Button(self.frameCimg,
									 text = 'Reset',
									 command = lambda:
													ControlPanel.image_reset(self))
		self.imgcropinfoButton = ttk.Button(self.frameCimg,
										 text = 'Crop Info Strip',
										 command = lambda:
														 ControlPanel.crop_infostrip(self))
		self.imgcropselecButton = ttk.Button(self.frameCimg,
										   text = 'Crop from selection',
										   command = lambda:
															ControlPanel.crop_selection(self))

		self.imgsizeLabel.grid(row = 0, column = 0, sticky = 'nsew',
								padx = 2, pady = 2)
		self.imgsizeEntry.grid(row = 0, column = 1, sticky = 'nsew',
								padx = 2, pady = 2)
		self.imgresetButton.grid(row = 0, column = 2, sticky = 'nsew',
									padx = 2, pady = 2)
		self.imgcropinfoButton.grid(row = 1, column = 0, sticky = 'nsew',
										columnspan = 2,
										padx = 2, pady = 2)
		self.imgcropselecButton.grid(row = 1, column = 2, sticky = 'nsew',
										  padx = 2, pady = 2)

	def createCedge(self):

		self.frameCedge = ttk.LabelFrame(self.frameControlpanel,
									text = 'Edge detection')
		self.frameCedge.grid(row = 2, column = 0, sticky = 'nsew',
								padx = 5, pady = 5)
		self.frameCedge.columnconfigure([0,1,2], weight = 1)

		self.erunButton = ttk.Button(self.frameCedge,
								text = 'Run',
								command = lambda:
												ControlPanel.edge_run(self))
		self.eshowButton = ttk.Button(self.frameCedge,
								  text = 'Show',
								  command = lambda:
												 CEdgeOptions.show(self))
		self.ethlowLabel = ttk.Label(self.frameCedge,
								text = 'Threshold Low: ')
		self.ethlowSpinbox = tk.Spinbox(self.frameCedge,
									width = 10,
									command = lambda:
													CEdgeOptions.update_ethlow(self, '<Button-1>'))
		self.ethlowSpinbox.config(from_=0, to = 1,
									increment = 0.001,
									textvariable = self._tracking_settings['edge_thlow'])
		self.ethlowSpinbox.bind('<Return>',
									lambda event, arg = self:
												CEdgeOptions.update_ethlow(arg, event))
		self.ethhighLabel = ttk.Label(self.frameCedge,
								 text = 'Threshold High: ')
		self.ethhighSpinbox = tk.Spinbox(self.frameCedge,
									 width = 10,
									 command = lambda:
													CEdgeOptions.update_ethhigh(self, '<Button-1>'))
		self.ethhighSpinbox.config(from_=0, to = 1,
									increment = 0.001,
									 textvariable = self._tracking_settings['edge_thhigh'])
		self.ethhighSpinbox.bind('<Return>',
									lambda event, arg = self:
												CEdgeOptions.update_ethhigh(arg, event))
		self.ethupCheckbutton = ttk.Checkbutton(self.frameCedge,
										text = 'Enable upper limit: ',
										variable = self._tracking_settings['edge_thup_use'],
										command = lambda: CEdgeOptions.enable_thup(self))
		self.ethupSpinbox = tk.Spinbox(self.frameCedge,
										width = 10,
										command = lambda:
													CEdgeOptions.update_ethup(self, '<Button-1>'))
		self.ethupSpinbox.config(from_=0, to = 1,
									increment = 0.001,
									textvariable = self._tracking_settings['edge_thup'])
		self.ethupSpinbox.bind('<Return>',
									lambda event, arg = self:
												CEdgeOptions.update_ethup(arg, event))


		self.erunButton.grid(row = 0, column = 0, sticky = 'nsew',
							   padx = 2, pady = 2)
		self.eshowButton.grid(row = 1, column = 0, sticky = 'nsew',
								 padx = 2, pady = 2)
		self.ethlowLabel.grid(row = 0, column = 1, sticky = 'nsew',
								padx = 2, pady = 2)
		self.ethlowSpinbox.grid(row = 0, column = 2, sticky = 'nsew',
									padx = 2, pady = 2)
		self.ethhighLabel.grid(row = 1, column = 1, sticky = 'nsew',
								 padx = 2, pady = 2)
		self.ethhighSpinbox.grid(row = 1, column = 2, sticky = 'nsew',
									 padx = 2, pady = 2)
		self.ethupCheckbutton.grid(row = 2, column = 0, sticky = 'nsew',
									columnspan = 2,
									padx = 2, pady = 2)
		self.ethupSpinbox.grid(row = 2, column = 2, sticky = 'nsew',
									padx = 2, pady = 2)

	def createCskeleton(self):

		self.frameCskeleton = ttk.LabelFrame(self.frameControlpanel,
									  text = 'Skeleton detection')
		self.frameCskeleton.grid(row = 3, column = 0, sticky = 'nsew',
									 padx = 5, pady = 5)
		self.frameCskeleton.columnconfigure([0,1,2], weight = 1)


		self.skthFrame = ttk.Frame(self.frameCskeleton)
		self.skthFrame.columnconfigure(1, weight = 1)
		self.skfilterButton = ttk.Button(self.frameCskeleton,
								  text = 'Filter',
								  command = lambda:
													ControlPanel.filter_run(self))
		self.skmaskButton = ttk.Button(self.frameCskeleton,
									text = 'Mask',
									command = lambda:
													ControlPanel.mask(self))
		self.skskeletonButton = ttk.Button(self.frameCskeleton,
										text = 'Skeleton',
										command = lambda:
														ControlPanel.skeleton(self))
		self.skthLabel = ttk.Label(self.skthFrame,
							 text = 'Threshold: ')
		self.skthSlider = tk.Scale(self.skthFrame,
							 orient = 'horizontal')
		self.skthSlider.bind('<ButtonRelease-1>',
									lambda event, arg = self:
												CSkeletonDetection.update_filterth(arg, event))


		self.skfilterButton.grid(row = 0, column = 0, sticky = 'nsew',
								 padx = 2, pady = 2)
		self.skmaskButton.grid(row = 0, column = 1, sticky = 'nsew',
								   padx = 2, pady = 2)
		self.skskeletonButton.grid(row = 0, column = 2, sticky = 'nsew',
									   padx = 2, pady = 2)
		self.skthFrame.grid(row = 1, column = 0, sticky = 'nsew',
							 columnspan = 3)
		self.skthLabel.grid(row = 0, column = 0, sticky = 'nsew',
							padx = 2, pady = 2)
		self.skthSlider.grid(row = 0, column = 1, sticky = 'nsew',
							padx = 2, pady = 2)

	def createCtrack(self):

		self.frameCtrack = ttk.LabelFrame(self.frameControlpanel,
										text = 'Filament Tracking')
		self.frameCtrack.grid(row = 4, column = 0, sticky = 'nsew',
								padx = 5, pady = 5)
		self.frameCtrack.columnconfigure([0,1], weight = 1)


		self.tlabelButton = ttk.Button(self.frameCtrack,
								text = 'Track & Label',
								command = lambda:
												  ControlPanel.tracking(self))
		self.tshowlabelButton = ttk.Button(self.frameCtrack,
										text = 'Show Labels',
										command = lambda:
														CFilamentTracking.show_track(self))
		self.tfitButton = ttk.Button(self.frameCtrack,
							text = 'Local Fit',
							command = lambda:
											ControlPanel.localfit(self))
		self.tshowfitButton = ttk.Button(self.frameCtrack,
									text = 'Show Fit',
									command = lambda:
													CFilamentTracking.show_localfit(self))


		self.tlabelButton.grid(row = 0, column = 0, sticky = 'nsew',
								padx = 2, pady = 2)
		self.tshowlabelButton.grid(row = 0, column = 1, sticky = 'nsew',
									   padx = 2, pady = 2)
		self.tfitButton.grid(row = 1, column = 0, sticky = 'nsew',
							padx = 2, pady = 2)
		self.tshowfitButton.grid(row = 1, column = 1, sticky = 'nsew',
								   padx = 2, pady = 2)

	def update_cal(self, event):
		CImageOptions.update_cal(self, event)
		try:
			self._cal_factor
			ControlPanel.setstate_aftercal(self)
		except AttributeError: pass

	def crop_infostrip(self):
		CImageOptions.crop_infostrip(self)
		ControlPanel.setstate_aftercrop(self)

	def crop_selection(self):
		CImageOptions.crop_selection(self)
		ControlPanel.setstate_aftercrop(self)

	def image_reset(self):
		CImageOptions.reset(self)

		self.imgresetButton.state(['disabled'])
		ControlPanel.setstate_init(self)
		ControlPanel.setstate_afterload(self)
		ControlPanel.setstate_aftercal(self)

		self._tracking_step = 1

	def edge_run(self):
		CEdgeOptions.run(self)
		ControlPanel.setstate_afteredge(self)

	def filter_run(self):
		if self.skfilterButton.cget('text') == 'Filter':
			CSkeletonDetection.runfilter(self)
			ControlPanel.setstate_afterfilter(self)
		elif self.skfilterButton.cget('text') == 'Hide':
			CSkeletonDetection.showfilter(self)

	def mask(self):
		if self.skmaskButton.cget('text') == 'Mask':
			CSkeletonDetection.runmask(self)
			ControlPanel.setstate_aftermask(self)
		elif self.skmaskButton.cget('text') == 'Hide':
			CSkeletonDetection.showmask(self, show_mask = 0)

	def skeleton(self):
		if self.skskeletonButton.cget('text') == 'Skeleton':
			CSkeletonDetection.runskeleton(self)
			ControlPanel.setstate_afterskeleton(self)
		elif self.skskeletonButton.cget('text') == 'Hide':
			CSkeletonDetection.showskeleton(self)

	def tracking(self):
		CFilamentTracking.tracklabel(self)
		ControlPanel.setstate_aftertrack(self)

	def localfit(self):
		CFilamentTracking.localfit(self)
		ControlPanel.setstate_afterfit(self)

	def profiles(self):

		CProfiles.run(self)
		ControlPanel.setstate_afterprofiles(self)
		ControlPanel.create_fepopup(self)

	def create_fepopup(self):

		try: self._fe_Window.destroy()
		except AttributeError: pass

		self._fe_Window = tk.Toplevel(self)
		self._fe_Window.title('Info')
		self._fe_Window.geometry('200x100+200+200')
		self._fe_Window.resizable(0,0)

		self._fe_Window.rowconfigure(0, weight = 1)
		self._fe_Window.columnconfigure(0, weight = 1)

		msg_finish = 'Finish Extracting Profiles\n'\
							+ 'Number of Filaments Found: '\
							+ str(len(np.unique(self._fiber_number)))

		self._feFrame = ttk.Frame(self._fe_Window)
		self._feLabel = ttk.Label(self._feFrame, text = msg_finish,
								wraplength = 200, justify = 'center')
		self._fecloseButton = ttk.Button(self._feFrame, text = 'Close',
								width = 20,
								command = lambda: self._fe_Window.destroy())

		self._feFrame.rowconfigure(0, weight = 1)
		self._feFrame.columnconfigure([0,1], weight = 1)

		self._feFrame.grid(row = 0, column = 0,
								sticky = 'nsew', padx = 2, pady = 2)
		self._feLabel.grid(row = 0, column = 0,
								sticky = 'nsew', padx = 2, pady = 2)
		self._fecloseButton.grid(row = 1, column = 0)

	def setstate_init(self):

		self.exprofilesButton.state(['disabled'])
		self.inspectsegButton.state(['disabled'])

		self.imgsizeEntry.state(['disabled'])
		self.imgresetButton.state(['disabled'])
		self.imgcropinfoButton.state(['disabled'])
		self.imgcropselecButton.state(['disabled'])

		self.erunButton.state(['disabled'])
		self.eshowButton.state(['disabled'])
		self.ethlowSpinbox.config(state = 'disabled')
		self.ethhighSpinbox.config(state = 'disabled')
		self.ethupCheckbutton.config(state = 'disabled')
		self.ethupSpinbox.config(state = 'disabled')

		self.skfilterButton.state(['disabled'])
		self.skmaskButton.state(['disabled'])
		self.skskeletonButton.state(['disabled'])
		self.skthSlider.config(state = 'disabled')

		self.tlabelButton.state(['disabled'])
		self.tshowlabelButton.state(['disabled'])
		self.tfitButton.state(['disabled'])
		self.tshowfitButton.state(['disabled'])

	def setstate_afterload(self):
		self.imgsizeEntry.state(['!disabled'])

	def setstate_aftercal(self):

		self.imgcropinfoButton.state(['!disabled'])
		self.imgcropselecButton.state(['!disabled'])
		self.exprofilesButton.state(['!disabled'])

	def setstate_aftercrop(self):
		self.imgcropinfoButton.state(['disabled'])
		self.imgresetButton.state(['!disabled'])

		self.ethhighSpinbox.config(state = 'normal')
		self.ethlowSpinbox.config(state = 'normal')
		self.ethupCheckbutton.config(state = 'normal')
		self.erunButton.state(['!disabled'])

		self.skfilterButton.state(['!disabled'])

	def setstate_afteredge(self):
		self.progressBar['value'] = 0
		self.progressBar.update()
		self.eshowButton.state(['!disabled'])

	def setstate_afterfilter(self):

		self.skmaskButton.state(['!disabled'])
		self.skthSlider.config(state='normal')

		th_min = np.min(self._filter_image.flatten())
		th_max = np.max(self._filter_image.flatten())
		try:
			th_mean = np.mean(self._filter_image[self._mask_edge>0].flatten())
		except AttributeError:
			th_mean = np.mean(self._filter_image.flatten())

		self._tracking_settings['mask_th'].set(int(th_mean))

		self.skthSlider.config(from_=th_min, to = th_max, resolution = 0.001*(th_max-th_min))
		self.skthSlider.set(self._tracking_settings['mask_th'].get())

		self.eshowButton.config(text = 'Show')

	def setstate_aftermask(self):
		self.eshowButton.config(text = 'Show')
		self.skskeletonButton.state(['!disabled'])

	def setstate_afterskeleton(self):
		self.tlabelButton.state(['!disabled'])
		self.skfilterButton.config(text = 'Filter')
		self.skmaskButton.config(text = 'Mask')

	def setstate_aftertrack(self):
		self.tshowlabelButton.state(['!disabled'])
		self.tfitButton.state(['!disabled'])
		self.eshowButton.config(text = 'Show')
		self.skfilterButton.config(text = 'Filter')
		self.skskeletonButton.config(text = 'Skeleton')

	def setstate_afterfit(self):

		self.tshowfitButton.state(['!disabled'])

		self.eshowButton.config(text = 'Show')
		self.skfilterButton.config(text = 'Filter')
		self.skskeletonButton.config(text = 'Skeleton')

		self.tshowlabelButton.config(text = 'Show Labels')

	def setstate_afterprofiles(self):

		self.exprofilesButton.state(['!disabled'])
		self.inspectsegButton.state(['!disabled'])
