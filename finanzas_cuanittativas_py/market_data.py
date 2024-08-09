#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  4 16:18:08 2024

@author: joseph
"""

import matplotlib as mpl
import scipy
import matplotlib.pyplot as plt
from scipy import stats as st
import numpy as np
import importlib
import pandas as pd
import os

def load_timeseries(ric):
    #directory = '/home/joseph/Documents/personal/quant/books_mastering_financial/finanzas_cuanittativas_py/2024-1-data/'
    directory = '/home/joseph/Documents/proyecto-portafolio/books_mastering_financial/finanzas_cuanittativas_py/2024-1-data/'
    path = directory + ric + '.csv' 
    raw_data = pd.read_csv(path)
    t = pd.DataFrame()
    t['date'] = pd.to_datetime(raw_data['Date'], format='%Y-%m-%d', errors='coerce')
    t['close'] = raw_data['Close']
    t = t.sort_values(by='date', ascending=True)
    t['close_previous'] = t['close'].shift(1)
    t['return'] = t['close']/t['close_previous'] - 1
    t = t.dropna()
    t = t.reset_index(drop=True)
    return t


def synchronise_timeseries(benchmark, security):
    timeseries_x = load_timeseries(benchmark) 
    timeseries_y = load_timeseries(security) 
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
    return timeseries
    
    


class distribution:
    
    # constructor
    def __init__(self, ric,decimals=5):

        self.ric = ric
        self.decimals = decimals
        self.str_title = None
        self.timeseries = None
        self.vector = None
        self.mean_annual = None
        self.volatility_annual = None
        self.sharpe_ratio = None
        self.skewness = None
        self.kurtosis = None
        self.jb_stat =None
        self.p_value =None
        self.is_normal = None 
        self.var_95 = None


        
    def load_timeseries(self):
        self.timeseries = load_timeseries(self.ric)
        self.vector = self.timeseries['return'].values
        self.size  = len(self.vector)
        self.str_title  = self.ric + "| real data"

    def plot_timeseries(self):
        plt.figure()
        self.timeseries.plot(kind='line', x='date', y='close', grid=True, color='blue',
                             title='Timeseries of close prices for ' + self.ric)
        plt.show()


        
    def compute_stats(self, factor = 252):
        
        self.mean_annual = st.tmean(self.vector) * factor
        self.volatility_annual = st.tstd(self.vector) *np.sqrt(factor)
        self.sharpe_ratio =  self.mean_annual / self.volatility_annual if self.volatility_annual > 0 else 0.0
        self.skewness = st.skew(self.vector)
        self.var_95 = np.percentile(self.vector, 5)
        self.kurtosis = st.kurtosis(self.vector)
        self.jb_stat = self.size/6*(self.skewness**2 + 1/4*self.kurtosis**2)
        self.p_value = 1 - st.chi2.cdf(self.jb_stat, df=2)
        self.is_normal = (self.p_value > 0.05) 

    def plot_histogram(self):
        
        self.str_title += 'mean_annual=' + str(np.round(self.mean_annual,self.decimals))\
            + "|" + 'volatility=' + str(np.round(self.volatility_annual,self.decimals)) \
            + '\n' + 'sharpe_ratio=' + str(np.round(self.sharpe_ratio,self.decimals)) \
            + 'Var_95=' + str(np.round(self.var_95,self.decimals)) \
            + '|' + 'skewness=' + str(np.round(self.skewness,self.decimals)) \
            + '\n' + 'kurtosis=' + str(np.round(self.kurtosis,self.decimals))\
            + 'JB stat=' + str(np.round(self.jb_stat,self.decimals)) \
            + '|' + 'p-values=' + str(np.round(self.p_value,self.decimals)) \
            + '\n' + 'kurtosis=' + str(self.is_normal)
        
        # plot
        plt.figure()
        plt.hist(self.vector,bins=100)
        plt.title(self.str_title)
        plt.show()
        

class capm:
    
    def __init__(self,benchmark, security, decimals=5):
        self.benchmark = benchmark
        self.security = security
        self.decimals = decimals
        self.timeseries = None
        self.alpha =None
        self.beta = None
        self.p_value = None
        self.null_hypothesis = None
        self.corrrelation =None
        self.r_squared = None
        self.predictor_linreg = None
        
    def synchonise_timeseries(self):
        self.timeseries = synchronise_timeseries(self.benchmark, self.security)
        
    def plot_timeseries(self):
        
        plt.figure(figsize=(12,5))
        plt.title('Time Series of close prices')
        plt.xlabel('Time')
        plt.ylabel('Prices')
        ax = plt.gca()
        ax1 = self.timeseries.plot(kind='line', x='date', y='close_x', ax=ax, grid=True,\
                              color='blue', label=self.benchmark)
        ax2 = self.timeseries.plot(kind='line', x='date', y='close_y', ax=ax, grid=True,\
                              color='red', secondary_y=True, label=self.security)
        ax1.legend(loc=2)
        ax2.legend(loc=1)

        
    def compute_linear_regression(self):
        self.x = self.timeseries['return_x'].values
        self.y = self.timeseries['return_y'].values
        slope,intercept, r_value,p_value,std_err = st.linregress(self.x,self.y)
        self.alpha = np.round(intercept, self.decimals)
        self.beta = np.round(slope, self.decimals)
        self.p_value = np.round(p_value, self.decimals)
        self.null_hypothesis = p_value > 0.05
        self.corrrelation = np.round(r_value, self.decimals)
        self.r_squared = np.round(r_value**2, self.decimals)
        self.predictor_linreg = intercept + slope * self.x
        
    
    def plot_regression_linear(self):
        
        # plot linear regression
        str_self = 'Linear regression | security ' + self.security\
        + '| benchmark ' + self.benchmark + '\n'\
        + 'alpha (intercept) ' + str(self.alpha)\
        + ' | beta (slope) ' + str(self.beta) + '\n'\
        + 'p_value ' + str(self.p_value)\
        + ' | null hypothesis ' + str(self.null_hypothesis)\
        + 'correl (r_value) ' + str(self.corrrelation)\
        + ' | r_squared ' + str(self.r_squared)

        str_title = 'Scatter of returns' + '\n' + str_self

        plt.figure(figsize=(12,5))
        plt.title(str_title)
        plt.scatter(self.x, self.y)
        plt.plot(self.x,self.predictor_linreg, color='green')
        plt.ylabel(self.security)
        plt.xlabel(self.benchmark)
        plt.grid()
        plt.show()




     
        