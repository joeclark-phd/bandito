# this file stores payoff, turbulence, strategy, and belief functions for re-use
import random


def defaultpayoff():
    return random.betavariate(2,2)
    
if __name__ == "__main__":
    print(defaultpayoff())
    
