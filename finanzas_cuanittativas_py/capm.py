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

import market_data
importlib.reload(market_data)

def compute_beta(benchmark, security):
    m = model(benchmark, security)
    m.synchonise_timeseries()
    m.compute_linear_regression()
    return m.beta
    

class model:
    
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


class hedger:
    
    def __init__(self, position_ric, position_delta_usd,benchmark,hedger_securities):
        
        self.position_ric = position_ric
        self.position_delta_usd  = position_delta_usd
        self.position_beta = None
        self.position_beta_usd = position_delta_usd
        self.benchmark = benchmark
        self.hedger_securities = hedger_securities
        self.hedger_betas = []
        
    def compute_betas(self):
        self.position_beta = compute_beta(self.benchmark, self.position_ric)
        self.position_beta_usd = self.position_beta_usd * self.position_beta
        for security in self.hedger_securities:
            beta = compute_beta(self.benchmark, security)
            self.hedger_betas.append(beta)
            
    def compute_hedge_weights(self):
        dimensions = len(self.hedger_securities)
        if dimensions != 2:
            print('-------')
            print('Cannot compute exact solution because dimensions = ' + str(dimensions))
            return
        deltas = np.ones([dimensions])
        mtx = np.transpose(np.column_stack((deltas,self.hedger_betas)))
        targets = -np.array([[self.position_delta_usd, self.position_beta_usd]])
        self.optimal_hedge = np.linalg.inv(mtx).dot(targets)
        self.hedger_betas = np.sum(self.optimal_hedge)
        self.hedger_betas_usd = np.transpose(betas).dot(self.optimal_hedge).item()

        
            
        


     
        