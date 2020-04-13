import tkinter as tk
import numpy as np

from display_an import ROIdisplay, MainDisplay


class ROIdraw():

	def init_var(self):

		self._roidrawline = tk.IntVar()
		self._roidrawcircle = tk.IntVar()
		self._roidrawrect = tk.IntVar()

		self._roidrawline.set(0)
		self._roidrawcircle.set(0)
		self._roidrawrect.set(0)

	def source(self):

		self._cpressed = 0

		if self._menucheckRI.get() == 0:
			canvas = self._canvas
			ROIimage.init_var(self)
		elif self._menucheckRI.get() == 2: canvas = self._canvas

		if self._menucheckRD.get() == 1: ROIdraw.connect_mpl(self, canvas)
		elif self._menucheckRD.get() == 0: ROIdraw.disconnect_mpl(self, canvas)

	def reset(self):

		self._menucheckRD.set(1)
		self._roidrawline.set(0)
		self._roidrawcircle.set(0)
		self._roidrawrect.set(0)

	def line(self):

		if self._menucheckRD.get() == 1:
			self._menucheckRD.set(0)
			ROIdraw.source(self)

		if self._roidrawline.get() == 1:
			self._menucheckRD.set(1)
			self._roidrawcircle.set(0)
			self._roidrawrect.set(0)

		elif self._roidrawline.get() == 0:
			self._menucheckRD.set(0)
			self._roidrawcircle.set(0)
			self._roidrawrect.set(0)

		ROIdraw.source(self)

	def circle(self):

		if self._menucheckRD.get() == 1:
			self._menucheckRD.set(0)
			ROIdraw.source(self)

		if self._roidrawcircle.get() == 1:
			self._menucheckRD.set(1)
			self._roidrawline.set(0)
			self._roidrawrect.set(0)

		elif self._roidrawcircle.get() == 0:
			self._menucheckRD.set(0)
			self._roidrawline.set(0)
			self._roidrawrect.set(0)

		ROIdraw.source(self)

	def rectangle(self):

		if self._menucheckRD.get() == 1:
			self._menucheckRD.set(0)
			ROIdraw.source(self)

		if self._roidrawrect.get() == 1:
			self._menucheckRD.set(1)
			self._roidrawline.set(0)
			self._roidrawcircle.set(0)

		elif self._roidrawrect.get() == 0:
			self._menucheckRD.set(0)
			self._roidrawline.set(0)
			self._roidrawcircle.set(0)

		ROIdraw.source(self)

	def connect_mpl(self, canvas):

		self._cid_press = canvas.mpl_connect('button_press_event',
								lambda event, arg = self: ROIdisplay.on_mousepress(arg, event))
		self._cid_drag = canvas.mpl_connect('motion_notify_event',
								lambda event, arg = self: ROIdisplay.on_mousedrag(arg, event))
		self._cid_up = canvas.mpl_connect('button_release_event',
								lambda event, arg = self: ROIdraw.connect_onmouseup(arg, event))						
								
	def connect_onmouseup(self, event):
		
		ROIdisplay.on_mouseup(self, event)

		try: 
			self._refpath
			ROIimage.setref(self)
			MainDisplay.show_ref(self)
			ROIdraw.connect_mpl(self, self._canvas)
		except AttributeError: pass
		
	def disconnect_mpl(self, canvas):

		canvas.mpl_disconnect(self._cid_press)
		canvas.mpl_disconnect(self._cid_drag)
		canvas.mpl_disconnect(self._cid_up)

