import tkinter as tk
from tkinter import ttk

import time as t

import numpy as np

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.patches import Circle, Rectangle, PathPatch
import matplotlib.pyplot as plt
from matplotlib import path, patches


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

	def show_image(self):

		colormap = self._colormap_options.get('Current Main')
		if colormap is None:
			colormap = self._colormap_options.get('Source')
			self._colormap_options['Current Main'] = self._colormap_options.get('Source')
			if colormap is None:
				self._colormap_options['Current Main'] = 'gray'
				colormap = 'gray'

		self._s_img = self._a_img.imshow(self._mat_img, cmap = colormap)

	def show_overlay(self):

		MainDisplay.init_canvas(self)
		MainDisplay.show_image(self)

		if self._overskel['enable'].get() == 1:
				self._a_img.scatter(np.where(self._skeleton_image>0)[1],
								np.where(self._skeleton_image>0)[0],
								s = int(self._overskel['size'].get()),
								edgecolor = self._overskel['ecolor'].get(),
								facecolor = self._overskel['fcolor'].get()
								)

		if self._overedge['enable'].get() == 1:
			self._a_img.scatter(np.where(self._mask_edge>0)[1],
								np.where(self._mask_edge>0)[0],
								s = int(self._overedge['size'].get()),
								edgecolor = self._overedge['ecolor'].get(),
								facecolor = self._overedge['fcolor'].get()
								)

		if self._overlabel['enable'].get() == 1:
			self._a_img.scatter(np.where(self._labelled_filaments>0)[1],
								np.where(self._labelled_filaments>0)[0],
								s = int(self._overlabel['size'].get()),
								edgecolor= self._overlabel['ecolor'].get(),
								c = self._labelled_filaments[self._labelled_filaments>0]
								)
		if self._overfit['enable'].get() == 1:
			npix = int(self._tracking_settings['tracking_npixfit'].get())/2
			for pm in np.arange(0, len(self._m), step = 2):
				if self._m[pm]<1e6:
					x = np.arange(self._xmm[pm] - npix, self._xmm[pm] + npix)
					self._a_img.plot(x,
									x*self._m[pm] + self._bm[pm],
									c= self._overfit['color'].get(),
									lw = self._overfit['lwidth'].get())
				else:
					y = np.arange(self._ymm[pm] - npix, self._ymm[pm] + npix)
					self._a_img.plot(0*y + self._bm[pm], y,
											c = self._overfit['color'].get(),
											lw = self._overfit['lwidth'].get())
			self._a_img.set_xlim([0, self._mat_img.shape[1]])
			self._a_img.set_ylim([self._mat_img.shape[0], 0])

		self._canvas.draw()

	def show_filter(self):

		colormap = self._colormap_options.get('Current Main')
		if colormap is None:
			colormap = self._colormap_options.get('Source')
			self._colormap_options['Current Main'] = self._colormap_options.get('Source')
			if colormap is None:
				self._colormap_options['Current Main'] = 'gray'
				colormap = 'gray'

		self._s_img = self._a_img.imshow(self._filter_image,
							 cmap = colormap)

	def show_mask(self):
		self._a_img.imshow(self._mask_image,
									 cmap = 'Greens',
									 interpolation = 'none',
									 alpha = 0.3)

	def show_extract(self, profiles, fiber_center, fiber_edges):

		try:
			self._profile_line.remove()
			self._fiber_center.remove()
			self._fiber_edge_1.remove()
			self._fiber_edge_2.remove()
		except AttributeError: pass

		self._profile_line = self._a_img.scatter(profiles[0], profiles[1], c = 'yellow', s = 5, edgecolor = 'none')
		self._fiber_center = self._a_img.scatter(fiber_center[0], fiber_center[1], c = 'red', s = 5, edgecolor = 'none')
		self._fiber_edge_1 = self._a_img.scatter(fiber_edges[0], fiber_edges[1], c = 'orange', s = 5, edgecolor = 'none')
		self._fiber_edge_2 = self._a_img.scatter(fiber_edges[2], fiber_edges[3], c = 'orange', s = 5, edgecolor = 'none')

		self._canvas.draw()


class OIdisplay():

	def init_canvas(self):
		try: plt.close(self._f_oimg)
		except AttributeError: pass

		try: self._oi_canvas.delete(ALL)
		except AttributeError: pass

		self._f_oimg = Figure(facecolor = [0.95,0.95,0.96])
		self._f_oimg.subplots_adjust(left = 0.0, bottom = 0.0,
												right = 1.0, top = 1.0,
												wspace = 0, hspace = 0)
		self._a_oimg = self._f_oimg.add_subplot(111);
		self._a_oimg.axis('off')
		self._oi_canvas = FigureCanvasTkAgg(
							   self._f_oimg, master = self.iot_frameMain)
		self._oi_frame_canvas = self._oi_canvas.get_tk_widget()
		self._oi_frame_canvas.grid(row = 1, column = 0, sticky = 'nsew')

		self._oi_frame_itoolbar = ttk.Frame(self.iot_frameMain)
		self._oi_frame_itoolbar.grid(row = 0, column = 0, sticky = 'nsew')
		self._t_oimg = NavigationToolbar2Tk(
						  self._oi_canvas, self._oi_frame_itoolbar)

	def show_image(self):
		colormap = self._colormap_options.get('Source')
		self._s_oimg = self._a_oimg.imshow(self._source_img, cmap = colormap)

		try:
			x1 = self._img_info['xmin'].get(); x2 = self._img_info['xmax'].get()
			y1 = self._img_info['ymin'].get(); y2 = self._img_info['ymax'].get()
			width = np.abs(x2 - x1); height = np.abs(y2 - y1)
			citem = Rectangle((x1, y1), width, height, fc = 'none', ec = 'green')
			self._a_oimg.add_artist(citem)
		except ValueError: pass

		self._canvas.draw()

	def hide_delete(self):
		try: plt.close(self._f_oimg)
		except AttributeError: pass

		try: self._oi_canvas.delete(ALL)
		except AttributeError: pass

