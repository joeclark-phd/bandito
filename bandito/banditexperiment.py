
import datetime, random, math
from bandito import Bandit
from banditfunctions import defaultpayoff



class BanditExperiment:
    """
    This object should set up a set of Bandit simulations with given
    parameters and run them as an experiment.  Its output will be a table
    of data, each row containing the variable inputs and the outcomes
    (averaged over replications within each experimental condition).
    
    Arguments except 'debug', 'experiment_name', 'replications', 'arms', and 
    'turns' are lists of values to experiment with.  For each combination
    of values, the simulation is repeated 'replications' times.
    So if you want to test the difference between turbulence of 0 and 0.1, 
    set turbulence=[0,0.1] and the experiment will be set up.
    """
    def __init__(self,
                 debug=True,
                 experiment_name=datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S"),
                 replications=100, # Posen & Levinthal used 25,000
                 arms=10,
                 turns=500,
                 payoff_fxn=[defaultpayoff],
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
        self._debug = debug
        self._expname = experiment_name
        self._reps = replications
        self._arms = arms
        self._turns = turns
        
        self._numexps = len(payoff_fxn)*len(turbulence_fxn)*len(strategy_fxn)*len(turbulence)*len(belief_fxn)*len(strategy)
        self.log("Planning "+str(self._numexps)+" experiments with "+str(replications)+
                 " replications x "+str(turns)+" turns each.\nI.e., a total of "+
                 str(self._numexps*replications*turns)+" turns of processing.\n")
        self._currentexp = 0  # which experiment are we on currently?

        #TODO: open three files: a logfile, a datafile of all simulations, and a datafile of aggregates/averages

        programstart = datetime.datetime.now()
        for pf in payoff_fxn:
            for tf in turbulence_fxn:
                for sf in strategy_fxn:
                    for tb in turbulence:
                        for bf in belief_fxn:
                            for st in strategy:
                                    self.runsims(pf,tf,sf,tb,bf,st)
        self.log("All experiments completed in " + str(datetime.datetime.now() - programstart))
        
        
        
    def runsims(self,payoff_fxn,turbulence_fxn,strategy_fxn,turbulence,belief_fxn,strategy):
        
        # hold the data from each replication (to be averaged later)
        finalscores = []
        finalknowledges = []
        finalopinions = []
        finalprobexplores = []
        
        self._currentexp += 1
        
        self.log("Starting experiment " + str(self._currentexp) +
                 " of " + str(self._numexps) +
                 " with:\n payoff_fxn="+str(payoff_fxn)+
                 "\n turbulence_fxn="+str(turbulence_fxn)+
                 "\n strategy_fxn="+str(strategy_fxn)+
                 "\n belief_fxn="+str(belief_fxn)+
                 "\n turbulence="+str(turbulence)+
                 "\n strategy="+str(strategy))
        expstart = datetime.datetime.now()
        
        for i in range(self._reps):
            b = Bandit( arms=self._arms, turns=self._turns, payoff_fxn=payoff_fxn, turbulence_fxn=turbulence_fxn, strategy_fxn=strategy_fxn, turbulence=turbulence, belief_fxn=belief_fxn,strategy=strategy)
            b.simulate()
            finalscores.append(b.score())
            finalknowledges.append(b.knowledge())
            finalopinions.append(b.opinion())
            finalprobexplores.append(b.probexplore())
            #self.log("simulation "+str(i+1)+" of "+str(self._reps)+" took "+str(b._simtime))
            #TODO: print this simulations' output to a complete datafile
        
        #TODO: print averages to an aggregated datafile
        self.log("FINISHED in "+str(datetime.datetime.now()-expstart)+"\n")
        
    def log(self,message):
        #TODO: log 'message' to a logfile
        if self._debug:
            print(message)  #only print to screen if user wants it wordy for debugging purposes
        


if __name__ == "__main__":
    be = BanditExperiment(strategy=[0.25,0.5])
    




    

