import matplotlib as mpl
import scipy
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2
import numpy as np
import importlib

import random_variables
importlib.reload(random_variables)

# inputs
coeff = 200
# df in student and chi-squared, scale in exponential
size = 10**6
random_variable_type = 'normal'
# options: normal student uniform exponential chi-squared
decimals = 5

sim = random_variables.simulator(coeff, random_variable_type)
sim.generate_vector()
sim.compute_stats()
sim.plot()
# code





