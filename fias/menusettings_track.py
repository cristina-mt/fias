import tkinter as tk
from tkinter import filedialog, ttk

import time


class SaveParameters():

	def save_options(self):
		save_options = options = {}

		try: options['initialdir'] = self._saving_info['Output Folder'].get()
		except KeyError: pass

		options['initialfile'] = 'Parameters.txt'
		options['defaultextension'] = '.txt'
		options['filetypes'] = [('Text files', '.txt')]
		options['title'] = 'Save Parameters As: '

		return save_options

	def save_to(self):
		save_options = SaveParameters.save_options(self)
		filename = tk.filedialog.asksaveasfilename(**save_options)
		SaveParameters.save(self, filename)

	def save(self, filename):
		try:
			with open(filename, 'w') as f:
				f.write(time.strftime('Saved on %Y-%m-%d %H:%M')+'\n\n')
				f.write('- # Image options \n')
				try:
					for idic in self._img_info.keys():
						f.write(idic + ': ' + str(self._img_info[idic].get()) +'\n')
				except AttributeError:
					f.write('Image not selected. Information unknown \n')
				f.write('\n # Tracking settings \n')
				for idic in self._tracking_settings.keys():
					f.write(idic + ': ' + str(self._tracking_settings[idic].get()) + '\n')
		except FileNotFoundError: pass

class LoadParameters():

	def load_options(self):
		load_options = options = {}

		try: options['initialdir'] = self._saving_info['Output Folder'].get()
		except KeyError: pass

		options['defaultextension'] = '.txt'
		options['filetypes'] = [('Text files', '.txt')]
		options['title'] = 'Select the file containing the parameters'
		return load_options

	def load(self):

		load_options = LoadParameters.load_options(self)
		filename = tk.filedialog.askopenfilename(**load_options)

		try:
			with open(filename, 'r') as f:
				file_content = f.readlines()
			for line in file_content[1:]:
				ind_sep = line.find(':')
				try:
					key_name = line[0:ind_sep]
					key_value = line[ind_sep+2:]
					try:
						key_str = isinstance(
									   self._tracking_settings[key_name].get(),str)
						if key_str == False:
							self._tracking_settings[key_name].set(int(key_value))
						else:
							self._tracking_settings[key_name].set(key_value)
					except KeyError: pass
				except IndexError: pass
		except FileNotFoundError: pass

