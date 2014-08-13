import random

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
                 payoff_fxn=lambda: random.betavariate(2,2),
                 turbulence_fxn=None,
                 arms=10,
                 turns=500,
                 turbulence=0):
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
        #todo: allow user to plug in a different random number function or different parameters

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
            # todo: run environmental turbulence
            # todo: determine player's choice
            # todo: capture the consequences of the player's choice
            pass
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
    assert b.score() == 0
    print(b._payoffs)
    print(b._payoff_fxn)
    print(b._payoff_fxn())
    print(b._payoff_fxn())




    

