## Bandit Model Research Simulations
This work begins by replicating the multi-armed bandit simulation of Posen & Levinthal (2012), "Chasing a Moving Target: Exploitation and Exploration in Dynamic Environments", Management Science 58(3), pp.587-601.  It extends this into a general-purpose bandit simulation with additional variables that can be manipulated for further research.

### Contributors
Joseph W Clark, joe.clark@maine.edu

### File Structure

- All files in this directory (except `README.md`) define experiments.
- The `output` subfolder will hold the data and log output from simulation experiments.
- The `analysis` subfolder contains some sample scripts for visualizing the data with Python.
- Files in the `bandito` subfolder run the actual experiments:
  - `/bandito/bandit.py` runs one replication of a bandit simulation.
  - `/bandito/banditexperiment.py` runs an experiment with any specified set of treatments and number of replications.
  - `/bandito/banditfunctions.py` contains algorithms for turbulence, strategy, beliefs, and payoffs. To implement a new algorithm, place it there.

### How to Use
Copy the file `sample_experiment.py` and modify to set up your experiment.  Run it with something like the following:

    python sample_experiment.py
    
Warning: You may want to change the number of replications for a faster test.  Posen & Levinthal used 25000 replications for each experimental treatment, and replicating their experiments may take hours or days.

Tested on Mac OS X with Python 3.5.2
