
import datetime, random, math
from bandito import Bandit
from banditfunctions import betadist_payoff, randomshock, softmax_strategy, simplebelief



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
                 replications=100, # Posen & Levinthal used 25,000
                 arms=10,
                 turns=500,
                 payoff_fxn=[betadist_payoff],
                 turbulence_fxn=[randomshock],
                 strategy_fxn=[softmax_strategy],
                 turbulence=[0],
                 belief_fxn=[simplebelief],
                 strategy=[0.5],
                 experiment_name=""
                 ):
                 
        programstart = datetime.datetime.now()
        
        self._experiment_name = experiment_name if experiment_name else programstart.strftime('%Y%m%d-%H%M%S')
        self._logfile = open(("output/"+self._experiment_name+"-log.txt"), 'w')
        self._datafile = open(("output/"+self._experiment_name+"-data.csv"), 'w')
        self._datafile.write("EXPERIMENT,REPLICATION,PAYOFF_FXN,TURBULENCE_FXN,STRATEGY_FXN,BELIEF_FXN,TURBULENCE,STRATEGY,SCORE,KNOWLEDGE,OPINION,PROBEXPLORE\n") # CSV header row
        self._summaryfile = open(("output/"+self._experiment_name+"-summary.csv"), 'w')
        self._summaryfile.write("EXPERIMENT,PAYOFF_FXN,TURBULENCE_FXN,STRATEGY_FXN,BELIEF_FXN,TURBULENCE,STRATEGY,MEAN_SCORE,MEAN_KNOWLEDGE,MEAN_OPINION,MEAN_PROBEXPLORE\n") # CSV header row

        #TODO: also add an average/aggregate datafile
                 
        self._debug = debug
        self._expname = experiment_name
        self._reps = replications
        self._arms = arms
        self._turns = turns
        
        self._numexps = len(payoff_fxn)*len(turbulence_fxn)*len(strategy_fxn)*len(turbulence)*len(belief_fxn)*len(strategy)
        self.log("Planning "+str(self._numexps)+" experiments with "+str(replications)+
                 " replications x "+str(turns)+" turns each.\nI.e., a total of "+
                 str(self._numexps*replications*turns)+" turns of processing.\n\n")
        self._currentexp = 0  # which experiment are we on currently?

        
        for pf in payoff_fxn:
            for tf in turbulence_fxn:
                for sf in strategy_fxn:
                    for tb in turbulence:
                        for bf in belief_fxn:
                            for st in strategy:
                                    self.runsims(pf,tf,sf,tb,bf,st)
        self.log("All experiments completed in " + str(datetime.datetime.now() - programstart))
        self._logfile.close()
        
        
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
                 "\n strategy="+str(strategy)+"\n")
        expstart = datetime.datetime.now()
        
        for i in range(self._reps):
            b = Bandit( arms=self._arms, turns=self._turns, payoff_fxn=payoff_fxn, turbulence_fxn=turbulence_fxn, strategy_fxn=strategy_fxn, turbulence=turbulence, belief_fxn=belief_fxn,strategy=strategy)
            b.simulate()
            finalscores.append(b.score())
            finalknowledges.append(b.knowledge())
            finalopinions.append(b.opinion())
            finalprobexplores.append(b.probexplore())
            # log the data
            self._datafile.write('{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                    self._currentexp, # experiment number
                    (i+1), # replication number
                    str(payoff_fxn),
                    str(turbulence_fxn),
                    str(strategy_fxn),
                    str(belief_fxn),
                    str(turbulence),
                    str(strategy),
                    b.score(),
                    b.knowledge(),
                    b.opinion(),
                    b.probexplore()
                    ))
            #self.log("simulation "+str(i+1)+" of "+str(self._reps)+" took "+str(b._simtime))
        
        #TODO: print averages to an aggregated datafile #self._summaryfile.write("EXPERIMENT,PAYOFF_FXN,TURBULENCE_FXN,STRATEGY_FXN,BELIEF_FXN,TURBULENCE,STRATEGY,MEAN_SCORE,MEAN_KNOWLEDGE,MEAN_OPINION,MEAN_PROBEXPLORE\n") # CSV header row
        self._summaryfile.write('{},{},{},{},{},{},{},{},{},{},{}\n'.format(
            self._currentexp,
            str(payoff_fxn),
            str(turbulence_fxn),
            str(strategy_fxn),
            str(belief_fxn),
            str(turbulence),
            str(strategy),
            sum(finalscores)/self._reps,
            sum(finalknowledges)/self._reps,
            sum(finalopinions)/self._reps,
            sum(finalprobexplores)/self._reps
            ))

        self.log("FINISHED in "+str(datetime.datetime.now()-expstart)+"\n\n")
        
    def log(self,message):
        self._logfile.write(message)
        if self._debug:
            print(message)  #only print to screen if user wants it wordy for debugging purposes
        


if __name__ == "__main__":
    be = BanditExperiment(strategy=[0.25,0.5])
    




    

