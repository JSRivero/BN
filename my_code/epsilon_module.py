import numpy as np
import pandas as pd
import os
from matplotlib import pyplot as plt

def compute_local_extremes(cds_data):
	''' Computes the indeces of local minima and local maxima
	Arguments: cds data in an array (one dimension)

	Returns: Two 1-D arrays, with minima and local maxima
	'''
	local_min = (np.diff(np.sign(np.diff(cds_data))) > 0).nonzero()[0] + 1
	local_max = (np.diff(np.sign(np.diff(cds_data))) < 0).nonzero()[0] + 1

	return local_min, local_max

def compute_std_deviation(cds_data, local_ext, time_param):
	''' Computes the standard deviation of the last "time_param" days at the 
	local_ext points. If it is in the first time_param days it computes
	the standard deviation of the first time_param days.

	Arguments:
	cds_data: 1-D np array of CDS spread time series
	local_ext: 1-D array of local minima or maxima
	time_param:integer for variance parameter corresponding to epsilon parameter

	Returns:
	List of standard deviations corresponding to local minima and maxima
	'''

	time_param = np.round(time_param)
	std_dev = []
	
	for index in local_ext:
		if index < time_param:
			std_dev.append(np.std(cds_data[:time_param], ddof = 1))
		else:
			std_dev.append(np.std(cds_data[index - time_param + 1: index + 1], ddof = 1))

	return std_dev

def compute_epsilon_drawup(cds_data, time_param):
	''' Calculates epsilon draw-ups for the time series of an entity
	based on the standard deviation
	'''

	local_min, local_max = compute_local_extremes(cds_data)
	epsilon_stddev_up_relative = compute_std_deviation(\
								cds_data, local_min, time_param)
	epsilon_stddev_down_relative = compute_std_deviation(\
								cds_data, local_max, time_param)
	# Scaling
	# epsilon_stddev_up_relative = [up_scale * stddev_up \
	# 						for stddev_up in epsilon_stddev_up_relative]
	# epsilon_stddev_down_relative = [down_scale * stddev_down \
	# 						for stddev_down in epsilon_stddev_down_relative]

	# Computation of the epsilon drawups based on the standard deviation
	epsilon_drawups_relative = calibrate_epsilon_drawups(\
							cds_data, local_min, local_max,\
							epsilon_stddev_up_relative,\
							epsilon_stddev_down_relative)

	return epsilon_drawups_relative




def calibrate_epsilon_drawups(cds_data, local_min, local_max, \
	epsilon_stddev_up, epsilon_stddev_down):
	''' Calibrates the epsilon draw-ups based on input parameters

	Arguments:
	cds_data: 1d numpy array of time series of spreads
	epsilon_stddev_up: list of epsilon draw-ups at local minima
	epsilon_stddev_down: list of epsilon draw-downs at local maxima
	local_min: list of indices of local minima
	local_max: list of indices of local maxima
	min_max_order_diff: difference parameter for ordering local minima and maxima

	Returns:
	epsilon_drawups: 1d numpy array of epsilon draw-ups

	'''
	# Needs to start with a minima
	if local_min[0] < local_max[0]:
		# Needs to end with a max
		if local_min[-1] > local_max[-1]:
			local_min = local_min[0:-1]
			epsilon_stddev_up = epsilon_stddev_up[0:-1]
			#local_max = local_max[0:-2]
			#epsilon_stddev_down = epsilon_stddev_down[0:-2]
	else:
		local_max = local_max[1:]
		epsilon_stddev_down = epsilon_stddev_down[1:]
		# Needs to end with a max
		if local_min[-1] > local_max[-1]:
			local_min = local_min[0:-1]
			epsilon_stddev_up = epsilon_stddev_up[0:-1]
			#local_max_index = local_max_index[0:-2]
			#epsilon_stddev_down = epsilon_stddev_down[0:-2]

	epsilon_drawups = []
	index = 0
	index_correction = 0
	# Correction for the quantity of local minima and maxima
	if(np.abs(len(local_min)-len(local_max)))>2:
		index_correction = np.abs(len(local_min)-len(local_max))

	while index < len(local_min) - 2 - index_correction:
		if cds_data[local_max[index]]-cds_data[local_min[index]] > epsilon_stddev_up[index]:
			epsilon_drawups.append(local_min[index])
		index += 1

	return epsilon_drawups