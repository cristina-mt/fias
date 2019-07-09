import tkinter as tk
from tkinter import ttk

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import Circle, Rectangle, PathPatch
from  matplotlib.lines import Line2D
from matplotlib import path, patches
import matplotlib.pyplot as plt


class MainDisplay():

	def init_canvas(self):
		try: plt.close(self._f_img)
		except AttributeError: pass

		try: self._canvas.delete(ALL)
		except AttributeError: pass

		self._f_img = Figure(facecolor = [0.95,0.95,0.96])
		self._f_img.subplots_adjust(left = 0.0, bottom = 0.0,
												right = 1.0, top = 1.0,
												wspace = 0, hspace = 0)
		self._a_img = self._f_img.add_subplot(111);
		self._a_img.axis('off')
		self._canvas = FigureCanvasTkAgg(
							   self._f_img, master = self.frameMainDisplay)
		self._frame_canvas = self._canvas.get_tk_widget()
		self._frame_canvas.grid(row = 1, column = 0, sticky = 'nsew')

		self._frame_itoolbar = ttk.Frame(self.frameMainDisplay)
		self._frame_itoolbar.grid(row = 0, column = 0, sticky = 'nsew')
		self._t_img = NavigationToolbar2Tk(
						  self._canvas, self._frame_itoolbar)

	def show_trackoutput(self):

		self._overskel['enable'].set(1)
		self._overedge['enable'].set(1)

		MainDisplay.show_overlay(self)
		
	def show_loaddata(self):
	
		
		if 'mat_img' in self._inputdata: self._overimg['enable'].set(1)
		if 'fiber_xc' in self._inputdata: self._overskel['enable'].set(1)
		if 'fiber_x1' in self._inputdata: self._overedge['enable'].set(1)
		
		MainDisplay.show_overlay(self)
		
		if 'fiber_mpl' in self._inputdata:
			canvas, subplot = PlotWindow.plot_scatter(self, self._inputdata['fiber_width'],
												self._inputdata['fiber_mpl'])
			subplot.set_xlabel('width (nm)')
			subplot.set_ylabel('MPL (nm)')
		
	def show_image(self):

		colormap = self._colormap_options.get('Current Main')
		if colormap is None:
			colormap = 'gray'
			self._colormap_options['Current Main'] = 'gray'
		
		if self._overimg['enable'].get() == 1: 
			self._s_img = self._a_img.imshow(self._inputdata['mat_img'], cmap = colormap)
		elif self._overimg['enable'].get() == 0:
			self._s_img = self._a_img.imshow(np.ones([1,1]), cmap = colormap)

	def show_overlay(self):

		MainDisplay.init_canvas(self)
		MainDisplay.show_image(self)
			
		fcolor_skel = self._overskel['fcolor'].get()
		fcolor_edge = self._overedge['fcolor'].get()

		fcolor_edge1 = fcolor_edge; fcolor_edge2 = fcolor_edge1

		if fcolor_skel == 'fiber number': fcolor_skel = self._inputdata['fiber_number']
		if fcolor_edge == 'fiber number':
			fcolor_edge1 = self._inputdata['fiber_number']
			fcolor_edge2 = fcolor_edge1
		elif fcolor_edge == 'edge strength':
			fcolor_edge1 = self._inputdata['fiber_e1']*100
			fcolor_edge2 = self._inputdata['fiber_e2']*100

		if self._overskel['enable'].get() == 1:

			self._a_img.scatter(self._inputdata['fiber_xc'],
								self._inputdata['fiber_yc'],
								s = int(self._overskel['size'].get()),
								c = fcolor_skel,
								edgecolor = self._overskel['ecolor'].get(),
								)
		if self._overedge['enable'].get() == 1:
			self._a_img.scatter(self._inputdata['fiber_x1'],
								self._inputdata['fiber_y1'],
								s = int(self._overedge['size'].get()),
								c = fcolor_edge1,
								edgecolor = self._overedge['ecolor'].get()
								)
			self._a_img.scatter(self._inputdata['fiber_x2'],
								self._inputdata['fiber_y2'],
								s = int(self._overedge['size'].get()),
								c = fcolor_edge2,
								edgecolor = self._overedge['ecolor'].get()
								)

		self._canvas.draw()
		
	def show_ref(self):
	
		MainDisplay.init_canvas(self)
		MainDisplay.show_image(self)
		
		data_filaments = self._inputdata['fiber_number']>=0
		
		self._a_img.scatter(self._inputdata['fiber_x1'][data_filaments],
									self._inputdata['fiber_y1'][data_filaments],
									s = 5, c = 'lightblue', edgecolor = 'none')
		self._a_img.scatter(self._inputdata['fiber_x2'][data_filaments],
									self._inputdata['fiber_y2'][data_filaments],
									s = 5, c = 'lightblue', edgecolor = 'none')
		
		try: 
			data_ref = self._inputdata['fiber_number'] < 0
			self._a_img.scatter(self._inputdata['fiber_x1'][data_ref],
										self._inputdata['fiber_y1'][data_ref],
										s = 5, c = 'red', edgecolor = 'none')
			self._a_img.scatter(self._inputdata['fiber_x2'][data_ref],
										self._inputdata['fiber_y2'][data_ref],
										s = 5, c = 'red', edgecolor = 'none')
		except: pass
		
