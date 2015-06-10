# This file replicates the experiment of Posen & Levinthal (2012), figure 1.
# To define and run your own experiments, copy and edit this file.


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
# Experimental treatments are defined by assigning lists of values to the arguments 
# of the BanditExperiment function.  The simulation engine will iterate through the lists,
# running the full number of simulation replications (500 by default) for each value. For
# example, Posen & Levinthal's (2012) Figure #1 compared five levels of the strategy variable
# tau from 0.02 to 1.  To replicate their experiment, we assign strategy=[0.02,0.25,0.5,0.75,1]
# and leave all other arguments with their defaults.
#
# Some other arguments do not set up experimental treatments but control the simulation parameters:
# replications, arms, turns, debug, and experiment_name. The optional experiment_name determines the
# name of the output files.  If not assigned, the current datetime will be used.
#
# Default values are used for arguments not assigned values.  
# See bandito/banditexperiment.py to examine the default arguments.

BanditExperiment(strategy=[0.02,0.25,0.5,0.75,1], replications=25000, experiment_name="PLfig1")

# Run this file by typing something like: python sample_experiment.py
# Output files will be found in the 'output' directory.
