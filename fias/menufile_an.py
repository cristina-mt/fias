import tkinter as tk
from tkinter import filedialog, ttk

import numpy as np

from display_an import MainDisplay

class FileLoad():

	def load_options(self):

		load_options = options = {}
		options['defaultextension'] = '.npz'
		options['filetypes'] = [
								('Numpy Files',('.npz','.npy')),
								('Text Files', '.txt')
								]
		options['title'] = 'Load File'

		return load_options

	def load_file(self):

		load_options = FileLoad.load_options(self)
		filename = tk.filedialog.askopenfilename(**load_options)

		try:
			filetype = filename[-3:]
			if 'npz' in filetype: FileLoad.numpy_load(self, filename)
		except IndexError: pass
		
	def numpy_load(self, filename):
		
		data = np.load(filename, allow_pickle = True)
		
		FileLoad.load_choice(self, data.files)
		self.wait_window(self.lc_Window)
		
		if self._importdata == 1:
			
			var_values = [self._checkImg, self._checkCalfactor,
							self._checkInt, self._checkPos, 
							self._checkImin, self._checkImean, self._checkImax, self._checkInti,
							self._checkCenter, self._checkCenter, 
							self._checkEdge, self._checkEdge, self._checkEdge, self._checkEdge, 
							self._checkSlope, self._checkNumber,
							self._checkWidth, self._checkMPL, self._checkRefint, self._checkMasscal]
			
			var_names  = ['mat_img','cal_factor',
								'int_profile', 'pos_profile',
								'int_min' ,'int_mean' ,'int_max' ,'fiber_inti_corr' ,
								'fiber_xc' ,'fiber_yc',
								'fiber_x1' ,'fiber_x2', 'fiber_y1', 'fiber_y2', 
								'fiber_slope' ,'fiber_number' ,
								'fiber_width' ,'fiber_mpl' ,'ref_inti' ,'mass_cal']
			
			for ikey in range(len(var_values)):
				if var_values[ikey].get() == 1: self._inputdata[var_names[ikey]] = data[var_names[ikey]]
			
			MainDisplay.show_loaddata(self)
			self._inputdata['filename'] = filename		
		data.close()
				
	def load_choice(self, key_names):
	
		FileLoad.create_loadchoice(self)
		FileLoad.setstate_loadchoice(self, key_names)
		
		self.lc_importButton.focus_set()
		self.lc_Window.bind('<Return>', lambda event: FileLoad.bindreturn_loadchoice(self))
				
	def create_loadchoice(self):
		
		try: self.lc_Window.destroy()
		except AttributeError: pass
		
		self.lc_Window = tk.Toplevel(self)
		self.lc_Window.title('Choose Data to Import')
		self.lc_Window.resizable(0,0)
		
		self.lc_Window.columnconfigure(0, weight = 1)
		self.lc_Window.rowconfigure(0, weight = 1)
		
		self._checkImg = tk.IntVar(value  = 0); self._checkCalfactor = tk.IntVar(value  = 0)
		self._checkInt = tk.IntVar(value  = 0); self._checkPos = tk.IntVar(value  = 0)
		self._checkImin = tk.IntVar(value  = 0); self._checkImean = tk.IntVar(value  = 0)
		self._checkImax = tk.IntVar(value  = 0); self._checkInti = tk.IntVar(value  = 0)
		self._checkCenter = tk.IntVar(value  = 0); self._checkEdge = tk.IntVar(value  = 0)
		self._checkSlope = tk.IntVar(value  = 0); self._checkNumber = tk.IntVar(value  = 0)
		self._checkWidth = tk.IntVar(value  = 0); self._checkMPL = tk.IntVar(value  = 0)
		self._checkInti = tk.IntVar(value  = 0); self._checkMasscal = tk.IntVar(value  = 0)
		self._checkRefint = tk.IntVar(value = 0)
		
		
		self.lc_buttonFrame = ttk.Frame(self.lc_Window)
		self.lc_buttonFrame.columnconfigure([0,1,2,3], weight = 1)
		
		self.lc_selectallButton = ttk.Button(self.lc_buttonFrame,
										text = 'Select All',
										command = lambda: FileLoad.clearselectall_loadchoice(self, 1))
		self.lc_clearallButton = ttk.Button(self.lc_buttonFrame,
										text = 'Clear All',
										command = lambda: FileLoad.clearselectall_loadchoice(self, 0))
		self.lc_importButton = ttk.Button(self.lc_buttonFrame,
										text = 'Import Data',
										command = lambda: FileLoad.import_loadchoice(self, 1))
		self.lc_cancelButton = ttk.Button(self.lc_buttonFrame,
										text = 'Cancel',
										command = lambda: FileLoad.import_loadchoice(self, 0))
				
		self.lc_VarFrame = ttk.Frame(self.lc_Window)
		self.lc_imgFrame = ttk.LabelFrame(self.lc_VarFrame,
									text = 'Image')
		self.lc_profileFrame = ttk.LabelFrame(self.lc_VarFrame,
									text = 'Profiles')
		self.lc_coordFrame = ttk.LabelFrame(self.lc_VarFrame,
									text ='Coordinates')
		self.lc_intFrame = ttk.LabelFrame(self.lc_VarFrame,
									text = 'Intensity')
		self.lc_massFrame = ttk.LabelFrame(self.lc_VarFrame,
									text = 'Mass Mapping')
		
		
		self.lc_imgCheckbutton = ttk.Checkbutton(self.lc_imgFrame,
										text = 'Image',
										variable = self._checkImg)
		self.lc_calfactorCheckbutton = ttk.Checkbutton(self.lc_imgFrame,
										text = 'Calibration Factor',
										variable = self._checkCalfactor)
		self.lc_intCheckbutton = ttk.Checkbutton(self.lc_profileFrame,
										text = 'Intensity',
										variable = self._checkInt)
		self.lc_posCheckbutton = ttk.Checkbutton(self.lc_profileFrame,
										text = 'Position',
										variable = self._checkPos)
		self.lc_centerCheckbutton = ttk.Checkbutton(self.lc_coordFrame,
										text = 'Center',
										variable = self._checkCenter)
		self.lc_edgeCheckbutton = ttk.Checkbutton(self.lc_coordFrame,
										text = 'Edges',
										variable = self._checkEdge)
		self.lc_slopeCheckbutton = ttk.Checkbutton(self.lc_coordFrame,
										text = 'Slope',
										variable = self._checkSlope)
		self.lc_numberCheckbutton = ttk.Checkbutton(self.lc_coordFrame,
										text = 'Fiber number',
										variable = self._checkNumber)
		self.lc_intminCheckbutton = ttk.Checkbutton(self.lc_intFrame,
										text = 'Minima',
										variable = self._checkImin)
		self.lc_intmeanCheckbutton = ttk.Checkbutton(self.lc_intFrame,
										text = 'Mean',
										variable = self._checkImean)
		self.lc_intmaxCheckbutton = ttk.Checkbutton(self.lc_intFrame,
										text = 'Maxima',
										variable = self._checkImax)
		self.lc_intiCheckbutton = ttk.Checkbutton(self.lc_intFrame,
										text = 'Integrated',
										variable = self._checkInti)
		self.lc_widthCheckbutton = ttk.Checkbutton(self.lc_massFrame,
										text = 'Fiber width',
										variable = self._checkWidth)
		self.lc_mplCheckbutton = ttk.Checkbutton(self.lc_massFrame,
										text = 'MPL',
										variable = self._checkMPL)
		self.lc_refintiCheckbutton = ttk.Checkbutton(self.lc_massFrame,
										text = 'Reference Int.',
										variable = self._checkRefint)
		self.lc_masscalCheckbutton = ttk.Checkbutton(self.lc_massFrame,
										text = 'Mass calibration',
										variable = self._checkMasscal)
							
		self.lc_imgCheckbutton.config(state = 'disabled')
		self.lc_calfactorCheckbutton.config(state = 'disabled')
		self.lc_intCheckbutton.config(state = 'disabled')
		self.lc_posCheckbutton.config(state = 'disabled')
		self.lc_centerCheckbutton.config(state = 'disabled')
		self.lc_edgeCheckbutton.config(state = 'disabled')
		self.lc_slopeCheckbutton.config(state = 'disabled')
		self.lc_numberCheckbutton.config(state = 'disabled')
		self.lc_intminCheckbutton.config(state = 'disabled')
		self.lc_intmeanCheckbutton.config(state = 'disabled')
		self.lc_intmaxCheckbutton.config(state = 'disabled')
		self.lc_intiCheckbutton.config(state = 'disabled')
		self.lc_widthCheckbutton.config(state = 'disabled')
		self.lc_mplCheckbutton.config(state = 'disabled')
		self.lc_refintiCheckbutton.config(state = 'disabled')
		self.lc_masscalCheckbutton.config(state = 'disabled')
				
		self.lc_buttonFrame.grid(row = 0, column = 0, sticky = 'nsew',
											padx = 5, pady = 5)
		self.lc_selectallButton.grid(row = 0, column = 0, sticky = 'nsew',
											padx = 5, pady = 5)
		self.lc_clearallButton.grid(row = 0, column = 1, sticky = 'nsew',
											padx = 5, pady = 5)
		self.lc_importButton.grid(row = 0, column = 2, sticky= 'nsew',
											padx = 5, pady = 5)
		self.lc_cancelButton.grid(row = 0, column = 3, sticky = 'nsew',
											padx = 5, pady = 5)
		self.lc_VarFrame.grid(row = 1, column = 0, sticky = 'nsew',
											padx = 5, pady = 5)
		self.lc_imgFrame.grid(row = 0, column = 0, sticky = 'nsew',
											padx = 5, pady = 5)
		self.lc_profileFrame.grid(row = 1, column = 0, sticky = 'nsew',
											padx = 5, pady = 5)
		self.lc_intFrame.grid(row = 0, column = 1, rowspan = 2, sticky = 'nsew',
											padx = 5, pady = 5)
		self.lc_coordFrame.grid(row = 0, column = 2, rowspan = 2, sticky = 'nsew',
											padx = 5, pady = 5)
		self.lc_massFrame.grid(row = 0, column = 3, rowspan = 2, sticky = 'nsew',
											padx = 5, pady = 5)
											
		self.lc_imgCheckbutton.grid(row = 0, column = 0, sticky = 'nsew')
		self.lc_calfactorCheckbutton.grid(row = 1, column = 0, sticky = 'nsew')
		self.lc_intCheckbutton.grid(row = 0, column = 0, sticky = 'nsew')
		self.lc_posCheckbutton.grid(row = 1, column = 0, sticky = 'nsew')
		self.lc_centerCheckbutton.grid(row = 0, column = 0, sticky = 'nsew')
		self.lc_edgeCheckbutton.grid(row = 1, column = 0, sticky = 'nsew')
		self.lc_slopeCheckbutton.grid(row = 2, column = 0, sticky = 'nsew')
		self.lc_numberCheckbutton.grid(row = 3, column = 0, sticky = 'nsew')
		self.lc_intminCheckbutton.grid(row = 0, column = 0, sticky = 'nsew')
		self.lc_intmeanCheckbutton.grid(row = 1, column = 0, sticky = 'nsew')
		self.lc_intmaxCheckbutton.grid(row  = 2, column = 0, sticky = 'nsew')
		self.lc_intiCheckbutton.grid(row = 3, column = 0, sticky = 'nsew')
		self.lc_widthCheckbutton.grid(row = 0, column = 0, sticky = 'nsew')
		self.lc_mplCheckbutton.grid(row = 1, column = 0, sticky = 'nsew')
		self.lc_refintiCheckbutton.grid(row = 2, column = 0, sticky = 'nsew')
		self.lc_masscalCheckbutton.grid(row = 3, column = 0, sticky = 'nsew')
	
	def bindreturn_loadchoice(self):
	
		focused_widget = self.lc_Window.focus_get()
		
		if focused_widget == self.lc_importButton: FileLoad.import_loadchoice(self, 1)
		elif focused_widget == self.lc_cancelButton: FileLoad.import_loadchoice(self, 0)
		elif focused_widget == self.lc_selectallButton: FileLoad.clearselectall_loadchoice(self, 1)
		elif focused_widget == self.lc_clearallButton: FileLoad.clearselectall_loadchoice(self, 0)
		
	def setstate_loadchoice(self, key_names):
		
		var_names  = ['mat_img','cal_factor',
								'int_profile', 'pos_profile',
								'int_min' ,'int_mean' ,'int_max' ,'fiber_inti_corr' ,
								'fiber_xc' ,'fiber_x1' ,'fiber_slope' ,'fiber_number' ,
								'fiber_width' ,'fiber_mpl' ,'ref_inti' ,'mass_cal']
	
		var_checkbutton = [self.lc_imgCheckbutton, self.lc_calfactorCheckbutton,
									self.lc_intCheckbutton, self.lc_posCheckbutton,
									self.lc_intminCheckbutton, self.lc_intmeanCheckbutton, self.lc_intmaxCheckbutton, self.lc_intiCheckbutton,
									self.lc_centerCheckbutton, self.lc_edgeCheckbutton, self.lc_slopeCheckbutton, self.lc_numberCheckbutton,
									self.lc_widthCheckbutton, self.lc_mplCheckbutton, self.lc_refintiCheckbutton, self.lc_masscalCheckbutton]
									
		var_values = [self._checkImg, self._checkCalfactor,
							self._checkInt, self._checkPos, 
							self._checkImin, self._checkImean, self._checkImax, self._checkInti,
							self._checkCenter, self._checkEdge, self._checkSlope, self._checkNumber,
							self._checkWidth, self._checkMPL, self._checkRefint, self._checkMasscal]
							
		for ivar in range(len(var_names)):
			if var_names[ivar] in key_names: 
				var_checkbutton[ivar].config(state = 'normal')
				var_values[ivar].set(1)
		
	def clearselectall_loadchoice(self, value_set):
		var_checkbutton = [self.lc_imgCheckbutton, self.lc_calfactorCheckbutton,
									self.lc_intCheckbutton, self.lc_posCheckbutton,
									self.lc_intminCheckbutton, self.lc_intmeanCheckbutton, self.lc_intmaxCheckbutton, self.lc_intiCheckbutton,
									self.lc_centerCheckbutton, self.lc_edgeCheckbutton, self.lc_slopeCheckbutton, self.lc_numberCheckbutton,
									self.lc_widthCheckbutton, self.lc_mplCheckbutton, self.lc_refintiCheckbutton, self.lc_masscalCheckbutton]
	
		var_values = [self._checkImg, self._checkCalfactor,
							self._checkInt, self._checkPos, 
							self._checkImin, self._checkImean, self._checkImax, self._checkInti,
							self._checkCenter, self._checkEdge, self._checkSlope, self._checkNumber,
							self._checkWidth, self._checkMPL, self._checkRefint, self._checkMasscal]


		for ivar in range(len(var_values)): 
			if 'disabled' not in var_checkbutton[ivar].state():  var_values[ivar].set(value_set)
	
	def import_loadchoice(self, ok_value):
		self.lc_Window.destroy()
		self._importdata = ok_value
		
