import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
import os
# import our own files and reload
import random_variables
importlib.reload(random_variables)

# inputs
ric = 'SPY'

directory = '/home/joseph/Documents/proyecto-portafolio/books_mastering_financial/finanzas_cuanittativas_py/2024-1-data/'
path = directory + ric + '.csv' 
raw_data = pd.read_csv(path)
t = pd.DataFrame()
t['date'] = pd.to_datetime(raw_data['Date'])
t['close'] = raw_data['Close']
t.sort_values(by='date', ascending=True)
t['close_previous'] = t['close'].shift(1)
t['return_close'] = t['close']/t['close_previous'] - 1
t = t.dropna()
t = t.reset_index(drop=True)


# inputs
inputs = random_variables.simulation_inputs()
inputs.rv_type = ric + ' | real data'
# options: standard_normal normal student uniform exponential chi-squared
inputs.decimals = 5

# computations
sim = random_variables.simulator(inputs)
sim.vector = t['return_close'].values
sim.inputs.size  = len(sim.vector)
sim.str_title = sim.inputs.rv_type
sim.compute_stats()
sim.plot()

rics = []
is_normals = []
for file_name in os.listdir(directory):
    if not file_name.endswith('.csv'):
        continue
    
    ric = file_name.split('.')[0]
    if ric == 'ReadMe':
        continue

    path = directory + ric + '.csv' 
    print(path)
    raw_data = pd.read_csv(path)
    t = pd.DataFrame()
    t['date'] = pd.to_datetime(raw_data['Date'])
    t['close'] = raw_data['Close']
    t.sort_values(by='date', ascending=True)
    t['close_previous'] = t['close'].shift(1)
    t['return_close'] = t['close']/t['close_previous'] - 1
    t = t.dropna()
    t = t.reset_index(drop=True)
    sim = random_variables.simulator(inputs)
    sim.vector = t['return_close'].values
    sim.inputs.size  = len(sim.vector)
    sim.str_title = sim.inputs.rv_type
    sim.compute_stats()
    #Generate list
    rics.append(ric)
    is_normals.append(sim.is_normal)
df = pd.DataFrame()
df['rics'] = rics
df['is_normal'] = is_normals



