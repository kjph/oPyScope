import numpy as np

def get_data_csv(path, **kwargs):

    data_raw = np.genfromtxt(path, **kwargs)

    return data_raw[np.logical_not(np.isnan(data_raw[:,1]))]