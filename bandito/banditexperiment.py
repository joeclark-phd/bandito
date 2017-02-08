
import datetime, random, math
from bandit import Bandit
from banditfunctions import *



class BanditExperiment():
    """
    This class sets up a set of Bandit simulations with given
    parameters and (when method "run" is fired) conducts an experiment.  
    Its output will be a table of data, each row containing the variable inputs 
    and the outcomes (averaged over replications within each experimental condition).
    
    Arguments except 'debug', 'experiment_name', 'replications', 'arms', and 
    'turns' are lists of values to experiment with.  For each combination
    of values, the simulation is repeated 'replications' times.
    So if you want to test the difference between turbulence of 0 and 0.1, 
    set turbulence=[0,0.1] and the experiment will be set up.
    """

    def __init__(self,
				 debug=True,
                 replications=100, # Posen & Levinthal used 25,000
                 arms=[10],
                 turns=[500],
                 payoff_fxn=[betadist_payoff],
                 turbulence_fxn=[randomshock],
                 strategy_fxn=[softmax_strategy],
                 turbulence=[0],
                 belief_fxn=[belief_with_latency_and_memory],
                 strategy=[0.5],
                 latency=[0],
                 memory=[500],
                 experiment_name="",
                 timeseries=False,
                 ):
        self.debug = debug
        self.replications = replications
        self.arms = arms
        self.turns = turns
        self.payoff_fxn = payoff_fxn
        self.turbulence_fxn = turbulence_fxn
        self.strategy_fxn = strategy_fxn
        self.turbulence = turbulence
        self.belief_fxn = belief_fxn
        self.strategy = strategy
        self.latency = latency
        self.memory = memory
        self.experiment_name = experiment_name
        self.timeseries = timeseries
	
    def run(self):
        programstart = datetime.datetime.now()
        _experiment_name = self.experiment_name if self.experiment_name else programstart.strftime('%Y%m%d-%H%M%S')
        _logfile = open(("output/"+_experiment_name+"-log.txt"), 'w', buffering=1)
        _datafile = open(("output/"+_experiment_name+"-data.csv"), 'w', buffering=1)
        _datafile.write("EXPERIMENT,REPLICATION,ARMS,TURNS,PAYOFF_FXN,TURBULENCE_FXN,STRATEGY_FXN,BELIEF_FXN,TURBULENCE,STRATEGY,LATENCY,INITIAL_LEARNING,MEMORY,SCORE,KNOWLEDGE,OPINION,PROBEXPLORE\n") # CSV header row
        _summaryfile = open(("output/"+_experiment_name+"-summary.csv"), 'w', buffering=1)
        _summaryfile.write("EXPERIMENT,ARMS,TURNS,PAYOFF_FXN,TURBULENCE_FXN,STRATEGY_FXN,BELIEF_FXN,TURBULENCE,STRATEGY,LATENCY,INITIAL_LEARNING,MEMORY,MEAN_SCORE,MEAN_KNOWLEDGE,MEAN_OPINION,MEAN_PROBEXPLORE\n") # CSV header row
        if self.timeseries: _timeseriesfile = open(("output/"+_experiment_name+"-timeseries.csv"), 'w', buffering=1)


        def log(message):
          _logfile.write(message)
          if self.debug:
              print(message)  #only print to screen if user wants it wordy for debugging purposes
        
        _numexps_without_turns = len(self.arms)*len(self.payoff_fxn)*len(self.turbulence_fxn)*len(self.strategy_fxn)*len(self.turbulence)*len(self.belief_fxn)*len(self.strategy)*len(self.latency)*len(self.memory)
        _numturns = sum([t*_numexps_without_turns for t in self.turns])
        _numexps = _numexps_without_turns*len(self.turns)

        log("Planning "+str(_numexps)+" experiments with "+str(self.replications)+
               " replications x "+" or ".join([str(t) for t in self.turns])+" turns each.\nI.e., a total of "+
               str(self.replications*_numturns)+" turns of processing.\n\n")
        _currentexp = 0  # which experiment are we on currently?
    

      # Loop through all experimental conditions and run simulations:
    
        for ar in self.arms:
            for tu in self.turns:
                #for il in self.initial_learning:
                    for pf in self.payoff_fxn:
                        for tf in self.turbulence_fxn:
                            for sf in self.strategy_fxn:
                                for tb in self.turbulence:
                                    for bf in self.belief_fxn:
                                        for st in self.strategy:
                                            for lt in self.latency:
                                                for mm in self.memory:

                                                    # Run several replications of the simulation within one experimental condition:

                                                    # hold the data from each replication (to be averaged later)
                                                    finalscores = []
                                                    finalknowledges = []
                                                    finalopinions = []
                                                    finalprobexplores = []

                                                    _currentexp += 1

                                                    il = lt #this should guarantee that latency conditions don't wait until turn lt+1 to start learning; they have some initial learning, it's just out of date

                                                    log("Starting experiment " + str(_currentexp) +
                                                        " of " + str(_numexps) +
                                                        " with:"+
                                                        "\n arms="+str(ar)+
                                                        "\n turns="+str(tu)+
                                                        "\n payoff_fxn="+str(pf)+
                                                        "\n turbulence_fxn="+str(tf)+
                                                        "\n strategy_fxn="+str(sf)+
                                                        "\n belief_fxn="+str(bf)+
                                                        "\n turbulence="+str(tb)+
                                                        "\n strategy="+str(st)+
                                                        "\n latency="+str(lt)+
                                                        "\n initial_learning="+str(il)+
                                                        "\n memory="+str(mm)+"\n")
                                                    expstart = datetime.datetime.now()

                                                    for i in range(self.replications):

                                                        # Do one replication (of many) within an experimental condition:

                                                        b = Bandit( arms=ar, turns=tu, payoff_fxn=pf, turbulence_fxn=tf, strategy_fxn=sf, turbulence=tb, belief_fxn=bf, strategy=st, latency=lt, initial_learning=il, memory=mm)
                                                        b.simulate()
                                                        finalscores.append(b.score())
                                                        finalknowledges.append(b.knowledge())
                                                        finalopinions.append(b.opinion())
                                                        finalprobexplores.append(b.probexplore())
                                                        # log the data
                                                        _datafile.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                                                                _currentexp, # experiment number
                                                                (i+1), # replication number
                                                                str(ar),
                                                                str(tu),
                                                                str(pf),
                                                                str(tf),
                                                                str(sf),
                                                                str(bf),
                                                                str(tb),
                                                                str(st),
                                                                str(lt),
                                                                str(il),
                                                                str(mm),
                                                                b.score(),
                                                                b.knowledge(),
                                                                b.opinion(),
                                                                b.probexplore()
                                                                ))
                                                        #log("simulation "+str(i+1)+" of "+str(replications)+" took "+str(b._simtime))
                                                        if self.timeseries:
                                                            _timeseriesfile.write(','.join([str(s) for s in b.allscores()])+'\n')

                                                    # Take average results from all replications (within one experimental condition)
                                                    # and output them to a 'summary' data file.

                                                    _summaryfile.write('{},{},{},{},{},{},{},{},{},{},{},{},{},{},{},{}\n'.format(
                                                        _currentexp,
                                                        str(ar),
                                                        str(tu),
                                                        str(pf),
                                                        str(tf),
                                                        str(sf),
                                                        str(bf),
                                                        str(tb),
                                                        str(st),
                                                        str(lt),
                                                        str(il),
                                                        str(mm),
                                                        sum(finalscores)/self.replications,
                                                        sum(finalknowledges)/self.replications,
                                                        sum(finalopinions)/self.replications,
                                                        sum(finalprobexplores)/self.replications
                                                        ))

                                                    log("FINISHED in "+str(datetime.datetime.now()-expstart)+"\n\n")

                                                    # Loop goes to the next experimental condition.




        log("All experiments completed in " + str(datetime.datetime.now() - programstart))
        _logfile.close()
        _datafile.close()
        _summaryfile.close()
          
        
        


if __name__ == "__main__":
    BanditExperiment(strategy=[0.25,0.5]).run()
    




    