class ROIimage():

	def init_var(self):
		self._deledge = tk.IntVar()
		self._delskel = tk.IntVar()

		self._deledge.set(0)
		self._delskel.set(1)

		if self._overedge['enable'].get() == 1:

			self._deledge.set(1)
			self._delskel.set(0)

	def keepdelall(self, keep):

		ROIdraw.reset(self)

		ind_sel = []
		ind_all = np.arange(len(self._inputdata['fiber_xc']))

		for item in np.arange(len(self._roipath)):
			ind_sel.extend(ROIimage.data_roi(self, self._roipath[item]))

		if keep == 0: ind_del = [x for x in ind_all if x in ind_sel]
		elif keep == 1: ind_del = [x for x in ind_all if x not in ind_sel]

		ROIdata.delete(self, ind_del)
		ROIdisplay.noshow_roi(self)

		del self._roipath; del self._roilabel

		if self._menucheckRM.get() == 1:
			self._roiListbox.delete(0, 'end')

		MainDisplay.show_overlay(self)

	def mergeall(self):

		ROIdraw.reset(self)

		ind_sel = []

		for item in np.arange(len(self._roipath)):
			ind_sel.extend(ROIimage.data_roi(self, self._roipath[item]))

		fiber_selec = np.unique(self._inputdata['fiber_number'][ind_sel])
		fn_min = np.min(fiber_selec)
		
		for ifiber in fiber_selec:
			ind_curr = np.where(self._inputdata['fiber_number']==ifiber)[0]
			self._inputdata['fiber_number'][ind_curr] = fn_min

		ROIdata.fiber_new_number(self)
		ROIdisplay.noshow_roi(self)

		del self._roipath; del self._roilabel

		if self._menucheckRM.get() == 1:
			self._roiListbox.delete(0, 'end')

		MainDisplay.show_overlay(self)


	def data_roi(self, id_roi):

		ind_all = np.arange(len(self._inputdata['fiber_number']))


		if self._deledge.get() == 1:
			test1 = []; test2 = []
			if hasattr(id_roi, 'get_radius'):
				test1 = ROIdata.get_incircle(self, id_roi,
											self._inputdata['fiber_x1'],
											self._inputdata['fiber_y1'])
				test2 = ROIdata.get_incircle(self, id_roi,
											self._inputdata['fiber_x2'],
											self._inputdata['fiber_y2'])

			elif hasattr(id_roi, 'get_width'):
				test1 = ROIdata.get_inrect(self, id_roi,
											self._inputdata['fiber_x1'],
											self._inputdata['fiber_y1'])
				test2 = ROIdata.get_inrect(self, id_roi,
											self._inputdata['fiber_x2'],
											self._inputdata['fiber_y2'])

			indices = [ix for ix in ind_all if (ix in test1) or (ix in test2)]

		elif self._delskel.get() == 1:
			test = []
			if hasattr(id_roi, 'get_radius'):

				indices = ROIdata.get_incircle(self, id_roi,
											self._inputdata['fiber_xc'],
											self._inputdata['fiber_yc'])

			elif hasattr(id_roi, 'get_width'):

				indices = ROIdata.get_inrect(self, id_roi,
											self._inputdata['fiber_xc'],
											self._inputdata['fiber_yc'])

		return indices
		
	def data_ref(self, id_roi):
		
		data_fib = np.where(self._inputdata['fiber_number']>=0)[0]
		
		ind_all = np.arange(len(data_fib))
			
		test_1 = ROIdata.get_incircle(self, id_roi,
													self._inputdata['fiber_x1'][data_fib],
													self._inputdata['fiber_y1'][data_fib])
		test_2 = ROIdata.get_incircle(self, id_roi,
													self._inputdata['fiber_x2'][data_fib],
													self._inputdata['fiber_y2'][data_fib])
		test_3 = ROIdata.get_incircle(self, id_roi,
													self._inputdata['fiber_xc'][data_fib],
													self._inputdata['fiber_yc'][data_fib])
		
		indices = [ix for ix in ind_all if (ix in test_1) or (ix in test_2) or (ix in test_3)]
		
		return indices
		
	def setref(self):
		
		ind_sel = ROIimage.data_ref(self, self._refpath)
		data_fib = self._inputdata['fiber_number'][self._inputdata['fiber_number'] >=0]

		for id_fil in np.unique(data_fib[ind_sel]):
			selec_data_indices = np.where(self._inputdata['fiber_number'] == id_fil)[0]
			if np.min(self._inputdata['fiber_number'].flatten()) > 0: fn_min = 0
			else: fn_min = np.min(self._inputdata['fiber_number'].flatten())
			self._inputdata['fiber_number'][selec_data_indices] = fn_min - 1
		
		ROIdata.fiber_new_number(self)

class ROIdata():

	def delete(self, indices):

		self._inputdata['int_profile'] = np.delete(self._inputdata['int_profile'],
													indices, axis = 0)
		self._inputdata['pos_profile'] = np.delete(self._inputdata['pos_profile'],
													indices, axis = 0)
		self._inputdata['fiber_number'] = np.delete(self._inputdata['fiber_number'],
													indices, axis = 0)
		self._inputdata['fiber_slope'] = np.delete(self._inputdata['fiber_slope'],
													indices, axis = 0)

		self._inputdata['fiber_xc'] = np.delete(self._inputdata['fiber_xc'],
												indices, axis = 0)
		self._inputdata['fiber_yc'] = np.delete(self._inputdata['fiber_yc'],
													indices, axis = 0)
		self._inputdata['fiber_x1'] = np.delete(self._inputdata['fiber_x1'],
													indices, axis = 0)
		self._inputdata['fiber_x2'] = np.delete(self._inputdata['fiber_x2'],
													indices, axis = 0)
		self._inputdata['fiber_y1'] = np.delete(self._inputdata['fiber_y1'],
													indices, axis = 0)
		self._inputdata['fiber_y2'] = np.delete(self._inputdata['fiber_y2'],
													indices, axis = 0)

	def fiber_new_number(self):
		try: 
			ind_fib = np.where(self._inputdata['fiber_number'] >=0)[0]
			ind_fib[0]
			nc = -1
			fiber_number = 1*self._inputdata['fiber_number']	
			for ich in np.unique(self._inputdata['fiber_number'][ind_fib]):
				nc = nc + 1
				selec_data_indices = np.where(self._inputdata['fiber_number'] == ich)[0]
				fiber_number[selec_data_indices] = nc
			self._inputdata['fiber_number'] = fiber_number
		except IndexError: pass

	def get_incircle(self, roi_circle, xp, yp):

		ind_all = np.arange(len(xp))

		xo, yo = roi_circle.center
		ro = roi_circle.get_radius()

		dist = np.sqrt((xp-xo)**2+(yp-yo)**2)

		ind_incircle = ind_all[dist<=ro]

		return ind_incircle

	def get_inrect(self, roi_rect, xp, yp):

		ind_all = np.arange(len(xp))

		xo, yo = roi_rect.get_xy()
		width = roi_rect.get_width()
		height = roi_rect.get_height()

		x1 = xo + width
		y1 = xo + height

		ind_1 = (xp >= xo) * (xp <= x1)
		ind_2 = (yp >= yo) * (yp <= y1)

		ind_inrect = ind_all[ind_1&ind_2]

		return ind_inrect

#class ROIshow():

#	def create(self):




