import numpy as np
from skimage.morphology import skeletonize, remove_small_objects, binary_dilation
from skimage.measure import label
from scipy.interpolate import interp1d
import warnings

from display_track import MainDisplay
from wavelet_filters import BuildFFT, Wavelet2D, EdgeDet

class CProfiles():
	def run(self):
		self.exprofilesButton.state(['disabled'])
		ts = int(self._tracking_step)
		if ts == 1: CProfiles.afterload(self)
		elif ts == 2: CProfiles.aftercrop(self)
		elif ts  == 3: CProfiles.afteredge(self)
		elif ts == 4: CProfiles.afterskeleton(self)
		elif ts == 5: CProfiles.aftertrack(self)

		CProfiles.finalstep(self)

	def afterload(self):
		CImageOptions.crop_infostrip(self)
		CEdgeOptions.run(self)
		CSkeletonDetection.runfilter(self)
		CSkeletonDetection.runmask(self)
		CSkeletonDetection.runskeleton(self)
		CFilamentTracking.tracklabel(self)
		CFilamentTracking.localfit(self)

	def aftercrop(self):
		CEdgeOptions.run(self)
		CSkeletonDetection.runfilter(self)
		CSkeletonDetection.runmask(self)
		CSkeletonDetection.runskeleton(self)
		CFilamentTracking.tracklabel(self)
		CFilamentTracking.localfit(self)

	def afteredge(self):
		CSkeletonDetection.runfilter(self)
		CSkeletonDetection.runmask(self)
		CSkeletonDetection.runskeleton(self)
		CFilamentTracking.tracklabel(self)
		CFilamentTracking.localfit(self)

	def afterskeleton(self):
		CFilamentTracking.tracklabel(self)
		CFilamentTracking.localfit(self)

	def aftertrack(self):
		CFilamentTracking.localfit(self)

	def finalstep(self):

		MainDisplay.init_canvas(self)
		MainDisplay.show_image(self)
		self.progressBar.config(mode='determinate', maximum = np.max(self._im.flatten())+1)
		self.progressBar['value'] = 1
		self.progressBar.update()

		ascale = self._tracking_settings['edge_ascale_current'].get()

		xm = 1*self._xmm[self._im>0]; ym = 1*self._ymm[self._im>0];
		im = 1*self._im[self._im>0]; m = self._m[self._im>0]

		int_profile = []; pos_profile = [];
		full_profile = []; full_position = []
		fiber_xc = []; fiber_yc = []
		fiber_x1 = []; fiber_x2 = [];
		fiber_y1 = []; fiber_y2 = []
		fiber_e1 = []; fiber_e2 = []
		fiber_number = [];
		fiber_slope = []
		xprofile = []; yprofile = []

		pix_edge = int(self._tracking_settings['pixels_edge_img'].get())
		pix_back  = int(self._tracking_settings['pixels_background_profile'].get())

		nc = 0

		for icn in np.unique(im):

			self.progressBar['value'] = icn
			self.progressBar.update()

			xcn = xm[np.where(im == icn)];
			ycn = ym[np.where(im == icn)]
			mcn = m[np.where(im == icn)]

			nc = nc+1
			

			for ix in range(len(xcn)):
				print('Filament: ' + str(icn) + ' (' + str(np.unique(im)[-1]) + ') Profile: ' + str(ix+1) + ' (' + str(len(xcn)) + ')')
				if (ycn[ix] >= pix_edge) and (xcn[ix] >= pix_edge):  # if the point lies inside the confidence area determined by the picture edge to discard
					if mcn[ix] >= 1e6:				# if the skeleton line is vertical
						direction = 0
						x_interp = np.arange(0, self._mat_img.shape[1])
						y_interp = np.array([int(x) for x in ycn[ix]*np.ones(len(x_interp))])
						offset_edge = int(ascale) + int(pix_back)
					elif np.abs(mcn[ix]) < 1/self._mat_img.shape[1]:        # if the skeleton line is horizontal
						direction = 1
						y_interp = np.arange(0, self._mat_img.shape[0])
						x_interp = np.array([int(x) for x in xcn[ix]*np.ones(len(y_interp))])
						offset_edge = int(ascale) + int(pix_back)
					else:   # if the skeleton line is diagonal
						direction = 2
						x_pline = np.arange(0, self._mat_img.shape[1])
						y_pline = ycn[ix] + 1/mcn[ix]*(xcn[ix] - x_pline)

						if y_pline[1] > y_pline[-1]:
							if np.max(y_pline) >= self._mat_img.shape[0]: ind_y1 = np.where(y_pline >= self._mat_img.shape[0])[0][-1] + 1
							else: ind_y1 = 1
							if np.min(y_pline) < 0 : ind_y2 = np.where(y_pline < 0)[0][0] - 1
							else: ind_y2 = len(y_pline)
						else:
							if np.max(y_pline) >= self._mat_img.shape[0]: ind_y2 = np.where(y_pline >= self._mat_img.shape[0])[0][0] - 1
							else: ind_y2 = len(y_pline)
							if np.min(y_pline) < 0 : ind_y1 = np.where(y_pline <0)[0][-1] - 1
							else: ind_y1 = 1

						x_profile = [int(x) for x in x_pline[ind_y1: ind_y2]]
						y_profile = [int(x) for x in y_pline[ind_y1: ind_y2]]

						try: 
							f_interp = interp1d(x_profile, y_profile)
							x_interp = np.arange(np.min(x_profile), np.max(x_profile), step = 0.1)
							offset_edge = 10*(int(ascale) + int(pix_back))
							y_interp = f_interp(x_interp)
						except ValueError: 
							x_interp = x_profile; y_interp = y_profile
							offset_edge = int(ascale) + int(pix_back)
							
					x_profile_int = [int(x) for x in x_interp]
					y_profile_int = [int(x) for x in y_interp]

					x_profile = np.array(x_profile_int)
					y_profile = np.array(y_profile_int)

					try:
						xms = np.mean(np.where(np.abs(x_profile - xcn[ix])<2))
						yms = np.mean(np.where(np.abs(y_profile - ycn[ix])<2))
						
						if direction == 0 : posx = int(xms)
						elif direction == 1: posx = int(yms)
						elif direction == 2: posx = int(np.mean([xms, yms]))
						sign_position = 0*x_profile
						sign_position[:posx] = -1; sign_position[posx:] = 1

						mask_profile = 0*self._mask_edge;
						mask_profile[y_profile[posx:], x_profile[posx:]] = 1
						mask_profile[y_profile[:posx], x_profile[:posx]] = -1

						
						mask_overlap = mask_profile*binary_dilation(self._mask_edge)

						try:
							ymatch = np.where(mask_overlap<0)[0]; xmatch = np.where(mask_overlap<0)[1]
							dmatch = np.sqrt((xmatch - xcn[ix])**2 + (ymatch - ycn[ix])**2)
							ind_x1 = xmatch[np.argmin(dmatch)]; ind_y1 = ymatch[np.argmin(dmatch)]
			
							ymatch = np.where(mask_overlap>0)[0]; xmatch = np.where(mask_overlap>0)[1]
							dmatch = np.sqrt((xmatch - xcn[ix])**2 + (ymatch - ycn[ix])**2)
							ind_x2 = xmatch[np.argmin(dmatch)]; ind_y2 = ymatch[np.argmin(dmatch)]
							ind_xmatch = [ind_x1, ind_x2]; ind_ymatch = [ind_y1, ind_y2]
							
							
							try:
								if direction == 0: ind_1 = np.where(x_profile == ind_x1)[0][0]; ind_2 = np.where(x_profile == ind_x2)[0][0]
								else: ind_1 = np.where(y_profile == ind_y1)[0][0]; ind_2 = np.where(y_profile == ind_y2)[0][0]
								xmatch = x_profile[ind_1 - offset_edge:ind_2 + offset_edge]
								ymatch = y_profile[ind_1 - offset_edge:ind_2 + offset_edge]

								full_profile.append(np.array(self._mat_img[y_profile, x_profile]))
								int_profile.append(np.array(self._mat_img[ymatch, xmatch]))
								fiber_xc.append(np.mean([x_profile[ind_1], x_profile[ind_2]]));
								fiber_yc.append(np.mean([y_profile[ind_1], y_profile[ind_2]]))
								fiber_x1.append(x_profile[ind_1]); fiber_x2.append(x_profile[ind_2])
								fiber_y1.append(y_profile[ind_1]); fiber_y2.append(y_profile[ind_2])
								fiber_e1.append(self._WT_m1[fiber_y1[-1],fiber_x1[-1]])
								fiber_e2.append(self._WT_m1[fiber_y2[-1], fiber_x2[-1]])
								fiber_number.append(nc); fiber_slope.append(mcn[ix])
								dist_full = np.sqrt((x_profile - fiber_xc[-1])**2+(y_profile-fiber_yc[-1])**2)*sign_position
								full_position.append(dist_full)
								pos_profile.append(dist_full[ind_1-offset_edge:ind_2+offset_edge])
							except IndexError as e: print('error 182:  ' +str(e))
						except ValueError as e: print('error 183:  ' +str(e))
					except ValueError as e: print('error 184: ' + str(e))

								
		mask_newlabel = 0*self._mat_img
		fx = [int(x) for x in fiber_xc]; fy = [int(x) for x in fiber_yc]
		mask_newlabel[np.array(fy), np.array(fx)] = 1
		
		labelled_filaments = remove_small_objects(label(mask_newlabel), min_size = 3)
		[yl, xl] = np.where(labelled_filaments)
		xy_l = [[xl[ix], yl[ix]] for ix in range(len(xl))]
		new_ind = [0 for x in fiber_xc]	
		for ix in range(0, len(fiber_xc)):
			if [fx[ix], fy[ix]] in  xy_l: new_ind[ix] = 1
		
		new_ind = np.array(new_ind)
		ind_del = np.where(new_ind==0)[0]
		self.progressBar['value'] = icn+1
		self.progressBar.update()

		self._full_int_profile = np.delete(np.array(full_profile), ind_del, axis = 0);
		self._full_position = np.delete(np.array(full_position), ind_del, axis = 0)
		self._int_profile = np.delete(np.array(int_profile), ind_del, axis = 0);
		self._fiber_xc = np.delete(np.array(fiber_xc), ind_del, axis = 0)
		self._fiber_yc = np.delete(np.array(fiber_yc), ind_del, axis = 0)
		self._fiber_x1 = np.delete(np.array(fiber_x1), ind_del, axis = 0)
		self._fiber_x2 = np.delete(np.array(fiber_x2), ind_del, axis = 0)
		self._fiber_y1 = np.delete(np.array(fiber_y1), ind_del, axis = 0)
		self._fiber_y2 = np.delete(np.array(fiber_y2), ind_del, axis = 0)
		self._fiber_e1 = np.delete(np.array(fiber_e1), ind_del, axis = 0)
		self._fiber_e2 = np.delete(np.array(fiber_e2), ind_del, axis = 0)
		self._fiber_number = np.delete(np.array(fiber_number), ind_del, axis = 0)
		self._fiber_slope = np.delete(np.array(fiber_slope), ind_del, axis = 0)
		self._pos_profile = np.delete(np.array(pos_profile), ind_del, axis = 0)

		self.progressBar['value'] = 0
		self.progressBar.update()

