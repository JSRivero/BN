import numpy as np
import pandas as pd
import os
import datetime
import data_proc as dp
import epsilon_module as em
import utilities as ut
from matplotlib import pyplot as plt

if __name__ == "__main__":
	start_time = datetime.datetime.now()
	path = r'C:\Users\Javier\Documents\MEGA\Universitattt\Master\Thesis\CDS_data\Russian_processed\data'
	filename = r'entities_data.xlsx'
	cds_ts = dp.read_data(path,filename)
	print(cds_ts)
	[row, col] = cds_ts.shape
	entities_names = cds_ts.loc[:,0]

	russian_cds = cds_ts.iloc[:-3,:]
	start = datetime.datetime(2014, 5, 1)
	end = datetime.datetime(2015, 3, 31)
	date_axis = pd.bdate_range(start, end)

	russian_names = entities_names[:-3]

	input_market_ts = np.zeros([(russian_cds.shape)[0]-1])

	print('Done loading data:' + str(datetime.datetime.now() - start_time))
	print ('----------------------------------------------------------------')

	local_min, local_max = em.compute_local_extremes(cds_ts.iloc[0,1:])
	epsilon_drawups = em.compute_epsilon_drawup(cds_ts.iloc[0,1:],10)

	print(local_min)
	print(type(local_min))
	print(epsilon_drawups)
	print(type(epsilon_drawups))

	ut.plot_epsilon_drawup_cds(cds_ts.iloc[0,1:], local_min, local_max,\
				epsilon_drawups, date_axis)


	#plt.plot(date_axis, cds_ts.iloc[0,1:],'-bx', markevery = epsilon_drawups,markerfacecolor = 'red')
	#plt.plot(date_axis[epsilon_drawups], (cds_ts.iloc[0,1:])[epsilon_drawups], 'rx')
	plt.show()

