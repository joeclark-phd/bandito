
import datetime, random, math
from bandito import Bandit




class BanditExperiment:
    """
    This object should set up a set of Bandit simulations with given
    parameters and run them as an experiment.  Its output will be a table
    of data, each row containing the variable inputs and the outcomes
    (averaged over replications within each experimental condition).
    
    Each argument except 'experiment_name', 'replications', 'arms', and 
    'turns' is a list of values to experiment with.  For each combination
    of values, the simulation is repeated 'replications' times.
    So if you want to test the difference between turbulence of 0 and 0.1, 
    set turbulence=[0,0.1] and the experiment will be set up.
    """
    def __init__(self,
                 experiment_name=datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S"),
                 replications=100, # Posen & Levinthal used 25,000
                 arms=10,
                 turns=500,
                 payoff_fxn=
                    [lambda: random.betavariate(2,2)],
                 turbulence_fxn= 
                    [lambda payoffs, payoff_fxn, turbulence:  
                    [ payoff_fxn() if random.random()<0.5 else x for x in payoffs ] 
                    if random.random()<turbulence else payoffs],
                 strategy_fxn=
                    [lambda beliefs, strategy:
                    [ math.exp(b/(strategy/10))/sum([ math.exp(a/(strategy/10)) for a in beliefs ]) for b in beliefs ]],
                 turbulence=[0],
                 belief_fxn=
                    [lambda beliefs, tries, wins:
                    [ wins[i]/tries[i] for i in range(len(beliefs)) ]],
                 strategy=[0.5]
                 ):
        self._expname = experiment_name
        self._reps = replications
        self._arms = arms
        self._turns = turns
        
        #TODO: print a message about how many experiments and reps will run
        #TODO: open three files: a logfile, a datafile of all simulations, and a datafile of aggregates/averages
        for pf in payoff_fxn:
            for tf in turbulence_fxn:
                for sf in strategy_fxn:
                    for tb in turbulence:
                        for bf in belief_fxn:
                            for st in strategy:
                                    self.runsims(pf,tf,sf,tb,bf,st)
                                        
    def runsims(self,payoff_fxn,turbulence_fxn,strategy_fxn,turbulence,belief_fxn,strategy):
        
        # hold the data from each replication (to be averaged later)
        finalscores = []
        finalknowledges = []
        finalopinions = []
        finalprobexplores = []
        
        #TODO: print a one-liner about what experiment is running
        #TODO: capture starting time
        
        for i in range(self._reps):
            b = Bandit( arms=self._arms, turns=self._turns, payoff_fxn=payoff_fxn, turbulence_fxn=turbulence_fxn, strategy_fxn=strategy_fxn, turbulence=turbulence, belief_fxn=belief_fxn,strategy=strategy)
            b.simulate()
            finalscores.append(b.score())
            finalknowledges.append(b.knowledge())
            finalopinions.append(b.opinion())
            finalprobexplores.append(b.probexplore())
            #TODO: print this simulations' output to a complete datafile
        
        #TODO: print averages to an aggregated datafile
        #TODO: announce how much time it took
        
        


if __name__ == "__main__":
    be = BanditExperiment(strategy=[0.25,0.5])
    




    

