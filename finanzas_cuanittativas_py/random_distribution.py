import matplotlib as mpl
import scipy
import matplotlib.pyplot as plt
from scipy.stats import skew, kurtosis, chi2
import numpy as np
import importlib

import random_variables
importlib.reload(random_variables)
#inputs
inputs = random_variables.simulation_input()
inputs.df = 23 # degrees of freedom or df in student and chi-squared
inputs.scale=17 # scale in exponential
inputs.mean = 5 # mean in normal
inputs.std = 10 # standard deviation ot std in normal
inputs.size = 10**6
inputs.rv_type = 'real'
# options: standard_normal, normal, student, uniform, exponetial, chi-squared'
inputs.decimals = 5


#Computations
sim = random_variables.simulator(inputs)
sim.generate_vector()
sim.compute_stats()
sim.plot()
# code





