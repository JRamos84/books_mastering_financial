import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
import os
# import our own files and reload

import market_data
importlib.reload(market_data)

benchmark = '^SPX' 
#security = 'XLK'
security = 'SPY'
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

# plot timeseries

plt.figure(figsize=(12,5))
plt.title('Time Series of close prices')
plt.xlabel('Time')
plt.ylabel('Prices')
ax = plt.gca()
ax1 = timeseries.plot(kind='line', x='date', y='close_x', ax=ax, grid=True,\
                      color='blue', label=benchmark)
ax2 = timeseries.plot(kind='line', x='date', y='close_y', ax=ax, grid=True,\
                      color='red', secondary_y=True, label=security)
ax1.legend(loc=2)
ax2.legend(loc=1)