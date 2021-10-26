import tkinter as tk
from tkinter import ttk

import numpy as np
from itertools import product

from display_track import OIdisplay, CMdisplay, Cdisplay, ROIdisplay, MainDisplay

class ImageOriginal():

	def create_window(self):

		try: self.iot_Window.destroy()
		except AttributeError: pass

		self.iot_Window = tk.Toplevel(self)
		self.iot_Window.title('Original Image')
		self.iot_Window.geometry('600x400+100+100')
		self.iot_Window.protocol('WM_DELETE_WINDOW',
								lambda: ImageOriginal.close(self))

		self.iot_Window.rowconfigure(0, weight = 1)
		self.iot_Window.columnconfigure(0, weight = 1)

		self.iot_frameMain = ttk.Frame(self.iot_Window)
		self.iot_frameMain.rowconfigure(1, weight = 1)
		self.iot_frameMain.columnconfigure(0, weight = 1)
		self.iot_frameMain.grid(row = 0, column = 0,
											sticky = 'nsew',
											padx = 10, pady = 10)

	def show(self):

		if self._menucheckOI.get() == 1:
			ImageOriginal.create_window(self)
			OIdisplay.init_canvas(self)
			OIdisplay.show_image(self)
		elif self._menucheckOI.get() == 0:
			try: self.iot_Window.destroy()
			except AttributeError: pass
			OIdisplay.hide_delete(self)

	def close(self):
		self.iot_Window.destroy()
		self._menucheckOI.set(0)