class PlotWindow():
	
	def plot_scatter(self, xdata, ydata):
	
		f_img = Figure()
		a_img = f_img.add_subplot(111)

		plot_window = tk.Toplevel(self)
		plot_window.title('Figure ' + str(plt.gcf().number)+': Scatter Plot')
		plot_window.columnconfigure(0, weight = 1)
		plot_window.rowconfigure(1, weight = 1)
		
		canvas = FigureCanvasTkAgg(
						f_img, master = plot_window)
		frame_canvas = canvas.get_tk_widget()
		frame_itoolbar = ttk.Frame(plot_window)
		
		frame_canvas.grid(row = 1, column = 0, sticky = 'nsew')
		frame_itoolbar.grid(row = 0, column = 0, sticky = 'nsew')
		t_img = NavigationToolbar2Tk(canvas, frame_itoolbar)
		
		a_img.scatter(xdata, ydata, 
							s = 10, c = 'w', edgecolor = 'k',
							alpha = 0.8)
							
		return canvas, a_img
		
class CMdisplay():

	def show_colormaps(self):

		screen_height = self.ico_frame.winfo_screenheight()

		try: plt.close(self._f_ic)
		except AttributeError: pass

		try: self._ic_canvas.delete(ALL)
		except AttributeError: pass

		self._f_ci = Figure(facecolor = [0.95,0.95,0.96])
		self._f_ci.subplots_adjust(top=0.99, bottom=0.01, left=0.2, right=0.99)

		a = np.linspace(0, 2, 256).reshape(1,-1)
		a = np.vstack((a,a))

		# Get a list of the colormaps in matplotlib.  Ignore the ones that end with
		# '_r' because these are simply reversed versions of ones that don't end
		# with '_r'
		maps_0 = sorted(m for m in plt.cm.datad if not m.endswith("_r"))

		if screen_height <= 1000 : maps = [maps_0[n] for n in np.arange(0,len(maps_0),step = 2)]
		else: maps = maps_0
		nmaps = len(maps) + 1

		self._colormap_options['Available'] = maps

		for i,m in enumerate(maps):
			ax = self._f_ci.add_subplot(nmaps, 1, i+1)
			ax.axis("off")
			ax.imshow(a, aspect='auto', cmap=plt.get_cmap(m), origin='lower')
			pos = list(ax.get_position().bounds)
			self._f_ci.text(pos[0] - 0.01, pos[1], m, fontsize=10, horizontalalignment='right')
		self._ic_canvas = FigureCanvasTkAgg(
							   self._f_ci, master = self.ico_frame)
		self._ic_frame_canvas = self._ic_canvas.get_tk_widget()
		self._ic_frame_canvas.grid(row = 0, column = 0, sticky = 'nsew')
		self._ic_canvas.draw()

