# -*- coding: utf-8 -*-
"""
This file will develop a visualization to show "value of real-time feedback", 
or conversely, "cost of latency in feedback" at a variety of turbulence levels.
"""

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# read the summary data
#df = pd.read_csv("clark01a-summary.csv") #clark01a was the version before the initialization bias fix
df = pd.read_csv("clark01b-summary.csv") #clark01b was the version after the initialization bias fix

# levels of latency and turbulence
latencys = df.LATENCY.unique()
turbs = df.TURBULENCE.unique()


# to hold the calculated values at each level of latency for one level of turbulence
optimumstrategy=np.empty((len(turbs),len(latencys)))
meanperformance=np.empty((len(turbs),len(latencys)))
maxperformance=np.empty((len(turbs),len(latencys)))
secondderiv=np.empty((len(turbs),len(latencys)))


# loop through all turbulence levels
for t in turbs:
    # loop through all latency levels
    for l in latencys:
        subset = df[(df.TURBULENCE==t)&(df.LATENCY==l)]    
        # fit the 3rd order polynomial
        poly = np.poly1d(np.polyfit(subset.STRATEGY,subset.MEAN_SCORE,3))
        # find the roots of the derivative
        optima = poly.deriv().r
        # maxima are optima where 2nd derivative is negative; or could be at x= 0 or 1
        concave_maxima = optima[poly.deriv().deriv()(optima)<0] # this is it in almost every case
        other_possible_maxima = [0,1] # sometimes you get a weird polynomial, though. may be useful to print out optstrat just to see when that happens
        all_possible_maxima = np.concatenate([other_possible_maxima,concave_maxima]) if concave_maxima.any() else other_possible_maxima
        optstrat = all_possible_maxima[poly(all_possible_maxima).argmax()]
        #i got optstrat=0 with turb 0, latency 16 and opstrat=1 with turb 0.32, latency 8 or 16. these are the edge cases for turbulence and the highest latency conditions. maybe I should drop them as outliers?
        #print("turb: "+str(t)+", latency: "+str(l)+", optstrat: "+str(optstrat))
        optimumstrategy[np.argmax(turbs==t)][np.argmax(latencys==l)] = optstrat
        meanperformance[np.argmax(turbs==t)][np.argmax(latencys==l)] = np.mean(subset.MEAN_SCORE)
        maxperformance[np.argmax(turbs==t)][np.argmax(latencys==l)] = poly(optstrat)
        secondderiv[np.argmax(turbs==t)][np.argmax(latencys==l)] = poly.deriv().deriv()(optstrat)



# this code block generates my first figure: cost of latency for T=0
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
t=0
ax.plot(range(len(latencys)),maxperformance[t], color='black', linewidth=3, label='Best Performance')
ax.set_xticks(range(len(latencys)))
ax.set_xticklabels(latencys)
ax.set_ylim([230,300])
ax.set_xlim([-0.5,len(latencys)-.5])
ax.set_ylabel("Performance")
ax.set_xlabel("Latency in Feedback (turns)")
ax.set_title("Attainable Performance at Turbulence=0\nwith Various Levels of Latency")
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=2,label='Performance')
plt.legend(handles=[performance_line],loc=3)
plt.show()

# this code block generates my second figure: cost of latency for T=0 with optimal strategy
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
t=0
ax.plot(range(len(latencys)),maxperformance[t], color='black', linewidth=3, label='Best Performance')
ax.set_xticks(range(len(latencys)))
ax.set_xticklabels(latencys)
ax.set_ylim([230,300])
ax.set_xlim([-0.5,len(latencys)-.5])
ax.set_ylabel("Performance")
ax.set_xlabel("Latency in Feedback (turns)")
ax.set_title("Attainable Performance and Strategy at\nTurbulence=0 with Various Levels of Latency")
ax2=ax.twinx()
ax2.plot(range(len(latencys)),optimumstrategy[t],"k--")
ax2.set_xlim([-0.5,len(latencys)-.5])
ax2.set_ylim([0,1])
ax2.set_ylabel("Strategy (tau)")
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=2,label='Performance')
strategy_line = mlines.Line2D([],[],color='black',linestyle="--",linewidth=1,label='Strategy')
plt.legend(handles=[performance_line,strategy_line],loc=3,ncol=2)
plt.show()


# this code block generates my third figure: cost of latency for T=0.04
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
t=4
ax.plot(range(len(latencys)),maxperformance[t], color='black', linewidth=3, label='Best Performance')
ax.set_xticks(range(len(latencys)))
ax.set_xticklabels(latencys)
ax.set_ylim([40,110])
ax.set_xlim([-0.5,len(latencys)-.5])
ax.set_ylabel("Performance")
ax.set_xlabel("Latency in Feedback (turns)")
ax.set_title("Attainable Performance at Turbulence=0.04\nwith Various Levels of Latency")
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=2,label='Performance')
plt.legend(handles=[performance_line],loc=3)
plt.show()

# this code block generates my fourth figure: cost of latency for T=0.04 with optimal strategy
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
t=4
ax.plot(range(len(latencys)),maxperformance[t], color='black', linewidth=3, label='Best Performance')
ax.set_xticks(range(len(latencys)))
ax.set_xticklabels(latencys)
ax.set_ylim([40,110])
ax.set_xlim([-0.5,len(latencys)-.5])
ax.set_ylabel("Performance")
ax.set_xlabel("Latency in Feedback (turns)")
ax.set_title("Attainable Performance and Strategy at\nTurbulence=0.04 with Various Levels of Latency")
ax2=ax.twinx()
ax2.plot(range(len(latencys)),optimumstrategy[t],"k--")
ax2.set_xlim([-0.5,len(latencys)-.5])
ax2.set_ylim([0,1])
ax2.set_ylabel("Strategy (tau)")
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=2,label='Performance')
strategy_line = mlines.Line2D([],[],color='black',linestyle="--",linewidth=1,label='Strategy')
plt.legend(handles=[performance_line,strategy_line],loc=3,ncol=2)
plt.show()




