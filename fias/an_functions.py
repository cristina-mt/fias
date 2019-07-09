import numpy as np


class FitFunctions():

	def gauss(x, a, x0, sigma):

		return a*np.exp(-(x-x0)**2/(2*sigma**2))