class Cdisplay():

	def init_canvas(self):

		try: plt.close(self._f_ih)
		except AttributeError: pass

		try: self._hi_canvas.delete(ALL)
		except AttributeError: pass

		self._f_hi = Figure(facecolor = [0.95, 0.95, 0.96])
		self._a_hi = self._f_hi.add_subplot(111)
		self._hi_canvas = FigureCanvasTkAgg(
									self._f_hi, master = self.ic_frame)
		self._hi_frame_canvas = self._hi_canvas.get_tk_widget()
		self._hi_frame_canvas.config(height = 125, width = 200)
		self._hi_frame_canvas.grid(row = 0, column = 0, sticky = 'nsew')

	def show_histogram(self):

		Cdisplay.init_canvas(self)

		self._a_hi.hist(self._inputdata['mat_img'].flatten(), 100, fc = 'k', ec = 'w')
		for item in (self._a_hi.get_xticklabels() + self._a_hi.get_yticklabels()): item.set_fontsize(7)

	def update_clim(self):

		try: self._hi_vmin_line.pop(0).remove()
		except AttributeError: pass

		try: self._hi_vmax_line.pop(0).remove()
		except AttributeError: pass

		vmin = self.ic_vminSlider.get()
		vmax = self.ic_vmaxSlider.get()

		ylim = self._a_hi.get_ylim()

		self._hi_vmin_line = self._a_hi.plot([vmin, vmin],ylim, c= [0, 0.2, 0.4], lw = 2)
		self._hi_vmax_line = self._a_hi.plot([vmax, vmax],ylim, c = [0, 0.2, 0.4], lw = 2)

		self._s_img.set_clim([vmin, vmax])

		self._hi_canvas.draw()
		self._canvas.draw()