class AdvancedSettings():

	def init_var(self):

		self._tracking_settings = {
										'edge_thlow' : tk.StringVar(),
										'edge_thhigh': tk.StringVar(),
										'edge_thup': tk.StringVar(),
										'edge_thup_current': tk.StringVar(),
										'edge_thup_use': tk.IntVar(),
										'edge_thlow_current': tk.StringVar(),
										'edge_thhigh_current': tk.StringVar(),
										'edge_ascale': tk.StringVar(),
										'edge_ascale_current': tk.StringVar(),
										'filter_ascale': tk.StringVar(),
										'filter_ascale_current': tk.StringVar(),
										'mask_th': tk.IntVar(),
										'tracking_lmin': tk.StringVar(),
										'tracking_lunits': tk.IntVar(),
										'tracking_npixfit': tk.StringVar(),
										'pixels_edge_img': tk.StringVar(),
										'pixels_background_profile': tk.StringVar()
											  }

		AdvancedSettings.set_initvar(self)

	def set_initvar(self):

		self._tracking_settings['edge_thlow'].set('0.05');
		self._tracking_settings['edge_thlow_current'].set('0.05')
		self._tracking_settings['edge_thhigh'].set('0.20');
		self._tracking_settings['edge_thhigh_current'].set('0.20')
		self._tracking_settings['edge_thup'].set('0.50')
		self._tracking_settings['edge_thup_current'].set('0.501')
		self._tracking_settings['edge_thup_use'].set(0)
		self._tracking_settings['edge_ascale'].set('6')
		self._tracking_settings['edge_ascale_current'].set('6')
		self._tracking_settings['filter_ascale'].set('6')
		self._tracking_settings['filter_ascale_current'].set('6')
		self._tracking_settings['mask_th'].set(0)
		self._tracking_settings['tracking_lmin'].set('20');
		self._tracking_settings['tracking_lunits'].set(2)
		self._tracking_settings['tracking_npixfit'].set('10')
		self._tracking_settings['pixels_edge_img'].set('10');
		self._tracking_settings['pixels_background_profile'].set('10')

	def create_window(self):

		try: self.st_Window.destroy()
		except AttributeError: pass

		self.st_Window = tk.Toplevel(self)
		self.st_Window.title('Custom Settings')
		self.st_Window.resizable(0,0)


		self.st_scaleLabelFrame = ttk.LabelFrame(self.st_Window,
										   text = 'Filter scale')
		self.st_scaleedgeLabel = ttk.Label(self.st_scaleLabelFrame,
										 text = 'Edge detection: ')
		self.st_scaleedgeEntry  =  ttk.Entry(self.st_scaleLabelFrame,
										   width = 10,
										   textvariable =
												self._tracking_settings['edge_ascale'])
		self.st_scaleskLabel = ttk.Label(self.st_scaleLabelFrame,
										  text = 'Skeleton detection: ')
		self.st_scaleskEntry = ttk.Entry(self.st_scaleLabelFrame,
									 width = 10,
									 textvariable =
										self._tracking_settings['filter_ascale'])

		self.st_trackLabelFrame = ttk.LabelFrame(self.st_Window,
										   text = 'Filament tracking')
		self.st_lminLabel = ttk.Label(self.st_trackLabelFrame,
								 text = 'Min. Length: ')
		self.st_lminEntry = ttk.Entry(self.st_trackLabelFrame,
								 width = 10,
								 textvariable =
									self._tracking_settings['tracking_lmin'])
		self.st_lunitsnmCheckbox = ttk.Radiobutton(self.st_trackLabelFrame,
											 text = 'nm',
											 variable =
												self._tracking_settings['tracking_lunits'],
											 value = 1)
		self.st_lunitspixCheckbox = ttk.Radiobutton(self.st_trackLabelFrame,
											 text = 'pixels',
											 variable =
												self._tracking_settings['tracking_lunits'],
											 value = 2)
		self.st_fitnpixLabel = ttk.Label(self.st_trackLabelFrame,
									text = 'Fit on (n) pixels: ')
		self.st_fitnpixEntry = ttk.Entry(self.st_trackLabelFrame,
									width = 10,
									textvariable =
										self._tracking_settings['tracking_npixfit'])

		self.st_profilesLabelFrame = ttk.LabelFrame(self.st_Window,
											   text = 'Profile extraction')
		self.st_backdiscardLabel = ttk.Label(self.st_profilesLabelFrame,
											text = 'Discard (n) pixels from: ')
		self.st_backimgnpixLabel = ttk.Label(self.st_profilesLabelFrame,
											 text = 'Image border: ')
		self.st_backimgnpixEntry = ttk.Entry(self.st_profilesLabelFrame,
											 width = 10,
											 textvariable =
												self._tracking_settings['pixels_edge_img'])
		self.st_backprofilenpixLabel = ttk.Label(self.st_profilesLabelFrame,
												 text = 'Profile background:')
		self.st_backprofilenpixEntry = ttk.Entry(self.st_profilesLabelFrame,
												 width = 10,
												 textvariable =
													self._tracking_settings['pixels_background_profile'])

		self.st_closeButton = ttk.Button(self.st_Window,
									text = 'Close',
									width = 20,
									command = lambda:
													self.st_Window.destroy())


		self.st_scaleLabelFrame.grid(row = 0, column = 0, sticky = 'nsew',
										   pady = 5, padx = 10)
		self.st_scaleedgeLabel.grid(row = 0, column = 0, sticky = 'nsew',
										 pady = 5, padx = 5)
		self.st_scaleedgeEntry.grid(row = 0, column = 1, sticky = 'nsew',
										 pady = 5, padx = 5)
		self.st_scaleskLabel.grid(row = 1, column = 0, sticky = 'nsew',
									 pady = 5, padx = 5)
		self.st_scaleskEntry.grid(row = 1, column = 1, sticky = 'nsew',
									 pady = 5, padx = 5)

		self.st_trackLabelFrame.grid(row = 1, column = 0, sticky = 'nsew',
										   pady = 5, padx = 10)
		self.st_lminLabel.grid(row = 0, column = 0, sticky = 'nsew',
								 pady = 5, padx = 5)
		self.st_lminEntry.grid(row = 0, column = 1, sticky = 'nsew',
								 pady = 5, padx = 20)
		self.st_lunitsnmCheckbox.grid(row = 1, column = 0, sticky = 'nsew',
											 pady = 5, padx = 10)
		self.st_lunitspixCheckbox.grid(row = 1, column = 1, sticky = 'nsew',
											 pady = 5, padx = 10)
		self.st_fitnpixLabel.grid(row = 2, column = 0, sticky = 'nsew',
									pady = 5, padx = 5)
		self.st_fitnpixEntry.grid(row = 2, column = 1,sticky = 'nsew',
									pady = 5, padx = 20)

		self.st_profilesLabelFrame.grid(row = 2, column = 0, sticky = 'nsew',
										   pady = 5, padx = 10)
		self.st_backdiscardLabel.grid(row = 0, column = 0, sticky = 'nsew',
										   pady = 5, padx = 5,
										   columnspan = 2)
		self.st_backimgnpixLabel.grid(row = 1, column = 0, sticky = 'nsew',
											pady = 5, padx = 5)
		self.st_backimgnpixEntry.grid(row = 1, column = 1, sticky = 'nsew',
											pady = 5, padx = 5)
		self.st_backprofilenpixLabel.grid(row = 2, column = 0, sticky = 'nsew',
												pady = 5, padx = 5)
		self.st_backprofilenpixEntry.grid(row = 2, column = 1, sticky = 'nsew',
												pady = 5, padx = 5)

		self.st_closeButton.grid(row = 3, column = 0,
									pady = 5, padx = 10)

