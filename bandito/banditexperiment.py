
import datetime, random, math
from bandit import Bandit
from banditfunctions import *



def BanditExperiment(debug=True,
                     replications=100, # Posen & Levinthal used 25,000
                     arms=10,
                     turns=500,
                     payoff_fxn=[betadist_payoff],
                     turbulence_fxn=[randomshock],
                     strategy_fxn=[softmax_strategy],
                     turbulence=[0],
                     belief_fxn=[belief_with_latency],
                     strategy=[0.5],
                     latency=[0],
                     experiment_name=""
                     ):
    """
    This function should set up a set of Bandit simulations with given
    parameters and run them as an experiment.  Its output will be a table
    of data, each row containing the variable inputs and the outcomes
    (averaged over replications within each experimental condition).
    
    Arguments except 'debug', 'experiment_name', 'replications', 'arms', and 
    'turns' are lists of values to experiment with.  For each combination
    of values, the simulation is repeated 'replications' times.
    So if you want to test the difference between turbulence of 0 and 0.1, 
    set turbulence=[0,0.1] and the experiment will be set up.
    """

    programstart = datetime.datetime.now()
    
    _experiment_name = experiment_name if experiment_name else programstart.strftime('%Y%m%d-%H%M%S')
    _logfile = open(("output/"+_experiment_name+"-log.txt"), 'w')
    _datafile = open(("output/"+_experiment_name+"-data.csv"), 'w')
    _datafile.write("EXPERIMENT,REPLICATION,PAYOFF_FXN,TURBULENCE_FXN,STRATEGY_FXN,BELIEF_FXN,TURBULENCE,STRATEGY,SCORE,KNOWLEDGE,OPINION,PROBEXPLORE\n") # CSV header row
    _summaryfile = open(("output/"+_experiment_name+"-summary.csv"), 'w')
    _summaryfile.write("EXPERIMENT,PAYOFF_FXN,TURBULENCE_FXN,STRATEGY_FXN,BELIEF_FXN,TURBULENCE,STRATEGY,MEAN_SCORE,MEAN_KNOWLEDGE,MEAN_OPINION,MEAN_PROBEXPLORE\n") # CSV header row

    def log(message):
        _logfile.write(message)
        if debug:
            print(message)  #only print to screen if user wants it wordy for debugging purposes
        
    _numexps = len(payoff_fxn)*len(turbulence_fxn)*len(strategy_fxn)*len(turbulence)*len(belief_fxn)*len(strategy)
    log("Planning "+str(_numexps)+" experiments with "+str(replications)+
             " replications x "+str(turns)+" turns each.\nI.e., a total of "+
             str(_numexps*replications*turns)+" turns of processing.\n\n")
    _currentexp = 0  # which experiment are we on currently?
    

    # Loop through all experimental conditions and run simulations:
    
    for pf in payoff_fxn:
        for tf in turbulence_fxn:
            for sf in strategy_fxn:
                for tb in turbulence:
                    for bf in belief_fxn:
                        for st in strategy:
                            for lt in latency:
                            
                                # Run several replications of the simulation within one experimental condition:
                            
                                # hold the data from each replication (to be averaged later)
                                finalscores = []
                                finalknowledges = []
                                finalopinions = []
                                finalprobexplores = []
                                
                                _currentexp += 1
                                
                                log("Starting experiment " + str(_currentexp) +
                                    " of " + str(_numexps) +
                                    " with:\n payoff_fxn="+str(pf)+
                                    "\n turbulence_fxn="+str(tf)+
                                    "\n strategy_fxn="+str(sf)+
                                    "\n belief_fxn="+str(bf)+
                                    "\n turbulence="+str(tb)+
                                    "\n strategy="+str(st)+"\n")
                                expstart = datetime.datetime.now()
                                
                                for i in range(replications):
                                
                                    # Do one replication (of many) within an experimental condition:
                                    
                                    b = Bandit( arms=arms, turns=turns, payoff_fxn=pf, turbulence_fxn=tf, strategy_fxn=sf, turbulence=tb, belief_fxn=bf, strategy=st, latency=lt)
                                    b.simulate()
                                    finalscores.append(b.score())
                                    finalknowledges.append(b.knowledge())
                                    finalopinions.append(b.opinion())
                                    finalprobexplores.append(b.probexplore())
                                    # log the data
                                    _datafile.write('{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                                            _currentexp, # experiment number
                                            (i+1), # replication number
                                            str(pf),
                                            str(tf),
                                            str(sf),
                                            str(bf),
                                            str(tb),
                                            str(st),
                                            b.score(),
                                            b.knowledge(),
                                            b.opinion(),
                                            b.probexplore()
                                            ))
                                    #log("simulation "+str(i+1)+" of "+str(replications)+" took "+str(b._simtime))
    
                                # Take average results from all replications (within one experimental condition)
                                # and output them to a 'summary' data file.
                                
                                _summaryfile.write('{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                                    _currentexp,
                                    str(pf),
                                    str(tf),
                                    str(sf),
                                    str(bf),
                                    str(tb),
                                    str(st),
                                    sum(finalscores)/replications,
                                    sum(finalknowledges)/replications,
                                    sum(finalopinions)/replications,
                                    sum(finalprobexplores)/replications
                                    ))
    
                                log("FINISHED in "+str(datetime.datetime.now()-expstart)+"\n\n")
                                
                                # Loop goes to the next experimental condition.




    log("All experiments completed in " + str(datetime.datetime.now() - programstart))
    _logfile.close()
    _datafile.close()
    _summaryfile.close()
        
        
        


if __name__ == "__main__":
    BanditExperiment(strategy=[0.25,0.5])
    




    

