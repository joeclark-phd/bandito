import random
import itertools
import bisect
import math




class Bandit:
    """
    With default parameters, this object should set up a single run
    of the multi-armed bandit simulation described by Posen & Levinthal
    in their 2012 Management Science paper.  The simulate() method
    will cause it to run all time periods (500 by default), and return
    the run time.  The other methods may be used to capture outcome
    data like the ending asset stock.
    """
    def __init__(self,
                 arms=10,
                 turns=500,
                 payoff_fxn=
                    lambda: random.betavariate(2,2),
                 turbulence_fxn= 
                    lambda payoffs, payoff_fxn, turbulence:  
                    [ payoff_fxn() if random.random()<0.5 else x for x in payoffs ] 
                    if random.random()<turbulence else payoffs,
                 strategy_fxn=
                    lambda beliefs, strategy:
                    [ math.exp(b/(strategy/10))/sum([ math.exp(a/(strategy/10)) for a in beliefs ]) for b in beliefs ],
                 turbulence=0,
                 strategy=0.5
                 ):
        self._arms = arms
        self._turns = turns
        self._assetstock = 0
        self._complete = False
        
        self._payoff_fxn = payoff_fxn 
        # User can pass in any random number generating function; 
        # by default the payoffs for each arm are drawn from a Beta 
        # distribution with alpha=2 and beta=2. This is a normal-like
        # distribution bounded between 0 and 1, with mean = 0.50 and 
        # std. dev. = 0.22.
        self._payoffs = [self._payoff_fxn() for i in range(arms)] 

        self._turbulence_fxn = turbulence_fxn
        self._turbulence = turbulence
        # In Posen&Levinthal, there is a set probability of turbulence 
        # occurring in any given turn (determined here by the turbulence
        # parameter, with a default of 0, no turbulence).  When it occurs,
        # it is manifested as a re-draw of some payoffs from the initial
        # beta distribution.  Each "arm" has an independent probability
        # of 0.5 of having its payoff re-drawn.  Each turn this program
        # will call self._turbulence_fxn( self._payoffs, self._payoff_fxn,
        # self._turbulence ), so if you provide a custom turbulence function,
        # the self._turbulence variable should be used to hold any variable 
        # parameters or configuration.
        
        self._strategy_fxn = strategy_fxn
        self._strategy = strategy
        # The _strategy_fxn returns probabilities, one for each "arm", that
        # the gambler will choose that arm.  This could be all 0s with one 1,
        # or some other distribution that adds up to 1.  By default we use
        # the SOFTMAX algorithm described by Posen & Levinthal. The function
        # is called with self._strategy_fxn( self._beliefs, self._strategy )
        # so the self._strategy variable should be used to hold any variable
        # parameters or configuration. By default, it is the "tau" of the 
        # SOFTMAX calculation.
        
        self._beliefs = [0.5 for i in range(arms)]
        # According to Hart Posen (personal communication), the initial
        # belief of 0.5 is simulated as two trials with one success;
        # this way the first true trial is averaged in as if it were
        # the third trial, so the belief will not jump to 0.0 or 1.0.
        # We simply keep track of the # tries and # wins for each arm.
        self._tries = [2 for i in range(arms)]
        self._wins = [1 for i in range(arms)]
        
    def simulate(self):
        # todo: store starting time
        for t in range(self._turns):
        
            # implement turbulence
            self._payoffs = self._turbulence_fxn( self._payoffs, self._payoff_fxn, self._turbulence)
            
            # determine gambler's choice
            choice_probabilities = self._strategy_fxn( self._beliefs, self._strategy )
            cumdist = list(itertools.accumulate(choice_probabilities))
            x = random.random()
            choice = bisect.bisect(cumdist,x)
            
            # The gambler's choice results in a win or a loss (a gain or loss of 1 "asset stock")
            self._tries[choice] += 1
            if random.random() < self._payoffs[choice]:
                self._wins[choice] += 1
                self._assetstock += 1
            else:
                self._assetstock -= 1
                
            # Update beliefs
            self._beliefs[choice] = self._wins[choice] / self._tries[choice]
            # Beliefs are simply the proportion of trials of each arm that have resulted in wins.
            # todo: implement the belief computation as a passed-in function, so that alternative models (such as exponentially weighted moving average) could be substituted
            
            # todo: compute + store "knowledge" and "opinion" theoretical variables

        self._complete = True
        # todo: check elapsed time and return it
        

    def score(self):
        if self._complete:
            return self._assetstock
        else:
            return None
            # todo: decide: if they request the score without first running the simulation, should we run self.simulate() for them? or raise an exception, or what?



if __name__ == "__main__":
    b = Bandit()
    assert b.score() == None
    b.simulate()
    print( "final asset stock:", b.score() )





    