class FileSave():

	def saveas(self):

		save_options = options = {}
		options['defaultextension'] = '.npz'
		options['filetypes'] = [('Numpy Files', '.npz')]
		options['title'] = 'Save As...'

		filename = tk.filedialog.asksaveasfilename(**save_options)

		try:
			FileSave.numpy_save(self, filename)
		except IndexError: pass

										
	def numpy_save(self, filename):


		data_names = ['mat_img','cal_factor',
						'int_profile', 'pos_profile',
						'fiber_number', 'fiber_slope',
						'fiber_xc', 'fiber_yc',
						'fiber_x1', 'fiber_x2',
						'fiber_y1', 'fiber_y2']

		data = [self._inputdata['mat_img'], self._inputdata['cal_factor'],
				self._inputdata['int_profile'], self._inputdata['pos_profile'],
				self._inputdata['fiber_number'], self._inputdata['fiber_slope'],
				self._inputdata['fiber_xc'], self._inputdata['fiber_yc'],
				self._inputdata['fiber_x1'], self._inputdata['fiber_x2'],
				self._inputdata['fiber_y1'], self._inputdata['fiber_y2']]

		data_dict = dict()
		for item in range(len(data_names)):
			data_dict[data_names[item]] = data[item]

		np.savez(filename, **data_dict)

		print('new Profiles save in ' +str(filename))

class FileClose():

	def delete_variables(self):
		try: del self._inputdata
		except AttributeError: pass