class ImageInfo():

	def create_window(self):
		try: self.iit_Window.destroy()
		except AttributeError: pass

		self.iit_Window = tk.Toplevel(self)
		self.iit_Window.title('Image Info')
		#self.iit_Window.geometry('300x360-100-100')
		self.iit_Window.resizable(0,0)
		self.iit_Window.protocol('WM_DELETE_WINDOW',
								lambda: ImageInfo.close(self))

		self.iit_frame = ttk.Frame(self.iit_Window)
		self.iit_frame.grid(row = 0, column = 0,
									sticky = 'nsew',
									padx = 2, pady = 2)

		self.iit_filedirLabel = ttk.Label(self.iit_frame, text = 'Folder: ')
		self.iit_filenameLabel = ttk.Label(self.iit_frame, text = 'File: ')
		self.iit_typeLabel = ttk.Label(self.iit_frame, text = 'Type: ')
		self.iit_sizepixxLabel = ttk.Label(self.iit_frame, text = 'Size X (pix) :')
		self.iit_sizepixyLabel = ttk.Label(self.iit_frame, text = 'Size Y (pix) : ')
		self.iit_sizenmxLabel = ttk.Label(self.iit_frame, text = 'Size X (nm) : ')
		self.iit_sizenmyLabel = ttk.Label(self.iit_frame, text = 'Size Y (nm) : ')
		self.iit_calfactorLabel = ttk.Label(self.iit_frame, text = 'Cal. Factor (nm/pix) : ')
		self.iit_vminLabel = ttk.Label(self.iit_frame, text = 'I min: ')
		self.iit_vmaxLabel = ttk.Label(self.iit_frame, text = 'I max: ')
		self.iit_xminLabel = ttk.Label(self.iit_frame, text = 'X min: ')
		self.iit_xmaxLabel = ttk.Label(self.iit_frame, text = 'X max: ')
		self.iit_yminLabel = ttk.Label(self.iit_frame, text = 'Y min: ')
		self.iit_ymaxLabel = ttk.Label(self.iit_frame, text = 'Y max: ')

		self.iit_filedirDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._file_info['directory'],
										wraplength = 160)
		self.iit_filenameDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._file_info['file'],
										wraplength = 160)
		self.iit_typeDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['type'])
		self.iit_sizepixxDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['sizepix_x'])
		self.iit_sizepixyDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['sizepix_y'])
		self.iit_sizenmxDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['sizenm_x'])
		self.iit_sizenmyDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['sizenm_y'])
		self.iit_calfactorDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['cal_factor'])
		self.iit_vminDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['vmin'])
		self.iit_vmaxDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['vmax'])
		self.iit_xminDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['xmin'])
		self.iit_xmaxDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['xmax'])
		self.iit_yminDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['ymin'])
		self.iit_ymaxDynLabel = ttk.Label(self.iit_frame,
										textvariable = self._img_info['ymax'])

		self.iit_filedirLabel.grid(row = 0, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_filenameLabel.grid(row = 1, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_typeLabel.grid(row = 2, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_sizepixxLabel.grid(row = 3, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_sizepixyLabel.grid(row = 4, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_sizenmxLabel.grid(row = 5, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_sizenmyLabel.grid(row = 6, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_calfactorLabel.grid(row = 7, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_vminLabel.grid(row = 8, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_vmaxLabel.grid(row = 9, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_xminLabel.grid(row = 10, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_xmaxLabel.grid(row = 11, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_yminLabel.grid(row = 12, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_ymaxLabel.grid(row = 13, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)

		self.iit_filedirDynLabel.grid(row = 0, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_filenameDynLabel.grid(row = 1, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_typeDynLabel.grid(row = 2, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_sizepixxDynLabel.grid(row = 3, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_sizepixyDynLabel.grid(row = 4, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_sizenmxDynLabel.grid(row = 5, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_sizenmyDynLabel.grid(row = 6, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_calfactorDynLabel.grid(row = 7, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_vminDynLabel.grid(row = 8, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_vmaxDynLabel.grid(row = 9, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_xminDynLabel.grid(row = 10, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_xmaxDynLabel.grid(row = 11, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_yminDynLabel.grid(row = 12, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)
		self.iit_ymaxDynLabel.grid(row = 13, column = 1,
									sticky = 'nsew', padx = 2, pady = 2)

	def show(self):

		if self._menucheckII.get() == 1:
			ImageInfo.create_window(self)
		elif self._menucheckII.get() == 0:
			try: self.iit_Window.destroy()
			except AttributeError: pass

	def close(self):
		self.iit_Window.destroy()
		self._menucheckII.set(0)

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
		#self.ico_Window.resizable(0,0)

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
			vmin = np.min(self._mat_img.flatten())
			vmax = np.max(self._mat_img.flatten())


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
											from_ = np.min(self._mat_img.flatten()), to = np.max(self._mat_img.flatten()))
		self.ic_vmaxSlider = tk.Scale(self.ic_controlFrame, orient = 'horizontal',
											from_ = np.min(self._mat_img.flatten()), to = np.max(self._mat_img.flatten()))
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
			vmin = np.min(self._mat_img.flatten())
			vmax = np.max(self._mat_img.flatten())

		self._s_img.set_clim([vmin, vmax])
		self._canvas.draw()

		try: self.ic_Window.destroy()
		except AttributeError: pass

		self._menucheckCC.set(0)

class ImageOverlay():

	def init_var(self):

		self._overcmap = {
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

		self._overlabel = {
									'enable': tk.IntVar(),
									'size' : tk.StringVar(),
									'ecolor': tk.StringVar(),
									}

		self._overfit = {
									'enable': tk.IntVar(),
									'lwidth' : tk.StringVar(),
									'color': tk.StringVar()
									}

		self._overedge['enable'].set(0)
		self._overedge['size'].set('5')
		self._overedge['ecolor'].set('none')
		self._overedge['fcolor'].set('orange')
		self._overskel['enable'].set(0)
		self._overskel['size'].set('5')
		self._overskel['ecolor'].set('none')
		self._overskel['fcolor'].set('cyan')
		self._overlabel['enable'].set(0)
		self._overlabel['size'].set('5')
		self._overlabel['ecolor'].set('none')
		self._overfit['enable'].set(0)
		self._overfit['lwidth'].set(1)
		self._overfit['color'].set('yellow')

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
		#self.ov_Window.geometry('450x300-250+80')
		self.ov_Window.resizable(0,0)
		self.ov_Window.protocol('WM_DELETE_WINDOW',
								lambda: ImageOverlay.close(self))

		self.ov_Window.rowconfigure([0,1,2,3,4,5], weight = 1)
		self.ov_Window.columnconfigure(0, weight = 1)

		self.oveLabelFrame = ttk.LabelFrame(self.ov_Window,
												text = 'Edge Options')
		self.ovsLabelFrame = ttk.LabelFrame(self.ov_Window,
												text = 'Skeleton Options')
		self.ovlLabelFrame = ttk.LabelFrame(self.ov_Window,
												text = 'Label Options')
		self.ovfLabelFrame = ttk.LabelFrame(self.ov_Window,
												text = 'Fit Options')
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
											values = self._overcmap['Basic'])
		self.ove_ecCombobox.set(self._overedge['ecolor'].get())
		self.ove_fcLabel = ttk.Label(self.oveLabelFrame,
											text = 'Face color: ')
		self.ove_fcCombobox = ttk.Combobox(self.oveLabelFrame,
											width = 7,
											values = self._overcmap['Basic'])
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
											values = self._overcmap['Basic'])
		self.ovs_ecCombobox.set(self._overskel['ecolor'].get())
		self.ovs_fcLabel = ttk.Label(self.ovsLabelFrame,
											text = 'Face color: ')
		self.ovs_fcCombobox = ttk.Combobox(self.ovsLabelFrame,
											width = 7,
											values = self._overcmap['Basic'])
		self.ovs_fcCombobox.set(self._overskel['fcolor'].get())

		self.ovl_enButton = ttk.Button(self.ovlLabelFrame,
											text = 'Enable',
											style = 'SunkableButton.TButton',
											command = lambda: ImageOverlay.enable_labels(self))
		self.ovl_szLabel = ttk.Label(self.ovlLabelFrame,
											text = 'Size : ')
		self.ovl_szSpinbox = tk.Spinbox(self.ovlLabelFrame,
											width = 3)
		self.ovl_szSpinbox.delete(0,'end')
		self.ovl_szSpinbox.insert(0, self._overlabel['size'].get())

		self.ovl_ecLabel = ttk.Label(self.ovlLabelFrame,
											text = 'Edge color : ')
		self.ovl_ecCombobox = ttk.Combobox(self.ovlLabelFrame,
											width  = 7,
											values = self._overcmap['Basic'])
		self.ovl_ecCombobox.set(self._overlabel['ecolor'].get())

		self.ovf_enButton = ttk.Button(self.ovfLabelFrame,
											text = 'Enable',
											style = 'SunkableButton.TButton',
											command = lambda: ImageOverlay.enable_fit(self))
		self.ovf_lwLabel = ttk.Label(self.ovfLabelFrame,
											text = 'Line Width : ')
		self.ovf_lwSpinbox = tk.Spinbox(self.ovfLabelFrame,
											width = 3)
		self.ovf_lwSpinbox.delete(0,'end')
		self.ovf_lwSpinbox.insert(0, self._overfit['lwidth'].get())

		self.ovf_lcLabel = ttk.Label(self.ovfLabelFrame,
											text = 'Line Color : ')
		self.ovf_lcCombobox = ttk.Combobox(self.ovfLabelFrame,
											width = 7,
											values = self._overcmap['Basic'])
		self.ovf_lcCombobox.set(self._overfit['color'].get())

		self.ovapplyButton = ttk.Button(self.ovbuttonFrame,
											text = 'Apply',
											command = lambda: ImageOverlay.apply(self))
		self.ovcloseButton = ttk.Button(self.ovbuttonFrame,
											text = 'Close',
											command = lambda: ImageOverlay.close(self))

		self.oveLabelFrame.rowconfigure(0, weight = 1)
		self.ovsLabelFrame.rowconfigure(0, weight = 1)
		self.ovlLabelFrame.rowconfigure(0, weight = 1)
		self.ovfLabelFrame.rowconfigure(0, weight = 1)
		self.ovbuttonFrame.columnconfigure([0,1], weight = 1)


		self.oveLabelFrame.grid(row = 1, column = 0, sticky = 'nsew',
											padx = 2, pady = 2)
		self.ovsLabelFrame.grid(row = 2, column = 0, sticky = 'nsew',
											padx = 2, pady = 2)
		self.ovlLabelFrame.grid(row = 3, column = 0, sticky = 'nsew',
											padx = 2, pady = 2)
		self.ovfLabelFrame.grid(row = 4, column = 0, sticky = 'nsew',
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
		self.ovl_enButton.grid(row = 0, column = 0, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovl_szLabel.grid(row = 0, column = 1, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovl_szSpinbox.grid(row = 0, column = 2, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovl_ecLabel.grid(row = 0, column = 3, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovl_ecCombobox.grid(row = 0, column = 4, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovf_enButton.grid(row = 0, column = 0, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovf_lwLabel.grid(row = 0, column = 1, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovf_lwSpinbox.grid(row = 0, column = 2, sticky = 'nsew',
												padx = 2, pady = 2)
		self.ovf_lcLabel.grid(row = 0, column = 3, sticky = 'nsew',
										padx = 2, pady = 2)
		self.ovf_lcCombobox.grid(row = 0, column = 4, sticky = 'nsew',
										padx = 2, pady = 2)
		self.ovapplyButton.grid(row = 0, column = 0, sticky = 'snew',
												padx = 50, pady = 2)
		self.ovcloseButton.grid(row = 0, column = 1, sticky = 'nsew',
												padx = 50, pady = 2)

	def setstate_init(self):

		try: self._skeleton_image
		except AttributeError: self._overskel['enable'].set(0)

		try: self._mask_edge
		except AttributeError: self._overedge['enable'].set(0)

		try: self._labelled_filaments
		except:  AttributeError: self._overlabel['enable'].set(0)

		try: self._m
		except: AttributeError: self._overfit['enable'].set(0)

		if self._overedge['enable'].get() == 1:
			self.ove_enButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)

		if self._overskel['enable'].get() == 1:
			self.ovs_enButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)

		if self._overlabel['enable'].get() == 1:
			self.ovl_enButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)

		if self._overfit['enable'].get() == 1:
			self.ovf_enButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief  = tk.SUNKEN)

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

	def enable_labels(self):
		if self._overlabel['enable'].get() == 1:
			self.ovl_enButton.state(['!pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.RAISED)
			self._overlabel['enable'].set(0)
		elif self._overlabel['enable'].get() == 0:
			self.ovl_enButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)
			self._overlabel['enable'].set(1)

	def enable_fit(self):
		if self._overfit['enable'].get() == 1:
			self.ovf_enButton.state(['!pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.RAISED)
			self._overfit['enable'].set(0)
		elif self._overfit['enable'].get() == 0:
			self.ovf_enButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)
			self._overfit['enable'].set(1)

	def apply(self):
		self._overedge['size'].set(self.ove_szSpinbox.get())
		self._overedge['ecolor'].set(self.ove_ecCombobox.get())
		self._overedge['fcolor'].set(self.ove_fcCombobox.get())
		self._overskel['size'].set(self.ovs_szSpinbox.get())
		self._overskel['ecolor'].set(self.ovs_ecCombobox.get())
		self._overskel['fcolor'].set(self.ovs_fcCombobox.get())
		self._overlabel['size'].set(self.ovl_szSpinbox.get())
		self._overlabel['ecolor'].set(self.ovl_ecCombobox.get())
		self._overfit['lwidth'].set(self.ovf_lwSpinbox.get())
		self._overfit['color'].set(self.ovf_lcCombobox.get())

		MainDisplay.show_overlay(self)
		try: ROIdisplay.show_roi(self)
		except AttributeError: pass
		ImageOverlay.setstate_cpanel(self)

	def setstate_cpanel(self):

		if self._overedge['enable'].get() == 1:
			self.eshowButton.config(text = 'Hide')
		elif self._overedge['enable'].get() == 0:
			self.eshowButton.config(text = 'Show')

		if self._overskel['enable'].get() == 1:
			self.skskeletonButton.config(text = 'Hide')
		elif self._overskel['enable'].get() == 0:
			self.skskeletonButton.config(text = 'Skeleton')

		if self._overlabel['enable'].get() == 1:
			self.tshowlabelButton.config(text = 'Hide Labels')
		elif self._overlabel['enable'].get() == 0:
			self.tshowlabelButton.config(text = 'Show Labels')

		if self._overfit['enable'].get() == 1:
			self.tshowfitButton.config(text = 'Hide Fit')
		elif self._overfit['enable'].get() == 0:
			self.tshowfitButton.config(text = 'Show Fit')

		self.skfilterButton.config(text = 'Filter')
		self.skmaskButton.config(text = 'Mask')

	def close(self):

		self.ov_Window.destroy()
		self._menucheckOO.set(0)

class ROImanager():

	def init_var(self):

		self._roicircle = 0
		self._roirect = 0
		self._roipoly = 0
		self._deledge = tk.IntVar()
		self._delskel = tk.IntVar()
		self._delchain = tk.IntVar()

		self._deledge.set(1)
		self._delskel.set(1)
		self._delchain.set(1)

	def create_window(self):

		try: self.rt_Window.destroy()
		except AttributeError: pass

		self.rt_Window = tk.Toplevel(self)
		self.rt_Window.title('ROI Manager Tracking')
		#self.rt_Window.geometry('240x350-80+50')
		self.rt_Window.resizable(0,1)
		self.rt_Window.protocol('WM_DELETE_WINDOW',
								lambda: ROImanager.close(self))

		self.rt_Window.columnconfigure(0, weight = 1)
		self.rt_Window.rowconfigure(1, weight = 1)

		self.rt_drawFrame = ttk.Frame(self.rt_Window)
		self.roicircleButton = ttk.Button(self.rt_drawFrame,
										text = 'Circle',
										style = 'SunkableButton.TButton',
										command = lambda: ROImanager.draw_circle(self))
		self.roirectButton = ttk.Button(self.rt_drawFrame,
										text = 'Rectangle',
										style = 'SunkableButton.TButton',
										command = lambda: ROImanager.draw_rectangle(self))
		self.roipolyButton = ttk.Button(self.rt_drawFrame,
										text = 'Polygon')

		self.rt_middleFrame = ttk.Frame(self.rt_Window)
		self.rt_middleFrame.rowconfigure(0, weight = 1)
		self.rt_middleFrame.columnconfigure([0,1], weight = 1)
		self.roilistFrame = ttk.LabelFrame(self.rt_middleFrame,
									text = 'ROIs')
		self.roilistFrame.rowconfigure(0, weight = 1)

		self.roiListbox = tk.Listbox(self.roilistFrame,
									width = 15, selectmode = 'extended')
		self.roiListbox.bind('<<ListboxSelect>>',
										lambda event, arg = self:
													ROIdisplay.draw_selec(self, event))
		self.roilistScrollbar = ttk.Scrollbar(self.roilistFrame)
		self.roilistScrollbar.config(command = self.roiListbox.yview)
		self.roiListbox.config(yscrollcommand = self.roilistScrollbar.set)

		self.rt_manageFrame = ttk.Frame(self.rt_middleFrame)
		self.roiselectallButton = ttk.Button(self.rt_manageFrame,
											text = 'Select All',
											command = lambda: ROImanager.selectall_roiList(self))
		self.roiclearallButton = ttk.Button(self.rt_manageFrame,
											text = 'Clear All',
											command = lambda: ROImanager.clearall_roiList(self))
		self.roideleteallButton = ttk.Button(self.rt_manageFrame,
											text = 'Delete All',
											command = lambda: ROImanager.keepdelall_roi(self, 0))
		self.roikeepallButton = ttk.Button(self.rt_manageFrame,
											text = 'Keep All',
											command = lambda: ROImanager.keepdelall_roi(self, 1))
		self.roideleteselecButton = ttk.Button(self.rt_manageFrame,
											text = 'Delete Selection',
											command = lambda: ROImanager.keepdelsel_roi(self, 0))
		self.roikeepselecButton = ttk.Button(self.rt_manageFrame,
											text = 'Keep Selection',
											command = lambda: ROImanager.keepdelsel_roi(self,1))

		self.rt_bottomFrame = ttk.Frame(self.rt_Window)
		self.rt_bottomFrame.columnconfigure([0,1], weight = 1)
		self.roioptionsButton = ttk.Button(self.rt_bottomFrame,
										text = 'Options',
										command = lambda: ROImanager.create_options(self))
		self.roicloseButton = ttk.Button(self.rt_bottomFrame,
										text = 'Close',
										command = lambda: ROImanager.close(self))


		self.rt_drawFrame.grid(row = 0, column = 0,
										sticky = 'nsew')
		self.roicircleButton.grid(row = 0, column = 0,
										sticky = 'nsew', padx = 2, pady = 10)
		self.roirectButton.grid(row = 0, column = 1,
										sticky = 'nsew', padx = 2, pady = 10)
		self.roipolyButton.grid(row = 0, column = 2,
										sticky = 'nsew', padx = 2, pady = 10)

		self.rt_middleFrame.grid(row = 1, column = 0, sticky = 'nsew')

		self.roilistFrame.grid(row = 0, column = 0,
									sticky = 'ns')
		self.roiListbox.grid(row = 0, column = 0, sticky = 'ns')
		self.roilistScrollbar.grid(row = 0, column = 1, sticky = 'ns')

		self.rt_manageFrame.grid(row = 0, column = 1,
										sticky = 'nsew')
		self.roiselectallButton.grid(row = 0, column = 0, sticky = 'nsew',
										pady = 2, padx = 2)
		self.roiclearallButton.grid(row = 1, column = 0, sticky = 'nsew',
										pady = 2, padx = 2)
		self.roideleteallButton.grid(row = 2, column = 0, sticky = 'nsew',
										pady = 2, padx = 2)
		self.roikeepallButton.grid(row = 3, column = 0, sticky = 'nsew',
										pady = 2, padx = 2)
		self.roideleteselecButton.grid(row = 4, column = 0, sticky = 'nsew',
										pady = 2, padx = 2)
		self.roikeepselecButton.grid(row = 5, column = 0, sticky = 'nsew',
										pady = 2, padx = 2)

		self.rt_bottomFrame.grid(row = 2, column = 0,
										sticky = 'nsew')
		self.roioptionsButton.grid(row = 0, column = 0,
										sticky = 'nsew', padx = 10, pady = 10)
		self.roicloseButton.grid(row = 0, column = 1,
										sticky = 'nsew', padx = 10, pady = 10)

		try:
			self._roipath[-1]
			ROImanager.setstate_roi(self)
			ROIdisplay.show_roi(self)
			ROImanager.update_roiList(self)
		except AttributeError:
			ROImanager.setstate_noroi(self)

	def update_roiList(self):

		self.roiListbox.delete(0,'end')

		for n, item in enumerate(self._roipath):
			if hasattr(item, 'get_radius'): text = 'Circle '
			elif hasattr(item, 'get_width'): text = 'Rectangle '
			self.roiListbox.insert('end', text + str(n+1))

	def selectall_roiList(self):

		self.roiListbox.selection_clear(0, 'end')
		self.roiListbox.selection_set(0, 'end')

		ROIdisplay.draw_selec(self, '<Button-1>')

	def clearall_roiList(self):

		MainDisplay.show_overlay(self)
		ROIdisplay.noshow_roi(self)

		del self._roipath
		del self._roilabel

		self.roiListbox.delete(0, 'end')

		self._canvas.draw()

	def create_options(self):

		try: self.ro_Window.destroy()
		except AttributeError: pass

		self.ro_Window = tk.Toplevel(self)
		self.ro_Window.title('ROI data options')
		#self.ro_Window.geometry('180x150-250+100')
		self.ro_Window.resizable(0,0)

		self.roLabelFrame = ttk.LabelFrame(self.ro_Window,
									text = 'Select variables to consider')
		self.roideledgeCheckbutton = ttk.Checkbutton(self.roLabelFrame,
									text = 'Edges',
									variable = self._deledge)
		self.roidelskelCheckbutton = ttk.Checkbutton(self.roLabelFrame,
									text = 'Skeleton',
									variable = self._delskel)
		self.roidelchainCheckbutton = ttk.Checkbutton(self.roLabelFrame,
									text = 'Labelled Chains',
									variable = self._delchain)
		self.roidelcloseButton = ttk.Button(self.roLabelFrame,
									text = 'Close',
									command  = lambda: self.ro_Window.destroy())

		self.ro_Window.rowconfigure(0, weight = 1)
		self.ro_Window.columnconfigure(0, weight = 1)
		self.roLabelFrame.columnconfigure(0, weight = 1)
		self.roLabelFrame.rowconfigure([0,1,2], weight = 1)

		self.roLabelFrame.grid(row = 0, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.roideledgeCheckbutton.grid(row = 0, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.roidelskelCheckbutton.grid(row = 1, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.roidelchainCheckbutton.grid(row = 2, column = 0,
									sticky = 'nsew', padx = 2, pady = 2)
		self.roidelcloseButton.grid(row = 3, column = 0,
									sticky = 'nsew', padx = 5, pady = 2)

	def keepdelall_roi(self, keep):

		self.roiListbox.selection_clear(0, 'end')
		self.roiListbox.selection_set(0, 'end')

		if keep == 0: ROImanager.deldata_inroi(self)
		elif keep == 1: ROImanager.keepdata_inroi(self)

		ROIdisplay.noshow_roi(self)

		del self._roipath; del self._roilabel

		self.roiListbox.delete(0, 'end')

		MainDisplay.show_overlay(self)

	def keepdelsel_roi(self, keep):

		if keep == 0:
			ROImanager.deldata_inroi(self)
			list_del = self.roiListbox.curselection()
		elif keep == 1:
			ROImanager.keepdata_inroi(self)
			list_del = [item for item in np.arange(self.roiListbox.size())
						if item not in self.roiListbox.curselection()]

		ROIdisplay.noshow_roi(self)

		for item in sorted(list_del, reverse=True):
			del self._roipath[item]
			del self._roilabel[item]

		for n, item in enumerate(self._roilabel):
			item.set_text(str(n+1))

		MainDisplay.show_overlay(self)

		ROIdisplay.show_roi(self)
		ROImanager.update_roiList(self)

	def keepdata_inroi(self):

		mask_all = np.zeros(self._mat_img.shape)

		for item in self.roiListbox.curselection():
			mask = ROImanager.data_roi(self, self._roipath[item], 1)
			mask_all = mask_all+mask

		if self._deledge.get() == 1:
			try:
				self._mask_edge = self._mask_edge*mask_all
			except AttributeError: pass
		if self._delskel.get() == 1:
			try:
				self._skeleton_image = self._skeleton_image*mask_all
			except AttributeError: pass
		if self._delchain.get() == 1:
			try:
				self._labelled_filaments = self._labelled_filaments*mask_all
			except AttributeError: pass

	def deldata_inroi(self):

		for item in self.roiListbox.curselection():

			mask = ROImanager.data_roi(self, self._roipath[item], 0)

			if self._deledge.get() == 1:
				try:
					self._mask_edge = self._mask_edge*mask
				except AttributeError: pass
			if self._delskel.get() == 1:
				try:
					self._skeleton_image = self._skeleton_image*mask
				except AttributeError: pass
			if self._delchain.get() == 1:
				try:
					self._labelled_filaments = self._labelled_filaments*mask
				except AttributeError: pass

	def data_roi(self, id_roi, keep):

		if keep == 1: mask = np.zeros(self._mat_img.shape)
		elif keep == 0: mask = np.ones(self._mat_img.shape)

		if hasattr(id_roi, 'get_radius'):
			x,y = id_roi.center
			r = id_roi.get_radius()
			mat_limroi = np.array(list(product(
							range(int(x-r), int(x+r)),
							range(int(y-r), int(y+r))
							)))
			for point in mat_limroi:
				dist = np.sqrt((point[0] - x)**2 + (point[1] - y)**2)
				if dist <= r: mask[point[1], point[0]] = keep
		elif hasattr(id_roi, 'get_width'):
			x,y = id_roi.get_xy()
			width = id_roi.get_width()
			height = id_roi.get_height()
			mat_roi = np.array(list(product(
						range(int(x),int(x+width)),
						range(int(y),int(y+height)))))
			for point in mat_roi:
				mask[point[1], point[0]] = keep
				
		return mask

	def setstate_noroi(self):

		self.roiselectallButton.state(['disabled'])
		self.roiclearallButton.state(['disabled'])
		self.roideleteallButton.state(['disabled'])
		self.roikeepallButton.state(['disabled'])

	def setstate_roi(self):

		self.roiselectallButton.state(['!disabled'])
		self.roiclearallButton.state(['!disabled'])
		self.roideleteallButton.state(['!disabled'])
		self.roikeepallButton.state(['!disabled'])

	def close(self):

		if self._roicircle == 1: ROImanager.draw_circle(self)
		elif self._roirect == 1: ROImanager.draw_rectangle(self)

		try: ROIdisplay.noshow_roi(self)
		except AttributeError: pass

		self.rt_Window.destroy()
		self._menucheckROI.set(0)

	def connect_mpl(self):
		self._cid_press = self._canvas.mpl_connect('button_press_event', lambda event, arg = self: ROIdisplay.on_mousepress(arg, event))
		self._cid_drag = self._canvas.mpl_connect('motion_notify_event', lambda event, arg = self: ROIdisplay.on_mousedrag(arg, event))
		self._cid_up = self._canvas.mpl_connect('button_release_event', lambda event, arg = self: ROIdisplay.on_mouseup(arg, event))

	def disconnect_mpl(self):

		self._canvas.mpl_disconnect(self._cid_press)
		self._canvas.mpl_disconnect(self._cid_drag)
		self._canvas.mpl_disconnect(self._cid_up)

	def draw_circle(self):

		if self._roirect == 1: ROImanager.draw_rectangle(self)

		self._drawmethod = 0
		self._cpressed = 0

		if self._roicircle == 1:
			ROImanager.disconnect_mpl(self)
			self.roicircleButton.state(['!pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.RAISED)
			self._roicircle = 0
		elif self._roicircle == 0:
			ROImanager.connect_mpl(self)
			self.roicircleButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)
			self._roicircle = 1

	def draw_rectangle(self):

		if self._roicircle  == 1 : ROImanager.draw_circle(self)

		self._drawmethod = 1
		self._cpressed = 0

		if self._roirect == 1:
			ROImanager.disconnect_mpl(self)
			self.roirectButton.state(['!pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.RAISED)
			self._roirect = 0
		elif self._roirect == 0:
			ROImanager.connect_mpl(self)
			self.roirectButton.state(['pressed'])
			ttk.Style().configure('SunkableButton.TButton', relief = tk.SUNKEN)
			self._roirect = 1


