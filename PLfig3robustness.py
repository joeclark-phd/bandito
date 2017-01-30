# This file replicates the experiment of Posen & Levinthal (2012), figure 3.


# Import statements: do not change

import random
import sys
from os import path
sys.path.insert(0,path.join(sys.path[0],"bandito"))
from bandito.banditexperiment import BanditExperiment

# By setting a random number seed, you can try to guarantee that your results are repeatable.
# Making note of your operating system and Python versions is also advisable.
# Simply comment out the following two lines if you want new random results each time you run the program.

random.seed(12345)


# Variations on the simulation to test the robustness of P+L 2012's figure 3 to different parameters

BanditExperiment(arms=[5],turns=[100], memory=[100], strategy=[0.02,0.25,0.5,0.75,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], replications=1000, experiment_name="fig3_5arms100turns").run()
BanditExperiment(arms=[5],turns=[2000], memory=[2000], strategy=[0.02,0.25,0.5,0.75,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], replications=1000, experiment_name="fig3_5arms2000turns").run()
BanditExperiment(arms=[20],turns=[100], memory=[100], strategy=[0.02,0.25,0.5,0.75,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], replications=1000, experiment_name="fig3_20arms100turns").run()
BanditExperiment(arms=[20],turns=[2000], memory=[2000], strategy=[0.02,0.25,0.5,0.75,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], replications=1000, experiment_name="fig3_20arms2000turns").run()

from banditfunctions import *

BanditExperiment(strategy=[0.02,0.25,0.5,0.75,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], replications=1000, payoff_fxn=[uniform_payoff], experiment_name="fig3_uniformdist").run()
BanditExperiment(strategy=[0,0.05,0.1,0.15,0.2,0.25], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], replications=1000, strategy_fxn=[epsilongreedy_strategy], experiment_name="fig3_epsilongreedy").run()

BanditExperiment(strategy=[0.02,0.33,0.67,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], replications=1000, experiment_name="fig3_4taulevels").run()
BanditExperiment(strategy=[0.02,0.125,0.25,0.375,0.5,0.625,0.75,0.875,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], replications=1000, experiment_name="fig3_9taulevels").run()