#transform all performance values relative to latency zero
maxpft = [maxperformance[i]-maxperformance[i][0] for i in range(len(maxperformance))]


# this code block generates my fifth figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for t in range(len(turbs)):
    lw = 3 if t == 0 else 1
    ax.plot(range(len(latencys)),maxperformance[t], color='black', linewidth=lw, label='Best Performance')
    plt.text(len(latencys)-0.5,maxperformance[t][-1],"T="+str(turbs[t]))
ax.set_xticks(range(len(latencys)))
ax.set_xticklabels(latencys)
#ax.set_ylim([-60,10])
ax.set_xlim([-0.5,len(latencys)+1.5])
ax.set_ylabel("Performance")
ax.set_xlabel("Latency in Feedback (turns)")
ax.set_title("Attainable Performance with Various\nLevels of Latency and Turbulence")
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=3,label='Performance at T=0')
plt.legend(handles=[performance_line],loc=3)
plt.show()

# this code block generates my sixth figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for t in range(len(turbs)):
    lw = 3 if t == 0 else 1
    ax.plot(range(len(latencys)),maxpft[t], color='black', linewidth=lw, label='Best Performance')
    plt.text(len(latencys)-0.5,maxpft[t][-1],"T="+str(turbs[t]))
ax.set_xticks(range(len(latencys)))
ax.set_xticklabels(latencys)
ax.set_ylim([-60,10])
ax.set_xlim([-0.5,len(latencys)+1.5])
ax.set_ylabel("Performance (relative to L=0)")
ax.set_xlabel("Latency in Feedback (turns)")
ax.set_title("Attainable Performance (Relative to Latency=0)\nwith Various Levels of Latency and Turbulence")
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=3,label='Performance at T=0')
plt.legend(handles=[performance_line],loc=3)
plt.show()


# this code block generates my seventh figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for t in range(len(turbs)):
    lw = 3 if t == 0 else 1
    ax.plot(range(len(latencys)),optimumstrategy[t], color='black', linewidth=lw, label='Best Performance')
    plt.text(len(latencys)-0.5,optimumstrategy[t][-1],"T="+str(turbs[t]))
ax.set_xticks(range(len(latencys)))
ax.set_xticklabels(latencys)
ax.set_ylim([-0.1,1.1])
ax.set_xlim([-0.5,len(latencys)+1.5])
ax.set_ylabel("Optimal Strategy")
ax.set_xlabel("Latency in Feedback (turns)")
ax.set_title("Optimal Strategy with Various\nLevels of Latency and Turbulence")
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=3,label='Strategy at T=0')
plt.legend(handles=[performance_line],loc=3)
plt.show()


#transform all performance values relative to latency zero
relativestrategy = [optimumstrategy[i]-optimumstrategy[i][0] for i in range(len(optimumstrategy))]

# this code block generates my eighth figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for t in range(len(turbs)):
    lw = 3 if t == 0 else 1
    ax.plot(range(len(latencys)),relativestrategy[t], color='black', linewidth=lw, label='Best Performance')
    plt.text(len(latencys)-0.5,relativestrategy[t][-1],"T="+str(turbs[t]))
ax.set_xticks(range(len(latencys)))
ax.set_xticklabels(latencys)
ax.set_ylim([-0.7,0.7])
ax.set_xlim([-0.5,len(latencys)+1.5])
ax.set_ylabel("Optimal Strategy (relative to L=0)")
ax.set_xlabel("Latency in Feedback (turns)")
ax.set_title("Optimal Strategy (Relative to Latency=0)\nwith Various Levels of Latency and Turbulence")
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=3,label='Strategy at T=0')
plt.legend(handles=[performance_line],loc=3)
plt.show()


#ninth figure: "cost of latency" (perf. at latency=16 - perf. at latency=0) at several levels of turbulence
#the data
cost_of_latency = []
for t in range(len(turbs)):
    cost_of_latency.append(maxperformance[t][0]-maxperformance[t][-1])
#the figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(range(len(turbs)),cost_of_latency, color='black', linewidth=3, label='Cost of Latency')
ax.set_xlim([-0.5,len(turbs)-0.5])
ax.set_xticks(range(len(turbs)))
ax.set_xticklabels(turbs)
ax.set_ylabel("Cost of Latency\n(performance at L=0 - performance at L=16)")
ax.set_xlabel("Turbulence")
ax.set_title("Cost of Latency (or Value of Real-Time Feedback)\nat Different Levels of Turbulence")
# now the legend
cost_line = mlines.Line2D([],[],color='black',linewidth=3,label='Cost of Latency')
plt.legend(handles=[cost_line],loc=4)
plt.show()

# conclusions: performance seems to decrease with latency when there is
# turbulence, but more so as turbulence increases.  however, there is somewhat
# of a reversal at even higher turbulence.  maybe there's a middle level
# of turbulence where latency is more harmful
# (or at high levels of turbulence, nothing matters anymore, therefore medium 
# levels of turbulence are where real-time can genuinely help the learner)

# next step: let's try limiting the memory.  hypothesis: fast feedback and 
# short memory (aka knowledge renewal capacity; the ability to discard old
# knowledge that is no longer relevant) work together in highly turbulent 
# environments, but neither works as well without the other.


# tweak: optimal strategy may drop in high-latency cases because they
# have the benefit of beginning to learn with up to 16 turns of random 
# arm-payoff data. pure exploitation strategies are feasible (if not optimal)
# but are not for learners with no latency. this should be corrected if we
# want to talk about optimal strategy.
