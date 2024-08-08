#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 08:20:39 2024

@author: joseph
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
import os

import market_data
importlib.reload(market_data)


class capm:
    
    def __init__(self,benchmark, security, decimals=5):
        self.benchmark = benchmark
        self.security = security
        self.decimals = decimals
        self.timeseries = None
        self.x = x
        self.y = y
        self.alpha = np.round(intercept, self.decimals)
        self.beta = np.round(slope, self.decimals)
        self.p_value = np.round(p_value, self.decimals)
        self.null_hypothesis = p_value > 0.05
        self.corrrelation = np.round(r_value, self.decimals)
        self.r_squared = np.round(r_value**2, self.decimals)
        self.predictor_linreg = intercept + self.slope * self.x
        
    def synchonise_timeseries(self):
        self.timeseries = market_data.synchronise_timeseries(self.benchmark, self.security)
        
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
        slope,intercept, r_value,p_value,std_err = st.linregress(x,y)
        self.alpha = np.round(intercept, self.decimals)
        self.beta = np.round(slope, self.decimals)
        self.p_value = np.round(p_value, self.decimals)
        self.null_hypothesis = p_value > 0.05
        self.corrrelation = np.round(r_value, self.decimals)
        self.r_squared = np.round(r_value**2, self.decimals)
        self.predictor_linreg = intercept + self.slope * self.x