import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
import os
# import our own files and reload

import market_data
importlib.reload(market_data)

benchmark = 'GOOG' 
#security = 'XLK'
security = 'AAPL'


camp = market_data.capm(benchmark, security)
camp.synchonise_timeseries()
camp.plot_timeseries()
camp.compute_linear_regression()
camp.plot_regression_linear()
# linear regression
































