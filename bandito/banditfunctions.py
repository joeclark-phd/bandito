# this file stores payoff, turbulence, strategy, and belief functions for re-use
import random, math


def betadist_payoff():
    return random.betavariate(2,2)

def uniform_payoff():
    return random.random()
    
def randomshock(payoffs, payoff_fxn, turbulence):
    # Turbulence as random "shocks" to the environment that re-set
    # the payoffs of the "arms" (with 50% probability for each). 
    # Frequency of shocks is determined by the 'turbulence' variable.
    # From replication of Posen & Levinthal (2012).
    if random.random()<turbulence:
        return [ payoff_fxn() if random.random()<0.5 else x for x in payoffs ]
    else:
        return payoffs
    
def softmax_strategy(beliefs, strategy):
    # Returns an array of probabilities that any particular arm will be
    # chosen.  The believed-best arm will be favored more, and the believed-worst
    # arms will be favored less, as the 'strategy' variable (tau) increases.
    # From replication of Posen & Levinthal (2012).
    return [ math.exp(b/(strategy/10))/sum([ math.exp(a/(strategy/10)) for a in beliefs ]) for b in beliefs ]
    
def epsilongreedy_strategy(beliefs, strategy):
    if random.random() < strategy:
      # explore
      options = [0 if b==max(beliefs) else 1 for b in beliefs]
    else:
      # exploit
      options = [1 if b==max(beliefs) else 0 for b in beliefs]
    # transform 1s to fractions adding up to 1
    if sum(options):
      return list(map( lambda x:x/sum(options), options ))
    else: # avoid divide by zero
      return [ 1/len(options) for o in options ]

def simplebelief(beliefs, tries, wins, latency, memory):
    # Simply calculate tries/wins for each arm to estimate the payoff.
    # This function never forgets and does not weight the data in any way.
    # Note: tries is initialized with 2 and wins with 1, so the first
    # simulated trial will not cause beliefs to jump to 0 or 1.
    # From replication of Posen & Levinthal (2012).
    return [ (sum(wins[i])+1)/(sum(tries[i])+2) for i in range(len(beliefs)) ]
    
def belief_with_latency(beliefs, tries, wins, latency, memory):
    # This algorithm calculates beliefs as wins/tries with one tweak:
    # it ignores tries within the last N turns (N=latency) to simulate
    # a less-than-immediate feedback loop.
    remembered_tries = [tries[i][:-latency] if latency !=0 else tries[i] for i in range(len(beliefs))]
    remembered_wins = [wins[i][:-latency] if latency !=0 else wins[i] for i in range(len(beliefs))]
    return [ (sum(remembered_wins[i])+1)/(sum(remembered_tries[i])+2) for i in range(len(beliefs)) ]
    
def belief_with_latency_and_memory(beliefs, tries, wins, latency, memory):
    # This algorithm calculates beliefs as wins/tries with one tweak:
    # it ignores tries within the last N turns (N=latency) to simulate
    # a less-than-immediate feedback loop.
    m = len(tries[0])-memory # the index of farthest-back remembrance
    m = m - latency # so all learners have the same amount of memory, those with latency remember more further back results
    remembered_tries = [tries[i][m if m>0 else 0:-latency if latency!=0 else None] for i in range(len(beliefs))]
    #print('number of tries = ',len(remembered_tries[0]))
    remembered_wins = [wins[i][m if m>0 else 0:-latency if latency!=0 else None] for i in range(len(beliefs))]
    return [ (sum(remembered_wins[i])+1)/(sum(remembered_tries[i])+2) for i in range(len(beliefs)) ]


    
if __name__ == "__main__":
    print(defaultpayoff())
    
