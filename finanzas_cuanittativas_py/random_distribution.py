import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
import os
# import our own files and reload
import random_variables
importlib.reload(random_variables)
import market_data
importlib.reload(market_data)

directory = '/home/joseph/Documents/personal/quant/books_mastering_financial/finanzas_cuanittativas_py/2024-1-data/'
ric = 'MA'
# computations
dist = market_data.distribution(ric)
dist.load_timeseries()
dist.plot_timeseries()
dist.compute_stats()
dist.plot_histogram()



# rics = []
# is_normals = []
# for file_name in os.listdir(directory):
#     if not file_name.endswith('.csv'):
#         continue
    
#     ric = file_name.split('.')[0]
#     if ric == 'ReadMe':
#         continue
#     path = directory + ric + '.csv' 
#     dist = market_data.distribution(ric)
#     dist.load_timeseries()
#     dist.compute_stats()
#     #Generate list
#     rics.append(ric)
#     is_normals.append(dist.is_normal)
# df = pd.DataFrame()
# df['rics'] = rics
# df['is_normal'] = is_normals
# df =  df.sort_values(by='is_normal', ascending=True)



