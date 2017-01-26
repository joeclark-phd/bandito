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



# Define the experiment:

BanditExperiment(strategy=[0.02,0.25,0.5,0.75,1], turbulence=[0,0.005,0.01,0.02,0.04,0.08,0.16,0.32], replications=25000, experiment_name="PLfig3")

# Warning: this took over 14 hours for my laptop to simulate.  While testing, you may want to decrease the number of replications to fewer than 25000!
