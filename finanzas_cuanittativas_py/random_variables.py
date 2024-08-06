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


class simulation_inputs:
    def __init__(self):
        self.df = None
        self.scale = None
        self.mean = None
        self.std = None
        self.rv_type = None
        self.size = None

class simulator:
    
    # constructor
    def __init__(self, inputs):
        self.inputs = inputs
        self.str_title = None
        self.vector = None
        self.mu = None
        self.sigma = None
        self.skewness = None
        self.kurt = None
        self.jb_stat =None
        self.p_value =None
        self.is_normal = None 


        
    def generate_vector(self):
        
        self.str_title  = self.inputs.rv_type 
        if self.inputs.rv_type == 'Standard_normal_unitary':
            self.vector = np.random.standard_normal(self.inputs.size)
        elif self.inputs.rv_type == 'normal':
            self.vector = np.random.normal(self.inputs.mean,self.inputs.std,self.inputs.size)
        elif self.inputs.rv_type == 'student':
            self.vector = np.random.standard_t(df=self.inputs.df, size=self.inputs.size)
            self.str_title = self.str_title  + ' df=' + str(self.inputs.df)
        elif self.inputs.rv_type == 'uniform':
            self.vector = np.random.uniform(size=self.inputs.size)
        elif self.inputs.rv_type == 'exponential':
            self.vector = np.random.exponential(scale=self.inputs.scale, size=self.inputs.size)
            self.str_title += ' scale=' + str(self.inputs.scale)
        elif self.inputs.rv_type == 'chi-squared':
            self.vector = np.random.chisquare(df=self.inputs.df, size=self.inputs.size)
            self.str_title  += ' df=' + str(self.inputs.df)
        
    def compute_stats(self):
        
        self.mean = st.tmean(self.vector)
        self.volatility = st.tstd(self.vector)
        self.skewness = st.skew(self.vector)
        self.kurt = st.kurtosis(self.vector)
        self.jb_stat = self.inputs.size/6*(self.skewness**2 + 1/4*self.kurt**2)
        self.p_value = 1 - st.chi2.cdf(self.jb_stat, df=2)
        self.is_normal = (self.p_value > 0.05) 

    def plot(self):
        
        self.str_title += '\n' + 'mean=' + str(np.round(self.mean,self.inputs.decimals)) \
            + '\n' + 'volatility=' + str(np.round(self.volatility,self.inputs.decimals)) \
            + '\n' + 'skewness=' + str(np.round(self.skewness,self.inputs.decimals)) \
            + '\n' + 'kurtosis=' + str(np.round(self.kurt,self.inputs.decimals))\
            + '\n' + 'JB stat=' + str(np.round(self.jb_stat,self.inputs.decimals)) \
            + '\n' + 'p-values=' + str(np.round(self.p_value,self.inputs.decimals)) \
            + '\n' + 'kurtosis=' + str(self.is_normal)
        
        # plot
        plt.figure()
        plt.hist(self.vector,bins=100)
        plt.title(self.str_title)
        plt.show()




        
        

     
        