class CImageOptions():

	def update_cal(self, event):
		size_nm = self.imgsizeEntry.get()
		try:
			size_nm[1]
			calibration = np.round(int(size_nm)/int(self._img_info['sizepix_x'].get()),5)
			self._img_info['cal_factor'].set(str(calibration))
			self._cal_factor = calibration
			size_nmy = int(self._img_info['sizepix_y'].get()) * calibration

			self._img_info['sizenm_x'].set(int(size_nm))
			self._img_info['sizenm_y'].set(int(size_nmy))

			self._tracking_step = 1

		except IndexError: pass

	def crop_infostrip(self):

		if self._img_info['sizepix_y'].get() == 2207: size_infostrip = 175
		elif self._img_info['sizepix_y'].get() == 1103: size_infostrip = 85

		try:
			self._mat_img = self._source_img[:-size_infostrip, :]
			self._img_info['xmin'].set(0); self._img_info['xmax'].set(int(self._img_info['sizepix_x'].get()))
			self._img_info['ymin'].set(0); self._img_info['ymax'].set(int(int(self._img_info['sizepix_y'].get())-size_infostrip))
			self._img_info['vmin'].set(np.min(self._mat_img.flatten()))
			self._img_info['vmax'].set(np.max(self._mat_img.flatten()))
			self._tracking_step = 2
		except NameError:
			self.imgcropinfoButton.config(text = 'Size not known')
			self.imgcropinfoButton.state(['disabled'])
		MainDisplay.init_canvas(self)
		MainDisplay.show_image(self)


	def crop_selection(self):

		x1, x2 = self._a_img.get_xlim(); y2, y1 = self._a_img.get_ylim()
		if int(x1) < 0 : x1 = 0
		if int(y1) <0 : y1 = 0
		if int(x2) > self._mat_img.shape[1]: x2 = self._mat_img.shape[1]
		if int(y2) > self._mat_img.shape[0]: y2 = self._mat_img.shape[0]

		self._img_info['xmin'].set(int(x1)); self._img_info['xmax'].set(int(x2))
		self._img_info['ymin'].set(int(y1)); self._img_info['ymax'].set(int(y2))

		self._mat_img = self._mat_img[int(y1):int(y2), int(x1):int(x2)]
		self._img_info['vmin'].set(np.min(self._mat_img.flatten()))
		self._img_info['vmax'].set(np.max(self._mat_img.flatten()))

		MainDisplay.init_canvas(self)
		MainDisplay.show_image(self)
		self._tracking_step = 2

	def reset(self):
		self._mat_img = 1*self._source_img

		self._img_info['xmin'].set(0); self._img_info['xmax'].set(int(self._img_info['sizepix_x'].get()))
		self._img_info['ymin'].set(0); self._img_info['ymax'].set(int(self._img_info['sizepix_y'].get()))
		self._img_info['vmin'].set(np.min(self._mat_img.flatten()))
		self._img_info['vmax'].set(np.max(self._mat_img.flatten()))

		MainDisplay.init_canvas(self)
		MainDisplay.show_image(self)

