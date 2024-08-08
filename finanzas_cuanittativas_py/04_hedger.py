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

position_ric = 'NVDA'
position_delta_usd = 10 # in mn USD
benchmark = '^SPX'
hedger_rics = ['AAPL', 'MSFT']

hedger = capm.hedger(position_ric,position_delta_usd,benchmark,hedger_rics)
hedger.compute_betas()