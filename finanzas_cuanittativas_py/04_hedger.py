#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug  8 15:04:50 2024

@author: joseph
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
import os
# import our own files and reload

import capm
importlib.reload(capm)

# inputs 

position_security= 'NVDA'
position_delta_usd = 10 # in mn USD
benchmark = '^SPX'
hedger_security = ['AAPL', 'MSFT']

hedger = capm.hedger(position_security,position_delta_usd,benchmark,hedger_security)
hedger.compute_betas()
hedger.compute_hedge_weights()