class CEdgeOptions():

	def update_ethlow(self, event):
		th_high =float(self.ethhighSpinbox.get())
		th_low = float(self.ethlowSpinbox.get())

		if th_low <=0 : th_low = 0.001
		elif th_low >= 0.99: th_low = 0.989

		if th_low>th_high:
			if th_low < 0.98: th_high = th_low + 0.001
			else: th_low = th_high - 0.001

		if th_low == th_high: th_high = th_low+0.001

		self.ethlowSpinbox.delete(0,'end');
		self.ethhighSpinbox.delete(0,'end')
		self.ethlowSpinbox.insert(0, str(round(th_low,3)))
		self.ethhighSpinbox.insert(0, str(round(th_high,3)))

	def update_ethhigh(self, event):

		th_low = float(self.ethlowSpinbox.get())
		th_high =float(self.ethhighSpinbox.get())

		if th_high <= 0.01 : th_high = 0.011
		elif th_high >= 1: th_high = 0.999

		if th_high<th_low:
			if th_high >= 0.02: th_low = th_high - 0.001
			else: th_high = th_low + 0.001

		if th_low == th_high: th_low = th_high  - 0.001

		self.ethlowSpinbox.delete(0,'end');
		self.ethhighSpinbox.delete(0,'end')
		self.ethlowSpinbox.insert(0, str(round(th_low,3)))
		self.ethhighSpinbox.insert(0, str(round(th_high,3)))

	def enable_thup(self):

		if self._tracking_settings['edge_thup_use'].get() == 0:
				self.ethupSpinbox.config(state = 'disabled')
				self._tracking_settings['edge_thup_current'].set(1)
		elif self._tracking_settings['edge_thup_use'].get() == 1:
				self.ethupSpinbox.config(state = 'normal')

	def update_ethup(self, event):

		th_up = float(self.ethupSpinbox.get())
		th_high = float(self.ethhighSpinbox.get())

		if th_up<=0.01: th_up = 0.011
		elif th_up >= 1: th_up = 0.999

		if th_up < th_high:
			if th_up >=0.999: th_up = 0.999
			else: th_up = th_high + 0.001

		self.ethupSpinbox.delete(0, 'end')
		self.ethupSpinbox.insert(0, str(round(th_up, 3)))

	def run(self):
		th_high = np.round(
							np.float(
								 self._tracking_settings['edge_thhigh'].get()
										),3)
		th_low = np.round(
						  np.float(
							  self._tracking_settings['edge_thlow'].get()
									  ),3)

		th_up = np.round(
						np.float(
								self._tracking_settings['edge_thup'].get()
									), 3)

		th_high_current= np.round(
									   np.float(
											self._tracking_settings['edge_thhigh_current'].get()
												  ),3)

		th_low_current = np.round(
									  np.float(
										   self._tracking_settings['edge_thlow_current'].get()
												  ),3)

		th_up_current = np.round(
								np.float(
											self._tracking_settings['edge_thup_current'].get()
											), 3)

		ascale = self._tracking_settings['edge_ascale'].get()
		if ascale != self._tracking_settings['edge_ascale_current'].get():
			try: del self._mask_init_edge
			except AttributeError: pass

		run_det = 0

		if th_high != th_high_current: run_det = 1;
		elif th_low != th_low_current: run_det = 1;
		elif th_up != th_up_current: run_det = 1

		try: self._mask_init_edge
		except AttributeError: run_det = 1

		if run_det == 1:
			self._tracking_settings['edge_thhigh_current'].set(str(np.round(th_high,3)))
			self._tracking_settings['edge_thlow_current'].set(str(np.round(th_low,3)))

			self.eshowButton.config(text = 'Show')

			self.progressBar.config(mode='determinate', maximum = 5)
			self.progressBar['value'] = 1
			self.progressBar.update()

			try:
				self._fft_img
			except AttributeError:
				self._xg, self._yg, self._fft_img = BuildFFT.img2D(self)
			self.progressBar['value'] = 2
			self.progressBar.update()

			try: self._mask_init_edge
			except AttributeError:
				self._tracking_settings['edge_ascale_current'].set(ascale)
				self._WT_m1, WT_a1 = Wavelet2D.firstder_gauss(self)
				self.progressBar['value'] = 3
				self.progressBar.update()
				self._mask_init_edge = EdgeDet.canny_wt(self._WT_m1, WT_a1)
			self.progressBar['value'] = 4
			self.progressBar.update()

			self._mask_edge = EdgeDet.hyst_threshold(self)

			if self._tracking_settings['edge_thup_use'].get() == 1:
				self._tracking_settings['edge_thup_current'].set(str(np.round(th_up, 3)))
				self._mask_edge[self._WT_m1/np.max(self._WT_m1.flatten()) >= th_up] = 0

			self.progressBar['value'] = 5
			self.progressBar.update()


		self.eshowButton.config(text = 'Show')
		CEdgeOptions.show(self)

		self._tracking_step = 3

	def show(self):

		if self.eshowButton.cget('text') == 'Show':
			self._overedge['enable'].set(1)
			self.eshowButton.config(text = 'Hide')
		elif self.eshowButton.cget('text') == 'Hide':
			self._overedge['enable'].set(0)
			self.eshowButton.config(text = 'Show')

		MainDisplay.show_overlay(self)

		self.skfilterButton.config(text = 'Filter')
		self.skmaskButton.config(text = 'Mask')

