# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import datetime
import pytz
import pandas as pd
import MetaTrader5 as mt5
import numpy as np

frame_M15 = mt5.TIMEFRAME_M15 # 15-minute time
frameframe_M30 = mt5.TIMEFRAME_M30 # 30-minute time frame
frame_H1 = mt5.TIMEFRAME_H1 # Hourly time frame
frame_H4 = mt5.TIMEFRAME_H4 # 4-hour time frame
frame_D1 = mt5.TIMEFRAME_D1 # Daily time frame
frame_W1 = mt5.TIMEFRAME_W1 # Weekly time frame
frame_M1 = mt5.TIMEFRAME_MN1 # Monthly time frame

now = datetime.datetime.now()

assets = ['EURUSD', 'USDCHF', 'GBPUSD', 'USDCAD', 'BTCUSD',
'ETHUSD', 'XAUUSD', 'XAGUSD', 'SP500m', 'UK100']

def get_quotes(time_frame, year=2005, month=1, day=1, asset='EURUSD'):
    
    if not mt5.initialize():
        print("Error al inicializar, error code = ", mt5.last_error())
        quit()
    
    timezone = pytz.timezone('Europe/Paris')
    
    time_from = datetime.datetime(year, month, day, tzinfo=timezone)
    time_to = datetime.datetime.now(timezone)+datetime.timedelta(days=1)
    rates = mt5.copy_rates_range(asset, timeframe, time_from, time_to)
    rates_frame = pd.DataFrame(rates)
    
    return rates_frame

def mass_import(asset, time_frame):
    
    if time_frame == 'H1':
        data = get_quotes(frame_H1, 2013, 1, 1, asset=asset)
        data = data.iloc[:,1:5]
        data = data.round(decimals=5)
        
        
    if time_frame == 'D1':
        data = get_quotes(frame_D1, 2000,1,1,asset=asset)
        data = data.iloc[:,1:5]
        data = data.round(decimals=5)
    return data
    

def add_column(data, times):
    for i in range(1, times + 1):
        new = np.zeros((len(data) + 1), dtype=float)
        
        data = np.append(data, new, axis=1)
    return data 

def delete_column(data, index, times):
    
    for i in range(1, times+1):
        data = np.delete(data, index, axis=1)
    return data
    
## The function to add Rowns to an array

def add_row(data, times):
    for i in range(1, times+ 1):
        columns = np.shape(data)[1]
        
        new = np.zeros((1, columns), dtype=float)
        
        data = np.append(data, new, axis=0)
    return data

# The Functionto remove rows fron an array

def delete_row(data, number):
    data = data[number:,]
    
    return data

# The function to round numbers

def rounding(data, how_far):
    
    data = data.round(decimals=how_far)
    return data


## Coding Signals


def signal(data):
    data = add_column(data, 5)
    
    for i in range(len(data)):
        
        try:
            
            if data[i,2] < data[i - 5,2] and data[i,2] < data[i - 13,2]:
                and data[i,2] > data[i - 21, 2] and
                data[i,3]>data[i -1, 3] and[i,4] == 0:
                    data[i+1,4] = 1
            elif data[i,1] > data[i -5, 1] and 
            data[i,1] > data[i -13, 1] and
            data[i,1] < data[i-21,1] and data[i,3] < data[i-1,3] and data[i,5]==0:
                    data[i+1,5] == -1
        except IndexError:
            pass
    return data
    
    
    
    
    
    
    
    
    
    
    
    
    
    