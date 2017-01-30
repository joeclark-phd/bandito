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

# Each of these should produce a dataset like the replication of figure 1, so we can use the same code (I hope) to produce the graph of it. 

BanditExperiment(arms=[5],turns=[100], memory=[100], strategy=[0.02,0.25,0.5,0.75,1], replications=1000, experiment_name="fig1_5arms100turns").run()
BanditExperiment(arms=[5],turns=[2000], memory=[2000], strategy=[0.02,0.25,0.5,0.75,1], replications=1000, experiment_name="fig1_5arms2000turns").run()
BanditExperiment(arms=[20],turns=[100], memory=[100], strategy=[0.02,0.25,0.5,0.75,1], replications=1000, experiment_name="fig1_20arms100turns").run()
BanditExperiment(arms=[20],turns=[2000], memory=[2000], strategy=[0.02,0.25,0.5,0.75,1], replications=1000, experiment_name="fig1_20arms2000turns").run()

from banditfunctions import *

BanditExperiment(strategy=[0.02,0.25,0.5,0.75,1], replications=1000, payoff_fxn=[uniform_payoff], experiment_name="fig1_uniformdist").run()
BanditExperiment(strategy=[0,0.05,0.1,0.15,0.2,0.25], replications=1000, strategy_fxn=[epsilongreedy_strategy], experiment_name="fig1_epsilongreedy").run() # crashed with division by zero problem

# These have different strategy levels and might require slightly different code.  Not sure!

BanditExperiment(strategy=[0.02,0.33,0.67,1], replications=1000, experiment_name="fig1_4taulevels").run()
BanditExperiment(strategy=[0.02,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1], replications=1000, experiment_name="fig1_9taulevels").run()



# Output files will be found in the 'output' directory.
