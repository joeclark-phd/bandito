###Bandit Model Research Simulations
This work begins by replicating the multi-armed bandit simulation of Posen & Levinthal (2012), "Chasing a Moving Target: Exploitation and Exploration in Dynamic Environments", Management Science 58(3), pp.587-601.  It extends this into a general-purpose bandit simulation with additional variables that can be manipulated for further research.

###Contributors
Joseph W Clark, joseph.w.clark@asu.edu

###To-do
1. Add "latency" variable to the Bandit class, representing the delay in assimiliating results of trials.
2. Update Bandit class to take different belief functions.
3. Implement research code that runs lots of simulations and organizes the results data.
4. Run experiments on different strategy, turbulence, and latency levels.
5. Code alternative Turbulence functions.
6. Run experiments on different types of turbulence.
7. Implement different Belief functions, in particular, ones that emphasize freshness of information under turbulence.
