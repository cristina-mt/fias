import tkinter as tk
from tkinter import filedialog

import numpy as np
from PIL import Image

from display_track import MainDisplay


class FileOpen():

	def init_info(self):
		file_info = {
							'directory': tk.StringVar(),
							'file' : tk.StringVar(),
							'extension' : tk.StringVar(),
							'type' : tk.StringVar()
							}

		return file_info

	def load_options(self):
		load_options = options = {}
		options['defaultextension'] = '.tif'
		options['filetypes'] = [('Tiff Files', ('.tif','.tiff')),
										('Text Files', '.txt'),
										('Numpy Files', ('.npy, .npz'))
										]
		options['title'] = 'Open File'

		return load_options

	def load_file(self):

		load_options = FileOpen.load_options(self)
		filename = tk.filedialog.askopenfilename(**load_options)

		try:
			FileOpen.get_info(self, filename)
			if 'Image' == self._file_info['type'].get(): FileOpen.image_load(self, filename)
			elif 'Text' == self._file_info['type'].get(): FileOpen.text_load(self, filename)
			elif 'Numpy' == self._file_info['type'].get(): FileOpen.numpy_load(self, filename)
		except IndexError: pass

	def get_info(self, filename):

		ind_sep_dir = [i for i, x in enumerate(filename) if x == '/'][-1]

		self._file_info = FileOpen.init_info(self)

		self._file_info['file'].set(filename[ind_sep_dir+1:])
		self._file_info['directory'].set(filename[:ind_sep_dir])
		try :	ind_sep_ext = self._file_info['file'].get().find('.')[-1]
		except TypeError: ind_sep_ext = self._file_info['file'].get().find('.')
		self._file_info['extension'].set(self._file_info['file'].get()[ind_sep_ext+1:])

		if 'tif' in self._file_info['extension'].get(): self._file_info['type'].set('Image')
		elif 'txt' in self._file_info['extension'].get(): self._file_info['type'].set('Text')
		elif 'np' in self._file_info['extension'].get(): self._file_info['type'].set('Numpy')

	def image_load(self, filename):

		self._img_info = FileOpen.initvar_img(self)
		self._img_info['type'].set('STEM')
		source_image = np.array(Image.open(filename))
		self._img_info['sizepix_x'].set(source_image.shape[1])
		self._img_info['sizepix_y'].set(source_image.shape[0])

		self._colormap_options['Source'] = 'gray'
		self._menucheckCO.set(0)

		try: self._source_img = source_image[:,:,0];
		except IndexError: self._source_img = source_image[:,:]

		self._img_info['vmin'].set(np.min(source_image.flatten()))
		self._img_info['vmax'].set(np.max(source_image.flatten()))

		self._mat_img = 1*self._source_img
		MainDisplay.init_canvas(self)
		MainDisplay.show_image(self)
		self._canvas.draw()

	def text_load(self, filename):

		with open(filename, 'r') as f:
			init_header = f.readline()

		if 'Channel' in init_header:
			self._img_info = FileOpen.initvar_img(self)
			self._img_info['type'].set('AFM')
			FileOpen.import_afm(self, filename)
			MainDisplay.init_canvas(self)
			MainDisplay.show_image(self)

	def numpy_load(self, filename):

		print('Numpy')

	def initvar_img(self):
		img_info = {
							'type': tk.StringVar(),
							'sizepix_x' : tk.IntVar(),
							'sizepix_y': tk.IntVar(),
							'sizenm_x': tk.IntVar(),
							'sizenm_y': tk.IntVar(),
							'vmin': tk.StringVar(),
							'vmax': tk.StringVar(),
							'cal_factor': tk.StringVar(),
							'xmin': tk.IntVar(),
							'xmax' : tk.IntVar(),
							'ymin' : tk.IntVar(),
							'ymax' : tk.IntVar()
							}
		return img_info

	def import_afm(self, filename):
		header_size = 4
		img_info = []
		with open(filename, 'r') as f:
			for iheader in range(0, header_size):
				line = f.readline()
				if ('Channel' or 'units') in line:
					img_info.append(line[line.find(':')+2:-1])
				else:
					img_info.append(line[line.find(':')+2:line.find('.')+3])

		self._source_img = np.loadtxt(filename)*1e9
		self._mat_img = 1*self._source_img

		xcal_factor=float(img_info[1])*1e3/self._source_img.shape[1]

		self._img_info['sizepix_x'].set(self._source_img.shape[1])
		self._img_info['sizepix_y'].set(self._source_img.shape[0])
		self._img_info['cal_factor'].set(str(xcal_factor))

		self._colormap_options['Source'] = 'inferno'
		self._menucheckCO.set(4)


class FileClose():

	def delete_info(self):

		try:  del self._img_info
		except AttributeError: pass

	def delete_variables(self):

		try:
			del self._source_img
			del self._mat_img
		except AttributeError: pass


class FileOutput():

	def load_options(self):
		load_options = options = {}
		options['title'] = 'Select Output Directory'

		return load_options


	def selec_folder(self):

		load_options = FileOutput.load_options(self)
		filedir = tk.filedialog.askdirectory(**load_options)

		try:
			filedir[-1]
			self._saving_info['Output Folder'] = filedir
		except IndexError: pass


class FileSave():


	def saveas(self):

		try: filedir = self._saving_info['Output Folder'].get()
		except KeyError: filedir = self._file_info['directory'].get()

		save_options = options = {}
		options['defaultextension'] = '.npz'
		options['filetypes'] = [('Numpy Files', '.npz'),
								('Text files', '.txt')]
		options['title'] = 'Save As...'

		filename = tk.filedialog.asksaveasfilename(**save_options)

		try:
			FileSave.numpy_save(self, filename)
		except IndexError: pass

	def numpy_save(self, filename):


		data_names = ['mat_img','cal_factor',
						'int_profile', 'pos_profile',
						'fiber_number', 'fiber_slope',
						'fiber_e1', 'fiber_e2',
						'fiber_xc', 'fiber_yc',
						'fiber_x1', 'fiber_x2',
						'fiber_y1', 'fiber_y2']

		data = [self._mat_img, self._cal_factor,
				self._int_profile, self._pos_profile,
				self._fiber_number, self._fiber_slope,
				self._fiber_e1, self._fiber_e2,
				self._fiber_xc, self._fiber_yc,
				self._fiber_x1, self._fiber_x2,
				self._fiber_y1, self._fiber_y2]

		data_dict = dict()
		for item in range(len(data_names)):
			data_dict[data_names[item]] = data[item]

		np.savez(filename, **data_dict)

		print('Profiles save in ' +str(filename))