class CSkeletonDetection():

	def runfilter(self):
		ascale = self._tracking_settings['filter_ascale'].get()
		if ascale != self._tracking_settings['filter_ascale_current'].get():
			try: del self._filter_image
			except AttributeError: pass

		try: self._filter_image
		except AttributeError:
			self.progressBar.config(maximum = 3)
			self.progressBar['value']=1; self.progressBar.update()
			try:
				self._fft_img
			except AttributeError:
				self._xg, self._yg, self._fft_img = BuildFFT.img2D(self)
			self.progressBar['value'] = 2; self.progressBar.update()
			self._filter_image =Wavelet2D.gauss(self)
			self.progressBar['value']=3; self.progressBar.update()

		CSkeletonDetection.showfilter(self)
		self.progressBar['value']=0; self.progressBar.update()

	def showfilter(self):
		MainDisplay.init_canvas(self)
		if self.skfilterButton.cget('text') == 'Hide':
			MainDisplay.show_image(self)
			self.skfilterButton.config(text = 'Filter')
		else:
			MainDisplay.show_filter(self);
			self.skfilterButton.config(text = 'Hide')

		if self.skmaskButton.cget('text') == 'Hide':
			MainDisplay.show_mask(self)

		self._canvas.draw()

		self.eshowButton.config(text = 'Show')
		self.skskeletonButton.config(text = 'Skeleton')
		self.tshowlabelButton.config(text = 'Show Labels')
		self.tshowfitButton.config(text = 'Show Fit')

		self._overedge['enable'].set(0)
		self._overskel['enable'].set(0)
		self._overlabel['enable'].set(0)
		self._overfit['enable'].set(0)

	def runmask(self):
		mask_th = float(self.skthSlider.get())
		run_mask = 0; show_mask = 0

		if self.skmaskButton.cget('text') == 'Mask':
			run_mask = 1
		elif mask_th != self._tracking_settings['mask_th'].get():
			run_mask = 1; show_mask = 1

		if run_mask ==1:
			self._tracking_settings['mask_th'].set(mask_th)
			self._mask_image = 0*self._mat_img
			self._mask_image[self._filter_image>=mask_th] = 1

			border_img = int(self._tracking_settings['pixels_edge_img'].get())

			self._mask_image[:border_img,:] = 0
			self._mask_image[-border_img:,:] = 0
			self._mask_image[:,:border_img] = 0
			self._mask_image[:,-border_img:] = 0

			self.tlabelButton.state(['disabled'])
			try:  del self._skeleton_image
			except AttributeError: pass
			self._back_img = np.mean(self._mat_img[self._mask_image == 0].flatten())
		try:
			CSkeletonDetection.showmask(self, show_mask);
		except AttributeError: pass

	def showmask(self, show_mask):
		MainDisplay.init_canvas(self)

		if self.skfilterButton.cget('text') == 'Hide':
			MainDisplay.show_filter(self)
		elif self.skfilterButton.cget('text') == 'Filter':
			MainDisplay.show_image(self)

		if show_mask == 0:
			if self.skmaskButton.cget('text') == 'Hide':
				self.skmaskButton.config(text='Mask')
			elif self.skmaskButton.cget('text') == 'Mask':
				MainDisplay.show_mask(self)
				self.skmaskButton.config(text='Hide')
		elif show_mask == 1:
			MainDisplay.show_mask(self)

		self._canvas.draw()

		self.eshowButton.config(text = 'Show')
		self.skskeletonButton.config(text = 'Skeleton')
		self.tshowlabelButton.config(text = 'Show Labels')
		self.tshowfitButton.config(text = 'Show Fit')

		self._overedge['enable'].set(0)
		self._overskel['enable'].set(0)
		self._overlabel['enable'].set(0)
		self._overfit['enable'].set(0)

	def runskeleton(self):
		try:
			self._skeleton_image
		except AttributeError:
			self.progressBar.config(maximum = 2)
			self.progressBar['value']=1; self.progressBar.update()
			self._skeleton_image = skeletonize(self._mask_image)
			self.progressBar['value']=2; self.progressBar.update()

		CSkeletonDetection.showskeleton(self)
		self.progressBar['value']=0; self.progressBar.update()

		self._tracking_step = 4

	def showskeleton(self):

		if self.skskeletonButton.cget('text') == 'Skeleton':
			self._overskel['enable'].set(1)
			self.skskeletonButton.config(text = 'Hide')
		elif self.skskeletonButton.cget('text') == 'Hide':
			self._overskel['enable'].set(0)
			self.skskeletonButton.config(text = 'Skeleton')

		MainDisplay.show_overlay(self)

		self.skfilterButton.config(text = 'Filter')
		self.skmaskButton.config(text = 'Mask')

	def update_filterth(self, event):
		if self.skthSlider.cget('state') == 'active':
			self.skthSlider.after(200)
			th_filter = self.skthSlider.get()
		else:
			th_filter = self._tracking_settings['mask_th'].get()

		try:
			self._filter_image
			if self.skmaskButton.cget('text') == 'Hide':
				CSkeletonDetection.runmask(self)
			elif self.skfilterButton.cget('text') == 'Filter':
				CSkeletonDetection.showfilter(self)
		except AttributeError: pass

		self.eshowButton.config(text = 'Show')
		self.skskeletonButton.config(text = 'Skeleton')

