import numpy as np 
import pandas as pd 
import os

def read_data(path,filename):
	if filename.endswith('.xlsx'):
		return pd.read_excel(os.path.join(path,filename))
	else:
		return pd.DataFrame(np.load(os.path.join(path,filename)))