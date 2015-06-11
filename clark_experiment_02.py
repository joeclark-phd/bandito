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
# This one only uses a few turbulence and latency levels but tries different memory values
BanditExperiment(strategy=[0.02,0.25,0.5,0.75,1], turbulence=[0,0.04,0.08], latency=[0,4,16], memory=[20,40,80,160,320,500] replications=2, experiment_name="clark02")