class CFilamentTracking():

	def tracklabel(self):
		xs = np.where(self._skeleton_image > 0)[1]
		ys = np.where(self._skeleton_image > 0)[0]

		for ij in range(len(xs)):
			mask_jp = self._skeleton_image[ys[ij]-1:ys[ij]+2, xs[ij]-1:xs[ij]+2]
			if np.count_nonzero(mask_jp) >= 4:
				self._skeleton_image[ys[ij], xs[ij]] = 0

		if self._tracking_settings['tracking_lunits'].get() == 2:
			tracking_lmin = int(self._tracking_settings['tracking_lmin'].get())
		else:
			tracking_lmin = int(self._tracking_settings['tracking_lmin'].get()*self._cal_factor)

		try: self._labelled_filaments = remove_small_objects(label(self._skeleton_image), min_size = tracking_lmin)
		except UserWarning: print('e'); self._labelled_filaments = label(self._skeleton_image)
		
		self.tshowlabelButton.config(text = 'Show Labels')
		CFilamentTracking.show_track(self)
		self._tracking_step = 5

	def show_track(self):

		if self.tshowlabelButton.cget('text') == 'Show Labels':
			self._overlabel['enable'].set(1)
			self.tshowlabelButton.config(text = 'Hide Labels')
		elif self.tshowlabelButton.cget('text') == 'Hide Labels':
			self._overlabel['enable'].set(0)
			self.tshowlabelButton.config(text = 'Show Labels')

		MainDisplay.show_overlay(self)

		self.skfilterButton.config(text = 'Filter')
		self.skmaskButton.config(text = 'Mask')

	def localfit(self):
		lf = int(int(self._tracking_settings['tracking_npixfit'].get())/2)

		m = []; xm = []; ym = []; im = []; bm = []
		isc_new = 0

		for isc in np.unique(self._labelled_filaments.flatten())[1:]:
			isc_new = isc_new + 1
			xp = np.where(self._labelled_filaments == isc)[1]
			yp = np.where(self._labelled_filaments == isc)[0]
			for iss in range(len(xp)):
				dist = np.sqrt((xp - xp[iss])**2+ (yp - yp[iss])**2);
				ind_min = np.where(dist<=lf)[0]
				try:
					xf = xp[ind_min]; yf = yp[ind_min]
					with warnings.catch_warnings():
						warnings.filterwarnings('error')
						try:
							m0, b0 = np.polyfit(xf, yf, 1)
							xm.append(xp[iss]); ym.append(yp[iss])
							m.append(m0); im.append(isc_new); bm.append(b0)
						except np.RankWarning:
							try:
								m0, b0 = np.polyfit(yf, xf,1)
								xm.append(xp[iss]); ym.append(yp[iss])
								m.append(1e6); im.append(isc_new); bm.append(b0)
							except np.RankWarning:
								xm.append(0); ym.append(0); m.append(0)
								im.append(0); bm.append(0)
							#if len(np.unique(xf))>3:
							#	xm.append(0); ym.append(0); m.append(0);
							#	im.append(0); bm.append(0)
							#else:
							#	xm.append(xp[iss]); ym.append(yp[iss])
							#	m.append(10*lf); im.append(isc_new); bm.append(yp[iss])
				except IndexError: pass

		self._xmm = np.array(xm); self._ymm = np.array(ym)
		self._m = np.array(m); self._im = np.array(im); self._bm = np.array(bm)


		self.tshowfitButton.config(text = 'Show Fit')
		CFilamentTracking.show_localfit(self)

	def show_localfit(self):

		if self.tshowfitButton.cget('text') == 'Show Fit':
			self._overfit['enable'].set(1)
			self.tshowfitButton.config(text = 'Hide Fit')
		elif self.tshowfitButton.cget('text') == 'Hide Fit':
			self._overfit['enable'].set(0)
			self.tshowfitButton.config(text = 'Show Fit')

		MainDisplay.show_overlay(self)

		self.skfilterButton.config(text = 'Filter')
		self.skmaskButton.config(text = 'Mask')
