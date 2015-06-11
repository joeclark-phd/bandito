# This file replicates the basic bandit simulation (like P+L fig 1) at several
# levels of latency in the feedback loop, and several levels of turbulence. The
# goal is to show the "value of real-time feedback" or conversely "the cost of
# latency" at different levels of turbulence.


# Import statements: do not change

import random
import sys
from os import path
sys.path.insert(0,path.join(sys.path[0],"bandito"))
from bandito.banditexperiment import BanditExperiment

# Run using Python 3.4 on Windows 7, random seed 12345
random.seed(12345)

# Define the experiment:
# 1000 reps seems a little more reasonable than P+L's 25000.  This is 240 experimental treatments x 1000 replications and should run in about 6 hours on my laptop.
BanditExperiment(strategy=[0.02,0.25,0.5,0.75,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], latency=[0,1,2,4,8,16], replications=100, experiment_name="clark01")