class CMdisplay():

	def show_colormaps(self):

		screen_height = self.ico_frame.winfo_screenheight()

		try: plt.close(self._f_ic)
		except AttributeError: pass

		try: self._ic_canvas.delete(ALL)
		except AttributeError: pass

#		self._f_ci = Figure(facecolor = [0.95,0.95,0.96], figsize=(5,10))
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

		self._a_hi.hist(self._mat_img.flatten(), 100, fc = 'k', ec = 'w')
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
		self._cpressed =1

		self._roix1 = event.xdata
		self._roiy1 = event.ydata

		if self._drawmethod == 0: self._citem = Circle((self._roix1, self._roiy1), 1, fc = 'none', ec = 'yellow')
		elif self._drawmethod == 1: self._citem = Rectangle((self._roix1, self._roiy1), 1, 1, fc = 'none', ec = 'yellow')
		self._a_img.add_artist(self._citem)
		self._canvas.draw()

	def on_mousedrag(self, event):

		if self._cpressed == 1:
			self._citem.remove()
			self._canvas.draw()
			self._roix2 = event.xdata
			self._roiy2 = event.ydata

			if self._drawmethod == 0:
				x1 = np.mean([self._roix1, self._roix2])
				y1 = np.mean([self._roiy1, self._roiy2])
				r = np.sqrt((self._roix2 - x1)**2+(self._roiy2 - y1)**2)
				self._citem = Circle((x1,y1), r, fc = 'none', ec = 'yellow')
			elif self._drawmethod == 1:
				width = np.abs(self._roix2 - self._roix1)
				height = np.abs(self._roiy2 - self._roiy1)
				x1  = np.min([self._roix1, self._roix2])
				y1 = np.min([self._roiy1, self._roiy2])
				self._citem = Rectangle((x1,y1), width, height, fc = 'none', ec = 'yellow')
			self._a_img.add_artist(self._citem)
			self._canvas.draw()

	def on_mouseup(self, event):

		self._roix2 = event.xdata
		self._roiy2 = event.ydata

		self._citem.remove()

		try: length_roipath = len(self._roipath)+1
		except AttributeError : length_roipath = 1

		if self._drawmethod == 0:
			x1 = np.mean([self._roix1, self._roix2])
			y1 = np.mean([self._roiy1, self._roiy2])
			r = np.sqrt((self._roix2 - x1)**2+(self._roiy2 - y1)**2)
			self._citem = Circle((x1,y1), r, fc = 'none', ec = 'orange')
		elif self._drawmethod == 1:
			width = np.abs(self._roix2 - self._roix1)
			height = np.abs(self._roiy2 - self._roiy1)
			x1  = np.min([self._roix1, self._roix2])
			y1 = np.min([self._roiy1, self._roiy2])
			self._citem = Rectangle((x1,y1), width, height, fc = 'none', ec = 'orange')
		self._a_img.add_artist(self._citem)
		roi_label = self._a_img.text(self._roix2, self._roiy2, str(length_roipath), ha="center", family='sans-serif', size=14, color = 'yellow')

		self._canvas.draw()
		self._cpressed = 0

		try:
			self._roipath.append(self._citem)
			self._roilabel.append(roi_label)
		except AttributeError:
			self._roipath = []
			self._roilabel = []
			self._roipath.append(self._citem)
			self._roilabel.append(roi_label)

		if self._drawmethod == 0: roi_type = 'Circle '
		elif self._drawmethod == 1: roi_type = 'Rectangle '
		elif self._drawmethod == 2: roi_type = 'Polygon '
		self.roiListbox.insert('end', roi_type+str(length_roipath))

		self.roiselectallButton.state(['!disabled'])
		self.roiclearallButton.state(['!disabled'])
		self.roideleteallButton.state(['!disabled'])
		self.roikeepallButton.state(['!disabled'])

	def draw_selec(self, event):

		for item in self._roipath: item.set_ec('orange')
		for item in self.roiListbox.curselection():
			self._roipath[item].set_ec('green')

		self._canvas.draw()

	def show_roi(self):

		for item in self._roipath: self._a_img.add_artist(item)
		for item in self._roilabel: self._a_img.add_artist(item)
		self._canvas.draw()

	def noshow_roi(self):

		for item in self._roipath:
			item.set_ec('orange')
			item.remove()
		for item in self._roilabel: item.remove()
		self._canvas.draw()
