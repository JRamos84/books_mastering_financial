import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
import os
# import our own files and reload

import market_data
importlib.reload(market_data)

directory = '/home/joseph/Documents/personal/quant/books_mastering_financial/finanzas_cuanittativas_py/2024-1-data/'
benchmark = '^SPX' 
#security = 'XLK'
security = 'BTC-USD'
# get timeseries of x and y

timeseries_x = market_data.load_timeseries(benchmark) 
timeseries_y = market_data.load_timeseries(security) 
timestamp_x = list(timeseries_x['date'].values)
timestamp_y = list(timeseries_y['date'].values)
timestamp  = list(set(timestamp_x)& set(timestamp_y))
timeseries_x = timeseries_x[timeseries_x['date'].isin(timestamp)]
timeseries_x = timeseries_x.sort_values(by='date', ascending=True)
timeseries_x = timeseries_x.reset_index(drop=True)
timeseries_y = timeseries_y[timeseries_y['date'].isin(timestamp)]
timeseries_y = timeseries_y.sort_values(by='date', ascending=True)
timeseries_y = timeseries_y.reset_index(drop=True)
timeseries = pd.DataFrame()
timeseries['date'] = timeseries_x['date']
timeseries['close_x'] = timeseries_x['close']
timeseries['close_y'] = timeseries_y['close']
timeseries['return_x'] = timeseries_x['return']
timeseries['return_y'] = timeseries_y['return']




