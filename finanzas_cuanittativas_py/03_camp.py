import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import scipy.stats as st
import importlib
import os
# import our own files and reload

import capm
importlib.reload(capm)

benchmark = 'GOOG' 
security = 'AAPL'

model = capm.model(benchmark, security)
model.synchonise_timeseries()
model.plot_timeseries()
model.compute_linear_regression()
model.plot_regression_linear()

































