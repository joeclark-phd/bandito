# This file runs variations on the replication of Posen & Levinthal (2012), figure 1,
# altering the number of turns and arms, the strategy function, payoff distribution function,
# and choices of strategy levels to test.  The idea is to prove that the findings are robust
# to arbitrary details of implementation.



# Import statements: do not change

import random
import sys
from os import path
sys.path.insert(0,path.join(sys.path[0],"bandito"))
from bandito.banditexperiment import BanditExperiment

# By setting a random number seed, you can try to guarantee that your results are repeatable.
# Making note of your operating system and Python versions is also advisable.
# Simply comment out the following two lines if you want new random results each time you run the program.

# test experiments used random seed 12345
random.seed(12345)

# Define the experiment:

BanditExperiment(arms=[5,20],turns=[2000], memory=[2000], strategy=[0.02,0.25,0.5,0.75,1], replications=100, experiment_name="2000turns").run()
BanditExperiment(arms=[5,20],turns=[100], memory=[100], strategy=[0.02,0.25,0.5,0.75,1], replications=100, experiment_name="100turns").run()

# Run this file by typing something like: python sample_experiment.py
# Output files will be found in the 'output' directory.
