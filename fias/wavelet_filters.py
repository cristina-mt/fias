import numpy as np

class BuildFFT():

	def img2D(self):
	
		x = np.arange(-self._mat_img.shape[1]/2, self._mat_img.shape[1]/2)
		y = np.arange(-self._mat_img.shape[0]/2, self._mat_img.shape[0]/2)
		xg = np.tile(x, (len(y),1)); yg = np.tile(y, (len(x), 1)).transpose()

		fft_img = np.fft.fftshift(np.fft.fft2(self._mat_img))

		return xg, yg, fft_img
		
class Wavelet2D():

	def firstder_gauss(self):
		a_scale = float(self._tracking_settings['edge_ascale'].get())

		phi = np.exp(-((self._xg/a_scale)*(self._xg/a_scale)+(self._yg/a_scale)*(self._yg/a_scale))/2)
		phi_x = -(self._xg/a_scale)*phi; phi_y = -(self._yg/a_scale)*phi
		phi_xg = 1/(a_scale**2)*phi_x; phi_yg  = 1/(a_scale**2)*phi_y
		fft_phi_x=np.fft.fftshift(np.fft.fft2(phi_xg));fft_phi_y=np.fft.fftshift(np.fft.fft2(phi_yg))
		WT_x=np.fft.ifftshift(np.fft.ifft2(fft_phi_x*self._fft_img));
		WT_y=np.fft.ifftshift(np.fft.ifft2(fft_phi_y*self._fft_img));

		WT_mod=np.sqrt(np.abs(WT_x)**2+np.abs(WT_y)**2)
		WT_arg = np.angle(WT_x + 1j*WT_y, deg = True)

		return WT_mod, WT_arg
		
	def gauss(self):
		a_scale = float(self._tracking_settings['filter_ascale'].get())

		phi = np.exp(-((self._xg/a_scale)*(self._xg/a_scale)+(self._yg/a_scale)*(self._yg/a_scale))/2)
		phi_xg = phi/np.sum(phi.flatten())
		fft_phi_x=np.fft.fftshift(np.fft.fft2(phi_xg));
		WT_x=np.fft.ifftshift(np.fft.ifft2(fft_phi_x*self._fft_img));
		WT_mod = np.abs(WT_x)

		return WT_mod
		
class EdgeDet():
	
	def canny_wt(WT_mod, WT_arg):
		rWT_arg = 45.*np.round(WT_arg/45)
		dir_sa=[0.,45.,90.,135.,-180.,-135.,-90.,-45.]
		WT_mod_0=np.zeros(WT_mod.shape);
		WT_mod_45=np.zeros(WT_mod.shape);
		WT_mod_90=np.zeros(WT_mod.shape)
		WT_mod_135=np.zeros(WT_mod.shape);
		WT_mod_m180=np.zeros(WT_mod.shape);
		WT_mod_m135=np.zeros(WT_mod.shape)
		WT_mod_m90=np.zeros(WT_mod.shape);
		WT_mod_m45=np.zeros(WT_mod.shape)

		WT_mod_0[:,:-1]=WT_mod[:,1:];
		WT_mod_m180[:,1:]=WT_mod[:,: -1];
		WT_mod_90[:-1,:]=WT_mod[1:,:];
		WT_mod_m90[1:,:]=WT_mod[:-1,:];
		WT_mod_45[:-1,:-1]=WT_mod[1:,1:];
		WT_mod_m135[1:,1:]=WT_mod[:-1,:-1];
		WT_mod_135[:-1,1:]=WT_mod[1:,:-1];
		WT_mod_m45[1:,:-1]=WT_mod[:-1,1:];

		WT_mod_ap=[WT_mod_0,WT_mod_45,
							WT_mod_90,WT_mod_135,
							WT_mod_m180,WT_mod_m135,
							WT_mod_m90,WT_mod_m45]
		WT_mod_am=[WT_mod_m180,WT_mod_m135,
							 WT_mod_m90,WT_mod_m45,
							 WT_mod_0,WT_mod_45,
							 WT_mod_90,WT_mod_135]

		mask_edge=np.zeros(WT_mod.shape)
		for idir in range(len(dir_sa)):
			mask_angle=rWT_arg==dir_sa[idir];
			mask_edge[mask_angle*np.greater(WT_mod,WT_mod_ap[idir])*np.greater(WT_mod,WT_mod_am[idir])]=1
			nWT_mod=WT_mod/np.max(WT_mod.flatten())

		return mask_edge

	def hyst_threshold(self):
		mask_edge = self._mask_init_edge
		th_low = float(self._tracking_settings['edge_thlow'].get())
		th_high =  float(self._tracking_settings['edge_thhigh'].get())
		
		WT_norm = self._WT_m1 /np.max(self._WT_m1.flatten())
		mask_high = mask_edge*(WT_norm>=th_high)
		mask_low = mask_edge*(WT_norm>=th_low)*(WT_norm<th_high)

		mask_edge_hyst = 1*mask_high
		for iy in np.where(mask_high>0)[0]:
			if (iy>1) and (iy<mask_high.shape[0]):
				for ix in np.where(mask_high[iy,:]>0)[0]:
					if (ix>1) and (ix<mask_high.shape[1]):
						test_sq = mask_low[iy-1:iy+2, ix-1:ix+2]
						if np.sum(test_sq.flatten())>0:
							mask_edge_hyst[iy-1:iy+2, ix-1:ix+2] = mask_edge_hyst[iy-1:iy+2, ix-1:ix+2] + test_sq

		mask_edge_hyst[mask_edge_hyst>0] = 1
		
		border_img = int(self._tracking_settings['pixels_edge_img'].get())
		
		mask_edge_hyst[:border_img,:] = 0
		mask_edge_hyst[-border_img:,:] = 0
		mask_edge_hyst[:,:border_img] = 0
		mask_edge_hyst[:,-border_img:] = 0

		return mask_edge_hyst
		