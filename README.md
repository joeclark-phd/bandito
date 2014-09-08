###Bandit Model Research Simulations
This work begins by replicating the multi-armed bandit simulation of Posen & Levinthal (2012), "Chasing a Moving Target: Exploitation and Exploration in Dynamic Environments", Management Science 58(3), pp.587-601.  It extends this into a general-purpose bandit simulation with additional variables that can be manipulated for further research.

###Contributors
Joseph W Clark, joseph.w.clark@asu.edu

###To-do
1. Make banditexperiment.py output to data and log files.
1. Complete 'experiment.py' and use it as a demonstration of how to use this software.
1. Add more options
    1. Add "latency" variable to the Bandit class, representing the delay in assimiliating results of trials.
1. Run some experiments
    1. Replicate P&L figure 1
    1. Run experiments on different strategy, turbulence, and latency levels.
1. Code some new variations
    1. Code alternative Turbulence functions.
    1. Run experiments on different types of turbulence.
    1. Implement different Belief functions, in particular, ones that emphasize freshness of information under turbulence.
1. Provide code for data visualizations?
