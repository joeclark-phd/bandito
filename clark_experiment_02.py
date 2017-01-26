# This file introduces experiments with the knowledge renewal capability, modeled as a time window of memory.


# This experiment is reported in: Clark, J. (2016). When are Real-Time Feedback Loops Most Valuable? New Insights from Bandit Simulations of Decision Making in Turbulent Environments. Proceedings of HICSS-49.
# Its results are featured in figs. 7-9.
# For figs. 3-6, see clark_experiment_01.py


# Import statements: do not change

import random
import sys
from os import path
sys.path.insert(0,path.join(sys.path[0],"bandito"))
from bandito.banditexperiment import BanditExperiment

# Run using Python 3.4 on Windows 7, random seed 12345
random.seed(12345)

# Define the experiment:
# This one introduces memory; only needs two latency levels to calculate "cost of latency". 480 experiments.
BanditExperiment(strategy=[0.02,0.25,0.5,0.75,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], latency=[0,16], memory=[20,40,80,160,320,500], replications=1000, experiment_name="clark02b", initial_learning=16).run()

