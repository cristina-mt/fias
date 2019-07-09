import tkinter as tk
from tkinter import ttk, filedialog

import numpy as np
from scipy.interpolate import interp1d
from scipy.optimize import curve_fit

from display_an import MainDisplay, CalDisplay
from menuroi_an import ROIdraw, ROIimage
from popup_an import ErrorMass
from an_functions import FitFunctions

class RefMass():

	def init_var(self):
	
		self._refdata = {'default_options' : {'name': ['TMV', 'FD rods', 'Other'],
															'mpl' : ['131', '18', 'Unknown'],
															'width': ['18', '6.6', 'Unknown']
															},
								'current_options': {'name': 'TMV',
															'mpl' : '131',
															'width': '18'
															},
								'ref_intensity' : [],
								'k_value' : [],
								'data_cal': [],
								'type_cal': [],
								'fit_histo': dict(),
								'fit_plot': dict()
								}

		try:
			self._refdata['ref_intensity'] = self._inputdata['ref_inti'].get()
		except AttributeError: pass
		try: 
			self._refdata['k_value'] = self._inputdata['mass_cal'].get()
		except AttributeError: pass
		
	def set(self):
	
		if self._menucheckMS.get() == 0: 
			
			MainDisplay.show_overlay(self)
			self._roidrawcircle.set(0) 
			try: del self._refpath
			except AttributeError: pass
			
		elif self._menucheckMS.get() == 1:
			
			MainDisplay.show_ref(self)
			self._roidrawcircle.set(1) 
			ROIdraw.circle(self)

	def create_cal(self):
	
		try: self.mc_Window.destroy()
		except AttributeError: pass
		
		self.mc_Window = tk.Toplevel(self)
		self.mc_Window.title('Mass-Intensity Calibration')
		self.mc_Window.resizable(0,0)
		
		self.mc_Window.rowconfigure([0,1,2,3], weight = 1)
		self.mc_Window.columnconfigure(0, weight = 1)
		
		self.mc_inputFrame = ttk.LabelFrame(self.mc_Window,
										text = 'Input Parameters')
		self.mc_inputFrame.columnconfigure([0,1], weight = 1)
		self.mc_refnameLabel = ttk.Label(self.mc_inputFrame,
										text = 'Reference Name: ')
		self.mc_refnameCombobox = ttk.Combobox(self.mc_inputFrame,
										width = 10)
		self.mc_refnameCombobox.config(values = self._refdata['default_options'].get('name'))
		#self.mc_refnameCombobox.state(['!disabled', 'readonly'])
		self.mc_refnameCombobox.set(self._refdata['current_options']['name'])
		self.mc_refnameCombobox.bind('<<ComboboxSelected>>',
												lambda event, arg = self:RefMass.update_caloptions(arg, event))
		self.mc_refmplLabel = ttk.Label(self.mc_inputFrame,
										text = 'MPL (kDa/nm) : ')
		self.mc_refmplEntry = ttk.Entry(self.mc_inputFrame,
										width = 4)
		self.mc_refmplEntry.insert(0,self._refdata['current_options']['mpl'])
		self.mc_refwidthLabel = ttk.Label(self.mc_inputFrame,
										text = 'Width (nm): ')
		self.mc_refwidthEntry = ttk.Entry(self.mc_inputFrame,
										width = 4)
		self.mc_refwidthEntry.insert(0,self._refdata['current_options']['width'])

		self.mc_calbuttonFrame = ttk.Frame(self.mc_Window)
		self.mc_calbuttonFrame.columnconfigure([0,1], weight = 1)
		self.mc_histoButton = ttk.Button(self.mc_calbuttonFrame,
										text = 'Histogram',
										command = lambda: RefMass.histo(self))
		self.mc_plotButton = ttk.Button(self.mc_calbuttonFrame,
										text = 'MPL (width) plot',
										command = lambda: RefMass.plot(self))
										
		self.mc_outputFrame = ttk.LabelFrame(self.mc_Window,
										text = 'Output Parameters')
		self.mc_outputFrame.columnconfigure([0,1], weight = 1)
		self.mc_refintLabel = ttk.Label(self.mc_outputFrame,
										text = 'Int. Intensity (a.u.)')
		self.mc_refintEntry = ttk.Entry(self.mc_outputFrame,
										width = 10)
		self.mc_refintEntry.insert(0, self._refdata['ref_intensity'])
		self.mc_refkLabel = ttk.Label(self.mc_outputFrame,
										text = 'k (units): ')
		self.mc_refkEntry = ttk.Entry(self.mc_outputFrame,
										width = 10)
		self.mc_refkEntry.insert(0, self._refdata['k_value'])
										
		self.mc_buttonFrame = ttk.Frame(self.mc_Window)
		self.mc_buttonFrame.columnconfigure([0,1], weight = 1)
		self.mc_saveButton = ttk.Button(self.mc_buttonFrame,
										text = 'Save',
										command = lambda: RefMass.save_caloptions(self))
		self.mc_closeButton = ttk.Button(self.mc_buttonFrame,
										text = 'Close',
										command = lambda: self.mc_Window.destroy())
										
		self.mc_inputFrame.grid(row = 0, column = 0, 
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_calbuttonFrame.grid(row = 1, column = 0,
											sticky = 'nsew', padx =5 , pady = 5)
		self.mc_outputFrame.grid(row = 2, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_buttonFrame.grid(row = 3, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		
		self.mc_refnameLabel.grid(row = 0, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_refnameCombobox.grid(row = 0, column = 1, 
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_refmplLabel.grid(row = 1, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_refmplEntry.grid(row = 1, column = 1,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_refwidthLabel.grid(row = 2, column = 0, 
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_refwidthEntry.grid(row = 2, column = 1,
											sticky = 'nsew', padx = 5, pady = 5)
		
		self.mc_histoButton.grid(row = 0, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_plotButton.grid(row = 0, column = 1,
											sticky = 'nsew', padx = 5, pady = 5)
											
		self.mc_refintLabel.grid(row = 0, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_refintEntry.grid(row = 0, column = 1,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_refkLabel.grid(row = 1, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_refkEntry.grid(row = 1, column = 1, 
											sticky = 'nsew', padx = 5, pady = 5)
							
		self.mc_saveButton.grid(row = 0, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mc_closeButton.grid(row = 0, column = 1,
											sticky = 'nsew', padx = 5, pady = 5)
											
	def save_caloptions(self):
		
		self._refdata['current_options']['name'] = self.mc_refnameCombobox.get()
		self._refdata['current_options']['mpl'] =  self.mc_refmplEntry.get()
		self._refdata['current_options']['width'] = self.mc_refwidthEntry.get()
		self._refdata['ref_intensity'] = self.mc_refintEntry.get()
		self._refdata['k_value'] = self.mc_refkEntry.get()
		
		try: 
			self._refdata['data_cal'] = self._datacal
			del self._datacal
		except AttributeError: pass
		try: 
			self._refdata['type_cal'] = self._typecal
			del self._typecal
		except AttributeError: pass
		try: 
			self._refdata['fit_histo'] = self._fithisto
			del self._fithisto
		except AttributeError: pass
		try: 
			self._refdata['fit_plot'] = self._fitplot
		except AttributeError: pass

		try: RunMass.update_caloptions(self)
		except AttributeError: pass
			
	def update_caloptions(self, event):

		if self.mc_refnameCombobox.get() == 'TMV' : ind_options = 0
		elif self.mc_refnameCombobox.get() == 'FD rods' : ind_options = 1
		elif self.mc_refnameCombobox.get() == 'Other' : ind_options = 2
		
		self.mc_refmplEntry.delete(0, 'end')
		self.mc_refmplEntry.insert(0, self._refdata['default_options']['mpl'][ind_options])
		self.mc_refwidthEntry.delete(0, 'end')
		self.mc_refwidthEntry.insert(0, self._refdata['default_options']['width'][ind_options])
	
	def get_data(self, data_cal):
	
		self._dataref = dict()
		
		ind_ref = np.where(self._inputdata['fiber_number']<0)[0]
		ind_ref[0]
		
		try:
			self._inputdata['fiber_inti_corr'][ind_ref]
		except KeyError: ComputeMPL.fiber_inticorr(self)
		self._dataref['inti_corr'] = 1*self._inputdata['fiber_inti_corr'][ind_ref]
		
		if data_cal == 'plot': 
			try: self._inputdata['fiber_width'][ind_ref]
			except KeyError: ComputeMPL.fiber_width(self)
			self._dataref['width'] = 1*self._inputdata['fiber_width'][ind_ref]
			
	def histo(self):
	
		try: 
			RefMass.get_data(self, 'histo')
			RefHisto.create(self)
			hist, bin_center = RefHisto.compute(self)
			
			wbin = 0.5*(bin_center[1]-bin_center[0])
			range = [bin_center[0]-wbin, bin_center[-1]+ wbin]
			bins = [len(hist), bin_center[1]-bin_center[0]]
			
			CalDisplay.init_canvas(self)
			CalDisplay.show_histo(self, hist, bin_center)
			
			RefHisto.update_input(self, range, bins)
			
		except IndexError: ErrorMass.needcal(self)
	
	def plot(self):
	
		try:
			RefMass.get_data(self, 'plot')
			RefPlot.create(self)
		except IndexError: ErrorMass.needcal(self)	
		
class RunMass():

	def create(self):
		
		try: self.rm_Window.destroy()
		except AttributeError: pass
		
		RunMass.init_var(self)
		
		self.rm_Window = tk.Toplevel(self)
		self.rm_Window.title('Mass Determination')
		self.rm_Window.resizable(0,0)
		
		self.rm_Window.columnconfigure([0,1], weight = 1)
		self.rm_Window.rowconfigure(0, weight = 1)
		
		
		self.rm_calFrame = ttk.LabelFrame(self.rm_Window,
									text = 'Calibration constants')
		self.rm_kLabel = ttk.Label(self.rm_calFrame,
									text = 'k: ')
		self.rm_kEntry = ttk.Entry(self.rm_calFrame,
									width = 15)
		self.rm_kuLabel = ttk.Label(self.rm_calFrame,
									text = 'kDa/nm * pix')
		self.rm_cLabel = ttk.Label(self.rm_calFrame,
									text = 'c: ')
		self.rm_cEntry = ttk.Entry(self.rm_calFrame,
									width = 15)
		self.rm_cuLabel = ttk.Label(self.rm_calFrame,
									text = 'nm/pix')
			
		self.rm_sideFrame = ttk.Frame(self.rm_Window)
		self.rm_sideFrame.columnconfigure(0, weight = 1)
		
		self.rm_settingsButton = ttk.Button(self.rm_sideFrame,
									text = 'Advanced Settings')
		self.rm_expFrame = ttk.Frame(self.rm_sideFrame)
		self.rm_expFrame.columnconfigure(0, weight = 1)
		self.rm_autoexpCheckbutton = ttk.Checkbutton(self.rm_expFrame,
													text = 'Automatic Export',
													variable = self._rm_autoexp)
		self.rm_exfileButton = ttk.Button(self.rm_expFrame,
										text = 'File name',
										command = lambda: ExportMPL.save_filename(self))
		self.rm_clearFrame = ttk.Frame(self.rm_sideFrame)
		self.rm_clearFrame.columnconfigure([0,1], weight = 1)
		self.rm_clearLabel = ttk.Label(self.rm_clearFrame,
										text = 'Keep profiles after run?')
		self.rm_yesCheckbutton = ttk.Radiobutton(self.rm_clearFrame,
										text = 'Yes',
										variable = self._rm_keep,
										value = 1)
		self.rm_noCheckbutton = ttk.Radiobutton(self.rm_clearFrame,
										text= 'No',
										variable = self._rm_keep,
										value = 0)
		self.rm_buttonFrame = ttk.Frame(self.rm_sideFrame)
		self.rm_runButton = ttk.Button(self.rm_buttonFrame,
										text = 'Run',
										command = lambda: RunMass.run(self))
		self.rm_cancelButton = ttk.Button(self.rm_buttonFrame,
										text = 'Cancel',
										command =lambda: self.rm_Window.destroy())
									

		self.rm_intFrame = ttk.LabelFrame(self.rm_Window,
									text = 'Intensity')
		self.rm_intminCheckbutton = ttk.Checkbutton(self.rm_intFrame,
									text = 'Minima',
									variable = self._rm_imin)
		self.rm_intmeanCheckbutton = ttk.Checkbutton(self.rm_intFrame,
									text = 'Mean',
									variable = self._rm_imean)
		self.rm_intmaxCheckbutton = ttk.Checkbutton(self.rm_intFrame,
									text = 'Max',
									variable = self._rm_imax)
		
		self.rm_massFrame = ttk.LabelFrame(self.rm_Window,
									text = 'Mass')
		self.rm_mplCheckbutton = ttk.Checkbutton(self.rm_massFrame,
									text = 'Mass per Length',
									variable = self._rm_mpl)
		self.rm_massnocorCheckbutton = ttk.Checkbutton(self.rm_massFrame,
									text = 'Raw values',
									variable = self._rm_mraw)
		self.rm_massbackCheckbutton = ttk.Checkbutton(self.rm_massFrame,
									text = 'Background',
									variable = self._rm_mback)
		
		
		self.rm_calFrame.grid(column = 0, row = 0, columnspan = 2,
										sticky = 'nsew', padx = 5, pady = 5)
		self.rm_kLabel.grid(column = 0, row = 0, 
										sticky = 'nsew', padx = 5, pady = 5)
		self.rm_kEntry.grid(column = 1, row = 0,
										sticky = 'nsew', padx = 5, pady = 5)
		self.rm_kuLabel.grid(column = 2, row = 0,
										sticky = 'nsew', padx =5 , pady = 5)
		self.rm_cLabel.grid(column = 0, row = 1,
										sticky = 'nsew', padx = 5, pady = 5)
		self.rm_cEntry.grid(column = 1, row = 1,
										sticky = 'nsew', padx = 5, pady = 5)
		self.rm_cuLabel.grid(column = 2, row = 1,
										sticky = 'nsew', padx = 5, pady = 5)
		self.rm_sideFrame.grid(column = 2, row = 0, rowspan = 2,
										sticky = 'nsew', padx = 5, pady = 5)
		self.rm_settingsButton.grid(column = 0, row = 0, 
										sticky = 'nsew', padx = 10, pady = 5)
		self.rm_expFrame.grid(row = 1, column = 0,
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_autoexpCheckbutton.grid(row = 0, column = 0,
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_exfileButton.grid(row = 1, column = 0, 
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_clearFrame.grid(row = 2, column = 0,
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_clearLabel.grid(row = 0, column = 0, columnspan = 2,
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_yesCheckbutton.grid(row = 1, column = 0, 
										sticky = 'nsew', padx =5, pady = 2)
		self.rm_noCheckbutton.grid(row = 1, column = 1,
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_buttonFrame.grid(row = 3, column = 0,
										sticky = 'nsew', padx = 5, pady = 5)		
		self.rm_runButton.grid(row = 0, column = 0, sticky = 'nsew', 
										padx = 2, pady = 2)
		self.rm_cancelButton.grid(row = 0, column = 1, sticky = 'nsew', 
										padx = 2, pady = 2)
										
		self.rm_intFrame.grid(column = 0, row = 1, 
										sticky = 'nsew', padx = 5, pady = 5)
		self.rm_intminCheckbutton.grid(row = 0, column = 0,
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_intmeanCheckbutton.grid(row = 1, column = 0,
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_intmaxCheckbutton.grid(row = 2, column = 0,
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_massFrame.grid(column = 1, row = 1, 
										sticky = 'nsew', padx = 2, pady = 5)
		self.rm_mplCheckbutton.grid(row = 0, column = 0, 
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_massnocorCheckbutton.grid(row = 1, column = 0,
										sticky = 'nsew', padx = 5, pady = 2)
		self.rm_massbackCheckbutton.grid(row = 2, column = 0,
										sticky = 'nsew', padx = 5, pady = 2)

		RunMass.update_caloptions(self)
		
	def init_var(self):
		self._rm_autoexp = tk.IntVar()
		self._rm_autofile = str(self._inputdata['filename']).replace('.','_mpl.')
		self._rm_keep = tk.IntVar()
		self._rm_imin = tk.IntVar()
		self._rm_imean = tk.IntVar()
		self._rm_imax = tk.IntVar()
		self._rm_mpl = tk.IntVar()
		self._rm_mraw = tk.IntVar()
		self._rm_mback = tk.IntVar()

		self._rm_autoexp.set(1)
		self._rm_keep.set(0)
		self._rm_imin.set(1)
		self._rm_imean.set(1)
		self._rm_imax.set(1)
		self._rm_mpl.set(1)
		self._rm_mraw.set(1)
		self._rm_mback.set(1)
		
	def update_caloptions(self):
		
		try:
			self.rm_kEntry.delete(0, 'end')	
			self.rm_kEntry.insert(0, str(self._refdata['k_value']))
		except KeyError: pass

		try: 
			self.rm_cEntry.delete(0, 'end')
			self.rm_cEntry.insert(0, str(self._inputdata['cal_factor']))
		except KeyError: pass

	def run(self):

		variables_tosave = [0,0,0,
										0,0,0,
										1,1,1,1,
										1,1,1,1,1,1]

		if self._rm_imin.get() == 1:
			try: self._inputdata['int_min'][0]
			except KeyError: ComputeMPL.fiber_inticorr(self)
			variables_tosave[0] = 1
		if self._rm_imean.get() == 1:
			try: self._inputdata['int_mean'][0]
			except KeyError: ComputeMPL.fiber_inticorr(self)
			variables_tosave[1] = 1
		if self._rm_imax.get() == 1:
			try: self._inputdata['int_max'][0]
			except KeyError: ComputeMPL.fiber_inticorr(self)
			variables_tosave[2] = 1
		if self._rm_mpl.get() == 1:
			try: self._inputdata['fiber_mpl'][0]
			except KeyError: ComputeMPL.fiber_mpl(self)
			variables_tosave[3] = 1
		if self._rm_mraw.get() == 1:
			try: self._inputdata['fiber_mpl_raw'][0]
			except KeyError: ComputeMPL.fiber_mpl(self)
			variables_tosave[4] = 1
		if self._rm_mback.get() == 1:
			try: self._inputdata['fiber_mpl_back'][0]
			except KeyError: ComputeMPL.fiber_mpl(self)
			variables_tosave[5] = 1
		try: self._inputdata['fiber_width'][0]
		except KeyError: ComputeMPL.fiber_width(self)

		if self._rm_autoexp.get() == 1:
			ExportMPL.save_file(self, variables_tosave)
		if self._rm_keep.get() == 0: 
				del self._inputdata['int_profile'], self._inputdata['pos_profile']
		
		self.rm_Window.destroy()

class RefHisto():

	def create(self):
		
		try: self.mch_Window.destroy()
		except AttributeError: pass
		
		self.mch_Window = tk.Toplevel()
		self.mch_Window.columnconfigure([0], weight = 1)
		self.mch_Window.rowconfigure(0, weight = 1)
		
		self.mch_frameDisplay = ttk.Frame(self.mch_Window)
		self.mch_frameDisplay.rowconfigure(1, weight = 1)
		self.mch_frameDisplay.columnconfigure(0, weight = 1)
		
		self.mch_lateralFrame = ttk.Frame(self.mch_Window)
		self.mch_lateralFrame.columnconfigure(0, weight = 1)
		self.mch_lateralFrame.rowconfigure([2], weight = 1)
		
		self.mch_rangeFrame = ttk.LabelFrame(self.mch_lateralFrame,
											text = 'Range')
		self.mch_rangeFrame.columnconfigure([0,1], weight = 1)
		self.mch_rangeminLabel = ttk.Label(self.mch_rangeFrame,
											text = 'Min: ')
		self.mch_rangeminEntry = ttk.Entry(self.mch_rangeFrame,
											width = 10)
		self.mch_rangeminEntry.bind('<Return>', lambda event, arg = self: RefHisto.update_wbins(arg, event))
		self.mch_rangemaxLabel = ttk.Label(self.mch_rangeFrame,
											text = 'Max: ')
		self.mch_rangemaxEntry = ttk.Entry(self.mch_rangeFrame,
											width = 10)
		self.mch_rangemaxEntry.bind('<Return>', lambda event, arg = self: RefHisto.update_wbins(arg, event))
		
		self.mch_binsFrame = ttk.LabelFrame(self.mch_lateralFrame,
											text = 'Bining')
		self.mch_binsFrame.columnconfigure([0,1], weight = 1)
		self.mch_nbinLabel = ttk.Label(self.mch_binsFrame,
											text = 'Nr. Bins: ')
		self.mch_nbinEntry = ttk.Entry(self.mch_binsFrame,
											width = 10)
		self.mch_nbinEntry.bind('<Return>', lambda event, arg = self: RefHisto.update_wbins(arg, event))
		self.mch_wbinLabel = ttk.Label(self.mch_binsFrame,
											text = 'Bin width: ')
		self.mch_wbinEntry = ttk.Entry(self.mch_binsFrame,
											width = 10)
		self.mch_wbinEntry.bind('<Return>', lambda event, arg = self: RefHisto.update_nbins(arg, event))
		
		self.mch_buttonsFrame = ttk.Frame(self.mch_lateralFrame)				
		self.mch_buttonsFrame.columnconfigure(0, weight = 1)
		self.mch_updateButton = ttk.Button(self.mch_buttonsFrame,
											text = 'Update histogram',
											command = lambda: RefHisto.update_histo(self))
		self.mch_fitButton = ttk.Button(self.mch_buttonsFrame,
											text = 'Fit Data',
											command = lambda: RefHisto.fit_data(self))
		self.mch_manualButton = ttk.Button(self.mch_buttonsFrame,
											text = 'Manual Selection')
		self.mch_saveButton = ttk.Button(self.mch_buttonsFrame,
											text = 'Save',
											command = lambda: RefHisto.save(self))
		self.mch_closeButton = ttk.Button(self.mch_buttonsFrame,
											text = 'Close',
											command = lambda:  self.mch_Window.destroy())
			
		self.mch_frameDisplay.grid(row = 0, column = 0, 
											sticky = 'nsew', padx = 5, pady = 5)
		self.mch_lateralFrame.grid(row = 0, column = 1,
												sticky = 'ew', padx = 15, pady = 5)
		self.mch_rangeFrame.grid(row = 0, column = 0,
												sticky = 'ew', padx = 5, pady = 5)
		self.mch_binsFrame.grid(row = 1, column = 0,
											sticky = 'ew', padx = 5, pady = 5)
		self.mch_buttonsFrame.grid(row = 2, column = 0,
											sticky = 'ew', padx = 5, pady = 5)
											
		self.mch_rangeminLabel.grid(row = 0, column = 0, 
											sticky = 'nsew', padx = 5, pady = 5)
		self.mch_rangeminEntry.grid(row = 0, column = 1, 
											sticky = 'nsew', padx = 5, pady = 5)
		self.mch_rangemaxLabel.grid(row = 1, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mch_rangemaxEntry.grid(row = 1, column = 1,
											sticky = 'nsew', padx = 5, pady = 5)
		
		self.mch_nbinLabel.grid(row = 0, column = 0, 
											sticky = 'nsew', padx = 5, pady = 5)
		self.mch_nbinEntry.grid(row = 0, column = 1,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mch_wbinLabel.grid(row = 1, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mch_wbinEntry.grid(row = 1, column = 1,
											sticky = 'nsew', padx = 5, pady = 5)
		
		self.mch_updateButton.grid(row = 0, column = 0,
												sticky = 'nsew', padx = 5, pady = 5)
		self.mch_fitButton.grid(row = 1, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mch_manualButton.grid(row = 2, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mch_saveButton.grid(row = 3, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		self.mch_closeButton.grid(row = 4, column = 0,
											sticky = 'nsew', padx = 5, pady = 5)
		
	def update_input(self, range, bins):

		vmin = range[0]; vmax = range[1]
		nbins = bins[0]; wbins = bins[1]
		
		self.mch_rangeminEntry.delete(0, 'end')
		self.mch_rangeminEntry.insert(0, str(vmin))
		self.mch_rangemaxEntry.delete(0, 'end')
		self.mch_rangemaxEntry.insert(0, str(vmax))
		self.mch_nbinEntry.delete(0, 'end')
		self.mch_nbinEntry.insert(0, str(nbins))
		self.mch_wbinEntry.delete(0, 'end')
		self.mch_wbinEntry.insert(0, str(wbins))
		
	def update_wbins(self, event):
		
		vmin = float(self.mch_rangeminEntry.get())
		vmax = float(self.mch_rangemaxEntry.get())
		
		nbins = int(self.mch_nbinEntry.get())
		
		wbins = (vmax - vmin) / nbins
		
		self.mch_wbinEntry.delete(0, 'end')
		self.mch_wbinEntry.insert(0, str(wbins))

	def update_nbins(self, event):
	
		vmin = float(self.mch_rangeminEntry.get())
		vmax = float(self.mch_rangemaxEntry.get())
		
		wbins = float(self.mch_wbinEntry.get())
		
		nbins = int((vmax - vmin)/wbins)

		self.mch_nbinEntry.delete(0, 'end')
		self.mch_nbinEntry.insert(0, str(nbins))

	def update_histo(self):

		vmin = float(self.mch_rangeminEntry.get())
		vmax = float(self.mch_rangemaxEntry.get())
		nbins = int(self.mch_nbinEntry.get())

		hist, bin_center = RefHisto.compute(self, range = (vmin, vmax), bins = nbins)
		CalDisplay.init_canvas(self)
		CalDisplay.show_histo(self, hist, bin_center)

		return [hist, bin_center]
		
	def fit_data(self):
		
		[y, x] = RefHisto.update_histo(self)
		data = self._dataref['inti_corr']

		popt, pcov = curve_fit(FitFunctions.gauss, x, y, 
										p0 = [np.max(y), np.mean(data), np.std(data)])
		fit = FitFunctions.gauss(x, popt[0], popt[1], popt[2])
		CalDisplay.show_fit(self, x, fit)

		self._refhist_fitparam = [popt,pcov]
		self._ref_intensity = popt[1]

		try: del self._refhist_manparam
		except AttributeError: pass

		try: RefHisto.update_fitinfo(self)
		except AttributeError: RefHisto.create_fitinfo(self)

	def create_fitinfo(self):

		try: self.rhf_Window.destroy()
		except AttributeError: pass

		self.rhf_Window = tk.Toplevel()

		self.rhf_Label = ttk.Label(self.rhf_Window)
		self.rhf_closeButton = ttk.Button(self.rhf_Window,
								text = 'Close',
								command = lambda: self.rhf_Window.destroy())
		self.rhf_Label.grid(row = 0, column = 0, sticky = 'nsew', 
								padx = 5, pady = 5)
		self.rhf_closeButton.grid(row = 1, column = 0, sticky = 'nsew', 
								padx = 5, pady = 5)

		RefHisto.update_fitinfo(self)
		
	def update_fitinfo(self):

		text_fit = 'Fit parameters \n \n ' +\
						'Mean Int. Intensity:  ' + \
						str(np.round(self._refhist_fitparam[0][1],4)) +\
						' +\- ' + str(np.round(np.sqrt(self._refhist_fitparam[1][1][1]),4)) +\
						'\n Std Int. Intensity: ' + \
						str(np.round(self._refhist_fitparam[0][2],4)) +\
						' +\- ' + str(np.round(np.sqrt(self._refhist_fitparam[1][2][2]), 4)) +'\n'
		
		self.rhf_Label.config(text = text_fit)

	def compute(self, range = None, bins = None):
		
		data = self._dataref['inti_corr']
	
		if range == None: range_histo  = (np.min(data), np.max(data))
		else: range_histo = range
		if bins == None: bins_histo = 10
		else: bins_histo = bins

		hist, bin_edges = np.histogram(data, bins = bins_histo, range = range_histo)
		bin_center = 0.5*(bin_edges[:-1]+bin_edges[1:])

		return hist, bin_center

	def save(self):
		
		try: 
			self._refdata['ref_intensity'] = self._ref_intensity
		
			ref_mpl = float(self._refdata['current_options']['mpl'])
			k_value = ref_mpl / self._ref_intensity 
			self._refdata['k_value'] = k_value
			self._refdata['data_cal'] = 'Histogram'
		
			try:
				a = self._refhist_fitparam[0][0]
				x0 = self._refhist_fitparam[0][1]
				sigma = self._refhist_fitparam[0][2]
				error_a = self._refhist_fitparam[1][0][0]
				error_x0 = self._refhist_fitparam[1][1][1]
				error_sigma = self._refhist_fitparam[1][2][2]
			
				self._refdata['fit_histo'] = {'a': a, 'x0': x0, 'sigma' : sigma, 
													'error_a': error_a, 
													'error_x0': error_x0, 
													'error_sigma': error_sigma}
			
				self._refdata['type_cal'] = 'Auto'
			except AttributeError: self._refdata['type_cal'] = 'Manual'
		except AttributeError: pass
	

		self.mc_refintEntry.delete(0,'end')
		self.mc_refintEntry.insert(0, self._refdata['ref_intensity'])
		self.mc_refkEntry.delete(0, 'end')
		self.mc_refkEntry.insert(0, str(self._refdata['k_value']))

class RefPlot():

	def create(self):
	
		print('plot')
		
class ComputeMPL():

	def fiber_inticorr(self):
		
		inti = 0.*self._inputdata['fiber_number']
	
		back_inti = 0*inti
		inti_corr = 0*inti
		min_int = 0*inti
		mean_int = 0*inti
		max_int = 0*inti
		
		pos_profile = self._inputdata['pos_profile']
		int_profile = self._inputdata['int_profile']

		dist = 0.5*np.sqrt((self._inputdata['fiber_x2'] - self._inputdata['fiber_x1'])**2+
							(self._inputdata['fiber_y2'] - self._inputdata['fiber_y1'])**2)
		
		for isi in range(len(pos_profile)):
			selec_posprofile = pos_profile[isi]
			selec_intprofile = int_profile[isi]
			
			try: 
				min_int[isi] = np.min(selec_intprofile)
				mean_int[isi] = np.mean(selec_intprofile)
				max_int[isi] = np.max(selec_intprofile)

				bind_1 = np.where(selec_posprofile < -dist[isi])[0]
				bind_2 = np.where(selec_posprofile > dist[isi])[0]
			
				back_inti1 = np.mean(selec_intprofile[bind_1])
				back_inti2 = np.mean(selec_intprofile[bind_2])
			
				back_inti[isi] = np.mean([back_inti1, back_inti2])
			
				try: 
					interp_profile = interp1d(selec_posprofile, selec_intprofile)
					vmin = np.min(selec_posprofile)+0.1
					vmax = np.max(selec_posprofile) - 0.1
					int_posprofile = np.arange(np.around(vmin,1),
															np.around(vmax,1),
															step = 0.1)
					interp_posprofile = [np.around(x,1) for x in int_posprofile]
					interp_intprofile = interp_profile(interp_posprofile)
			
					inti[isi] = np.sum(interp_intprofile*0.1)
					inti_corr[isi] = np.sum((interp_intprofile - back_inti[isi])*0.1)
				except ValueError:inti[isi] = 0; inti_corr[isi] = 0
			except ValueError: pass
					
		
		inti[np.isnan(inti)] = 0; inti_corr[np.isnan(inti_corr)] = 0
		self._inputdata['fiber_inti'] = 1*inti
		self._inputdata['fiber_inti_corr'] = 1*inti_corr
		self._inputdata['back_inti'] = 1*back_inti

		self._inputdata['int_min'] = min_int
		self._inputdata['int_mean'] = mean_int
		self._inputdata['int_max'] = max_int
					
	def fiber_width(self):	
	
		dist = np.sqrt((self._inputdata['fiber_x2'] - self._inputdata['fiber_x1'])**2+
							(self._inputdata['fiber_y2'] - self._inputdata['fiber_y1'])**2)
						
		
		self._inputdata['fiber_width'] = self._inputdata['cal_factor']*dist

	def fiber_mpl(self):

		k_value = float(self.rm_kEntry.get())
		
		self._inputdata['fiber_mpl'] = k_value*self._inputdata['fiber_inti_corr']
		self._inputdata['fiber_mpl_raw'] = k_value*self._inputdata['fiber_inti']
		self._inputdata['fiber_mpl_back'] = k_value*self._inputdata['back_inti']

class ExportMPL():

	def save_options(self):
		
		save_options = options = {}
		options['defaultextension'] = '.npz'
		options['filetypes'] = [
										('Numpy Files', ('.npz', '.npy')),
										('Text Files', '.txt')]
		options['title'] = 'Save As'
		options['initialfile'] = self._rm_autofile

		return save_options

	def save_filename(self):

		save_options = ExportMPL.save_options(self)
		filename = tk.filedialog.asksaveasfilename(**save_options)
		
		try: 
			filename[1]
			self._rm_autofile = filename
		except IndexError as e: print(e)
		
	def save_file(self, variables_tosave):
	
		filename = self._rm_autofile

		try: 
			filetype = filename[-3:]
			if 'npz' in filetype: ExportMPL.numpy_save(self, filename, variables_tosave)
		except IndexError as e: print(e)

	def numpy_save(self, filename, variables_tosave):

		all_data_names = ['int_min', 'int_mean','int_max', 
								'mpl', 'mpl_raw', 'mpl_back',
								'refdata', 'cal_factor',
								'fiber_number', 'fiber_width',
								'fiber_xc', 'fiber_yc',
								'fiber_x1', 'fiber_x2',
								'fiber_y1', 'fiber_y2']

		all_data = [self._inputdata['int_min'], 
					self._inputdata['int_mean'],
					self._inputdata['int_max'],
					self._inputdata['fiber_mpl'],
					self._inputdata['fiber_mpl_raw'],
					self._inputdata['fiber_mpl_back'],
					self._refdata, self._inputdata['cal_factor'],
					self._inputdata['fiber_number'],self._inputdata['fiber_width'],
					self._inputdata['fiber_xc'], self._inputdata['fiber_yc'],
					self._inputdata['fiber_x1'], self._inputdata['fiber_x2'],
					self._inputdata['fiber_y1'], self._inputdata['fiber_y2']]
		
		var_tosave = [int(x) for x in range(len(variables_tosave)) if variables_tosave[x] == 1]

		data_names = [all_data_names[x] for x in var_tosave]
		data = [all_data[x] for x in var_tosave]

		data_dict = dict()
		for item in range(len(data_names)):
			data_dict[data_names[item]] = data[item]

		np.savez(filename, **data_dict)
		print('MPL results saved in ' + str(filename))
		

		