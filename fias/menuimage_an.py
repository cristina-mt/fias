import tkinter as tk
from tkinter import ttk

import numpy as np
from itertools import product

from display_an import CMdisplay, Cdisplay, MainDisplay

class ImageColormap():

	def invert(self):

		if self._menucheckCI.get() == 1:
			colormap = self._colormap_options.get('Current Main')+'_r'
		elif self._menucheckCI.get() == 0:
			colormap = self._colormap_options.get('Current Main').replace('_r','')

		self._colormap_options['Current Main'] = colormap
		self._s_img.set_cmap(colormap)
		self._canvas.draw()

	def change(self):

		colormap_option = self._menucheckCO.get()

		if colormap_option == 0: colormap = 'gray'
		elif colormap_option == 1: colormap = 'bone'
		elif colormap_option == 2: colormap  = 'hot'
		elif colormap_option == 3: colormap = 'magma'
		elif colormap_option == 4: colormap = 'inferno'

		self._colormap_options['Current Main'] = colormap

		ImageColormap.invert(self)

	def other(self):

		colormap = self._colormap_options.get('Current Main')

		if 'gray' in colormap : colormap_option = 0
		elif 'bone' in colormap: colormap_option = 1
		elif 'hot' in colormap: colormap_option = 2
		elif 'magma' in colormap: colormap_option = 3
		elif 'inferno' in colormap: colormap_option = 4
		else: colormap_option = 5

		self._menucheckCO.set(colormap_option)
		ImageColormap.other_create(self)

	def other_create(self):

		try: self.ico_Window.destroy()
		except AttributeError: pass

		self.ico_Window = tk.Toplevel(self)
		self.ico_Window.title('Other Colormap')

		self.ico_frame = ttk.Frame(self.ico_Window)
		self.ico_frame.grid(row = 0, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.ico_buttonFrame = ttk.Frame(self.ico_Window)

		CMdisplay.show_colormaps(self)

		self.ico_combobox = ttk.Combobox(self.ico_frame,
										values = self._colormap_options['Available'])
		self.ico_combobox.set(self._colormap_options.get('Current Main').replace('_r',''))
		self.ico_applyButton = ttk.Button(self.ico_buttonFrame, text = 'Apply',
									command = lambda: ImageColormap.other_apply(self))
		self.ico_okButton = ttk.Button(self.ico_buttonFrame, text = 'OK',
									command = lambda: ImageColormap.other_ok(self))

		self.ico_combobox.grid(row = 1, column = 0)
		self.ico_buttonFrame.grid(row = 2, column = 0)
		self.ico_applyButton.grid(row = 0, column = 0)
		self.ico_okButton.grid(row = 0, column = 1)

	def other_apply(self):

		self._colormap_options['Current Main'] = self.ico_combobox.get()
		self._menucheckCO.set(5)
		ImageColormap.invert(self)

	def other_ok(self):

		ImageColormap.other_apply(self)

		self.ico_Window.destroy()
		try: self._ic_canvas.delete(ALL)
		except AttributeError: pass

		self._menucheckCO.set(5)

class ImageContrast():

	def show(self):

		if self._menucheckCC.get() == 1:
			ImageContrast.create(self)
		elif self._menucheckCC.get() == 0:
			ImageContrast.close(self)

	def create(self):

		try: self.ic_Window.destroy()
		except AttributeError: pass

		self.ic_Window = tk.Toplevel(self)
		self.ic_Window.title('Adjust Contrast')
		self.ic_Window.geometry('300x300-100+200')
		self.ic_Window.protocol('WM_DELETE_WINDOW',
								lambda: ImageContrast.close(self))

		try:
			vmin = self._colormap_options['Vmin']
			vmax = self._colormap_options['Vmax']
		except KeyError:
			vmin = np.min(self._inputdata['mat_img'].flatten())
			vmax = np.max(self._inputdata['mat_img'].flatten())


		self.ic_frame = ttk.Frame(self.ic_Window)
		self.ic_controlFrame = ttk.Frame(self.ic_Window)
		self.ic_buttonFrame = ttk.Frame(self.ic_Window)
		self.ic_frame.grid(row = 0, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.ic_controlFrame.grid(row = 1, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.ic_buttonFrame.grid(row = 2, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)

		self.ic_Window.rowconfigure([0,1,2], weight = 1)
		self.ic_Window.columnconfigure(0, weight = 1)
		self.ic_frame.columnconfigure(0, weight = 1)
		self.ic_frame.rowconfigure(0, weight = 1)
		self.ic_controlFrame.columnconfigure(0, weight = 1)
		self.ic_buttonFrame.columnconfigure([0,1], weight = 1)

		self.ic_vminSlider = tk.Scale(self.ic_controlFrame, orient = 'horizontal',
											from_ = np.min(self._inputdata['mat_img'].flatten()), to = np.max(self._inputdata['mat_img'].flatten()))
		self.ic_vmaxSlider = tk.Scale(self.ic_controlFrame, orient = 'horizontal',
											from_ = np.min(self._inputdata['mat_img'].flatten()), to = np.max(self._inputdata['mat_img'].flatten()))
		self.ic_applyButton = ttk.Button(self.ic_buttonFrame, text = 'Apply',
										command = lambda: ImageContrast.ok_close(self))
		self.ic_closeButton = ttk.Button(self.ic_buttonFrame, text = 'Close',
										command = lambda: ImageContrast.close(self))

		self.ic_vminSlider.bind('<ButtonRelease-1>',
										lambda event, arg = self: ImageContrast.change_slide(arg, event))
		self.ic_vmaxSlider.bind('<ButtonRelease-1>',
										lambda event, arg = self: ImageContrast.change_slide(arg, event))

		self.ic_vminSlider.grid(row = 0, column = 0,
										sticky = 'nsew', padx = 2, pady = 2)
		self.ic_vmaxSlider.grid(row = 1, column = 0,
										sticky = 'nsew', padx = 2, pady = 2)
		self.ic_applyButton.grid(row = 0, column = 0,
										sticky = 'nsew', padx = 10, pady = 2)
		self.ic_closeButton.grid(row = 0, column = 1,
										sticky = 'nsew', padx = 10, pady = 2)

		self.ic_vminSlider.set(vmin)
		self.ic_vmaxSlider.set(vmax)

		Cdisplay.show_histogram(self)
		Cdisplay.update_clim(self)

	def change_slide(self, event):

		if self.ic_vminSlider.cget('state') == 'active':
			self.ic_vminSlider.after(100)
		elif self.ic_vmaxSlider.cget('state') == 'active':
			self.ic_vmaxSlider.after(100)

		vmin = self.ic_vminSlider.get()
		vmax = self.ic_vmaxSlider.get()

		Cdisplay.update_clim(self)

	def ok_close(self):

		vmin = self.ic_vminSlider.get()
		vmax = self.ic_vmaxSlider.get()

		self._colormap_options['Vmin'] = vmin
		self._colormap_options['Vmax'] = vmax

		ImageContrast.close(self)

	def close(self):

		try:
			vmin = self._colormap_options['Vmin']
			vmax = self._colormap_options['Vmax']
		except KeyError:
			vmin = np.min(self._inputdata['mat_img'].flatten())
			vmax = np.max(self._inputdata['mat_img'].flatten())

		self._s_img.set_clim([vmin, vmax])
		self._canvas.draw()

		try: self.ic_Window.destroy()
		except AttributeError: pass

		self._menucheckCC.set(0)

class ImageOverlay():

	def init_var(self):

		self._overimg = {
								'enable': tk.IntVar()}
		
		self._overecolor = {
								   'Basic': ['none',
								   			'black',
											'gray',
											'white',
											'yellow',
											'orange',
											'red',
											'magenta',
											'blue',
											'cyan',
											'green',
											]
									}
		self._oversfcolor = {
									'Basic': ['none',
											'fiber number',
								   			'black',
											'gray',
											'white',
											'yellow',
											'orange',
											'red',
											'magenta',
											'blue',
											'cyan',
											'green',
											]

							}

		self._overefcolor = {
									'Basic': ['none',
											'fiber number',
											'edge strength',
								   			'black',
											'gray',
											'white',
											'yellow',
											'orange',
											'red',
											'magenta',
											'blue',
											'cyan',
											'green',
											]

							}

		self._overedge = {
									'enable': tk.IntVar(),
									'size' : tk.StringVar(),
									'ecolor': tk.StringVar(),
									'fcolor': tk.StringVar()
									}

		self._overskel = {
									'enable': tk.IntVar(),
									'size' : tk.StringVar(),
									'ecolor': tk.StringVar(),
									'fcolor': tk.StringVar()
									}

		self._overimg['enable'].set(0)
		self._overedge['enable'].set(0)
		self._overedge['size'].set('2')
		self._overedge['ecolor'].set('none')
		self._overedge['fcolor'].set('orange')
		self._overskel['enable'].set(0)
		self._overskel['size'].set('2')
		self._overskel['ecolor'].set('none')
		self._overskel['fcolor'].set('cyan')

	def show(self):
		if self._menucheckOO.get() == 1:
			ImageOverlay.create_options(self)
			ImageOverlay.setstate_init(self)
		else: ImageOverlay.close(self)

	def create_options(self):

		try: self.ov_Window.destroy()
		except AttributeError: pass

		self.ov_Window = tk.Toplevel(self)
		self.ov_Window.title('Display Overlay Options')
		self.ov_Window.resizable(0,0)
		self.ov_Window.protocol('WM_DELETE_WINDOW',
								lambda: ImageOverlay.close(self))

		self.ov_Window.rowconfigure([0,1,2,3,4,5], weight = 1)
		self.ov_Window.columnconfigure(0, weight = 1)

		self.oveLabelFrame = ttk.LabelFrame(self.ov_Window,
												text = 'Edge Options')
		self.ovsLabelFrame = ttk.LabelFrame(self.ov_Window,
												text = 'Skeleton Options')
		self.ovbuttonFrame = ttk.Frame(self.ov_Window)

		self.ove_enButton = ttk.Button(self.oveLabelFrame,
											text = 'Enable',
											style = 'SunkableButton.TButton',
											command = lambda: ImageOverlay.enable_edge(self))
		self.ove_szLabel = ttk.Label(self.oveLabelFrame,
											text = 'Size : ')
		self.ove_szSpinbox = tk.Spinbox(self.oveLabelFrame,
											width = 3)
		self.ove_szSpinbox.delete(0,'end')
		self.ove_szSpinbox.insert(0, self._overedge['size'].get())

		self.ove_ecLabel = ttk.Label(self.oveLabelFrame,
											text = 'Edge color : ')
		self.ove_ecCombobox = ttk.Combobox(self.oveLabelFrame,
											width  = 7,
											values = self._overecolor['Basic'])
		self.ove_ecCombobox.set(self._overedge['ecolor'].get())
		self.ove_fcLabel = ttk.Label(self.oveLabelFrame,
											text = 'Face color: ')
		self.ove_fcCombobox = ttk.Combobox(self.oveLabelFrame,
											width = 7,
											values = self._overefcolor['Basic'])
		self.ove_fcCombobox.set(self._overedge['fcolor'].get())

		self.ovs_enButton = ttk.Button(self.ovsLabelFrame,
											text = 'Enable',
											style = 'SunkableButton.TButton',
											command = lambda: ImageOverlay.enable_skeleton(self))
		self.ovs_szLabel = ttk.Label(self.ovsLabelFrame,
											text = 'Size : ')
		self.ovs_szSpinbox = tk.Spinbox(self.ovsLabelFrame,
											width = 3)
		self.ovs_szSpinbox.delete(0,'end')
		self.ovs_szSpinbox.insert(0, self._overskel['size'].get())

		self.ovs_ecLabel = ttk.Label(self.ovsLabelFrame,
											text = 'Edge color : ')
		self.ovs_ecCombobox = ttk.Combobox(self.ovsLabelFrame,
											width  = 7,
											values = self._overecolor['Basic'])
		self.ovs_ecCombobox.set(self._overskel['ecolor'].get())
		self.ovs_fcLabel = ttk.Label(self.ovsLabelFrame,
											text = 'Face color: ')
		self.ovs_fcCombobox = ttk.Combobox(self.ovsLabelFrame,
											width = 7,
											values = self._oversfcolor['Basic'])
		self.ovs_fcCombobox.set(self._overskel['fcolor'].get())


		self.ovapplyButton = ttk.Button(self.ovbuttonFrame,
											text = 'Apply',
											command = lambda: ImageOverlay.apply(self))
		self.ovcloseButton = ttk.Button(self.ovbuttonFrame,
											text = 'Close',
											command = lambda: ImageOverlay.close(self))

		self.oveLabelFrame.rowconfigure(0, weight = 1)
		self.ovsLabelFrame.rowconfigure(0, weight = 1)
		self.ovbuttonFrame.columnconfigure([0,1], weight = 1)


		self.oveLabelFrame.grid(row = 1, column = 0, sticky = 'nsew',
											padx = 2, pady = 2)
		self.ovsLabelFrame.grid(row = 2, column = 0, sticky = 'nsew',
											padx = 2, pady = 2)
		self.ovbuttonFrame.grid(row = 5, column = 0, sticky = 'nsew',
											padx = 2, pady = 2)

		self.ove_enButton.grid(row = 0, column = 0, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ove_szLabel.grid(row = 0, column = 1, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ove_szSpinbox.grid(row = 0, column = 2, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ove_ecLabel.grid(row = 0, column = 3, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ove_ecCombobox.grid(row = 0, column = 4, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ove_fcLabel.grid(row = 0, column = 5, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ove_fcCombobox.grid(row = 0, column = 6, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovs_enButton.grid(row = 0, column = 0, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovs_szLabel.grid(row = 0, column = 1, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovs_szSpinbox.grid(row = 0, column = 2, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovs_ecLabel.grid(row = 0, column = 3, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovs_ecCombobox.grid(row = 0, column = 4, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovs_fcLabel.grid(row = 0, column = 5, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovs_fcCombobox.grid(row = 0, column = 6, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovapplyButton.grid(row = 0, column = 0, sticky = 'snew',
												padx = 50, pady = 2)
		self.ovcloseButton.grid(row = 0, column = 1, sticky = 'nsew',
												padx = 50, pady = 2)

	def setstate_init(self):

		try: self._inputdata['fiber_xc']
		except KeyError: self._overskel['enable'].set(0)

		try: self._inputdata['fiber_x1']
		except KeyError: self._overedge['enable'].set(0)

		if self._overedge['enable'].get() == 1:
			self.ove_enButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)

		if self._overskel['enable'].get() == 1:
			self.ovs_enButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)

	def enable_edge(self):
		if self._overedge['enable'].get() == 1:
			self.ove_enButton.state(['!pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.RAISED)
			self._overedge['enable'].set(0)
		elif self._overedge['enable'].get() == 0:
			self.ove_enButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)
			self._overedge['enable'].set(1)

	def enable_skeleton(self):
		if self._overskel['enable'].get() == 1:
			self.ovs_enButton.state(['!pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.RAISED)
			self._overskel['enable'].set(0)
		elif self._overskel['enable'].get() == 0:
			self.ovs_enButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)
			self._overskel['enable'].set(1)

	def apply(self):
		self._overedge['size'].set(self.ove_szSpinbox.get())
		self._overedge['ecolor'].set(self.ove_ecCombobox.get())
		self._overedge['fcolor'].set(self.ove_fcCombobox.get())
		self._overskel['size'].set(self.ovs_szSpinbox.get())
		self._overskel['ecolor'].set(self.ovs_ecCombobox.get())
		self._overskel['fcolor'].set(self.ovs_fcCombobox.get())


		MainDisplay.show_overlay(self)
		#try: ROIdisplay.show_roi(self)
		#except AttributeError: pass

	def close(self):

		self.ov_Window.destroy()
		self._menucheckOO.set(0)