class ROIdisplay():

	def on_mousepress(self, event):
		self._cpressed = 1

		self._roix1 = event.xdata
		self._roiy1 = event.ydata

		if self._roidrawline.get() == 1:
			self._citem = Line2D([self._roix1, self._roix1+1],
									[self._roiy1, self._roiy1+1],
									c = 'yellow')
		elif self._roidrawcircle.get() == 1:
			self._citem = Circle((self._roix1, self._roiy1), 1,
								fc = 'none', ec = 'yellow')
		elif self._roidrawrect.get() == 1:
			self._citem = Rectangle((self._roix1, self._roiy1), 1, 1,
									fc = 'none', ec = 'yellow')

		if self._menucheckRI.get() == 0:
			self._a_img.add_artist(self._citem)
			self._canvas.draw()

	def on_mousedrag(self, event):

		if self._cpressed == 1:
			self._citem.remove()
			self._canvas.draw()
			self._roix2 = event.xdata
			self._roiy2 = event.ydata

			if self._roidrawline.get() == 1:
				self._citem = Line2D([self._roix1, self._roix2],[self._roiy1, self._roiy2],
								c = 'yellow')
			elif self._roidrawcircle.get() == 1:
				x1 = np.mean([self._roix1, self._roix2])
				y1 = np.mean([self._roiy1, self._roiy2])
				r = np.sqrt((self._roix2 - x1)**2+(self._roiy2 - y1)**2)
				self._citem = Circle((x1,y1), r, fc = 'none', ec = 'yellow')
			elif self._roidrawrect.get() == 1:
				width = np.abs(self._roix2 - self._roix1)
				height = np.abs(self._roiy2 - self._roiy1)
				x1  = np.min([self._roix1, self._roix2])
				y1 = np.min([self._roiy1, self._roiy2])
				self._citem = Rectangle((x1,y1), width, height, fc = 'none', ec = 'yellow')

			if self._menucheckRI.get() == 0:
				self._a_img.add_artist(self._citem)
				self._canvas.draw()

	def on_mouseup(self, event):

		self._cpressed = 0

		self._roix2 = event.xdata
		self._roiy2 = event.ydata

		try: self._citem.remove()
		except AttributeError: pass

		try: length_roipath = len(self._roipath)+1
		except AttributeError : length_roipath = 1

		if self._roidrawline.get() == 1:
			self._citem = Line2D([self._roix1, self._roix2],[self._roiy1, self._roiy2],
								c = 'orange')
		elif self._roidrawcircle.get() == 1:
			x1 = np.mean([self._roix1, self._roix2])
			y1 = np.mean([self._roiy1, self._roiy2])
			r = np.sqrt((self._roix2 - x1)**2+(self._roiy2 - y1)**2)
			self._citem = Circle((x1,y1), r, fc = 'none', ec = 'orange')
		elif self._roidrawrect.get() == 1:
			width = np.abs(self._roix2 - self._roix1)
			height = np.abs(self._roiy2 - self._roiy1)
			x1  = np.min([self._roix1, self._roix2])
			y1 = np.min([self._roiy1, self._roiy2])
			self._citem = Rectangle((x1,y1), width, height, fc = 'none', ec = 'orange')

		if self._menucheckRI.get() == 0:
			self._a_img.add_artist(self._citem)
			roi_label = self._a_img.text(self._roix2, self._roiy2, str(length_roipath), ha="center", family='sans-serif', size=14, color = 'yellow')
			self._canvas.draw()

		if self._menucheckMS.get() == 0:
			try:
				self._roipath.append(self._citem)
				self._roilabel.append(roi_label)
			except AttributeError:
				self._roipath = []
				self._roilabel = []
				self._roipath.append(self._citem)
				self._roilabel.append(roi_label)

			if self._roidrawline.get() == 1: roi_type = 'Line '
			elif self._roidrawcircle.get() == 1: roi_type = 'Circle '
			elif self._roidrawrect.get() == 1: roi_type = 'Rectangle '

			if self._menucheckRM.get() == 1:
				self.roiListbox.insert('end', roi_type+str(length_roipath))
			
		elif self._menucheckMS.get() == 1: 
			self._refpath = self._citem

	def noshow_roi(self):

		for item in self._roipath: item.remove()
		for item in self._roilabel: item.remove()

		if self._menucheckRI == 0: self._canvas.draw()

class CalDisplay():

	def init_canvas(self):
		
		try: plt.close(self._f_mch)
		except AttributeError: pass
		
		try: self._mch_canvas.delete(ALL)
		except AttributeError: pass
		
		self._f_mch = Figure(facecolor = [0.95,0.95,0.96])
		self._a_mch = self._f_mch.add_subplot(111)
		
		self._mch_canvas = FigureCanvasTkAgg( self._f_mch, master = self.mch_frameDisplay)
		self._frame_mch_canvas = self._mch_canvas.get_tk_widget()
		self._frame_mch_canvas.grid(row = 1, column = 0, sticky = 'nsew')
		
		self._frame_mch_itoolbar = ttk.Frame(self.mch_frameDisplay)
		self._frame_mch_itoolbar.grid(row = 0, column = 0, sticky = 'nsew')
		self._t_mch = NavigationToolbar2Tk(self._mch_canvas, self._frame_mch_itoolbar)
		
	def show_histo(self, histo, bin_center):
	
		width_bar = 0.95*np.abs(bin_center[1] - bin_center[0])
		self._a_mch.bar(bin_center, histo, 
								width = width_bar, 
								facecolor = 'k',edgecolor = 'w')
		self._mch_canvas.draw()
	
	def show_fit(self, x, fit):
		
		try: self._a_mch.self._mch_fitplot.remove()
		except AttributeError: pass

		self._mch_fitplot = self._a_mch.plot(x, fit, c = 'blue')
		self._mch_canvas.draw()
