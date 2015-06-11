# This file continues experiment 01 with some additional latency values, just because I have some overnight machine time to use.


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
BanditExperiment(strategy=[0.02,0.25,0.5,0.75,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], latency=[32,48,64,80], replications=1000, experiment_name="clark02")

