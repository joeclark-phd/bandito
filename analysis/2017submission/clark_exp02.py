# -*- coding: utf-8 -*-
"""
This file will show how the length of memory (proxy for knowledge renewal
capacity) affects the cost of latency and overall performance at various
levels of latency and turbulence
"""

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# read the summary data
#df = pd.read_csv("clark02a-summary.csv") #02a is an earlier version with only 3 levels of turbulence and latency, before the initialization bias bug was fixed
df = pd.read_csv("clark02-summary.csv") #02b has more levels of turbulence 

# levels of latency and turbulence
latencys = df.LATENCY.unique()
turbs = df.TURBULENCE.unique()
mems = df.MEMORY.unique()


# to hold the calculated values at each experimental condition (latency x turbulence x memory)
optimumstrategy=np.empty((len(turbs),len(latencys),len(mems)))
meanperformance=np.empty((len(turbs),len(latencys),len(mems)))
maxperformance=np.empty((len(turbs),len(latencys),len(mems)))
secondderiv=np.empty((len(turbs),len(latencys),len(mems)))


# loop through all turbulence levels
for t in turbs:
    # loop through all latency levels
    for l in latencys:
        # loop through all memory levels
        for m in mems:
            subset = df[(df.TURBULENCE==t)&(df.LATENCY==l)&(df.MEMORY==m)]    
            # fit the 3rd order polynomial
            poly = np.poly1d(np.polyfit(subset.STRATEGY,subset.MEAN_SCORE,3))
            # find the roots of the derivative
            optima = poly.deriv().r
            # maxima are optima where 2nd derivative is negative; or could be at x= 0 or 1
            concave_maxima = optima[poly.deriv().deriv()(optima)<0] # this is it in almost every case
            other_possible_maxima = [0,1] # sometimes you get a weird polynomial, though. may be useful to print out optstrat just to see when that happens
            all_possible_maxima = np.concatenate([other_possible_maxima,concave_maxima]) if concave_maxima.any() else other_possible_maxima
            optstrat = all_possible_maxima[poly(all_possible_maxima).argmax()]
            #i got a warning when the optstrat was a complex number, 0j, but the program knows to treat it as a normal zero, so no bug
            #print("turb: "+str(t)+", latency: "+str(l)+", mem: "+str(m)+", optstrat: "+str(optstrat))
            optimumstrategy[np.argmax(turbs==t)][np.argmax(latencys==l)][np.argmax(mems==m)] = optstrat
            meanperformance[np.argmax(turbs==t)][np.argmax(latencys==l)][np.argmax(mems==m)] = np.mean(subset.MEAN_SCORE)
            maxperformance[np.argmax(turbs==t)][np.argmax(latencys==l)][np.argmax(mems==m)] = poly(optstrat)
            secondderiv[np.argmax(turbs==t)][np.argmax(latencys==l)][np.argmax(mems==m)] = poly.deriv().deriv()(optstrat)


# get data for optimal memory for each turbulence level, holding latency=0
optmemforturb = np.empty(len(turbs))
for t in range(len(turbs)):
    print(mems[maxperformance[t][0].argmax()])



# first let's plot the curve performance = f(memory), for each turbulence level
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for t in range(len(turbs)):
    lw = 3 if t == 0 else 1
    ax.plot(range(len(mems)),maxperformance[t][0], color='black', linewidth=lw, label='Best Performance')
    plt.text(len(mems)-.8,maxperformance[t][0][-1],"T="+str(turbs[t]))
ax.set_xticks(range(len(mems)))
ax.set_xticklabels(mems)
ax.set_xlim([-0.5,len(mems)+1])
ax.set_ylim([0,350])
ax.set_ylabel("Performance")
ax.set_xlabel("Length of Memory (turns)")
ax.set_title("Attainable Performance as function of Memory\nat several levels of Turbulence")
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=3,label='Performance at T=0')
plt.legend(handles=[performance_line],loc=0)
plt.show()

#transform all performance values relative to memory 20
relativeperformance = [maxperformance[i]-maxperformance[i][0][0] for i in range(len(maxperformance))]

# now plot it again but normalized to memory=20
# first let's plot the curve performance = f(memory), for each turbulence level
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for t in range(len(turbs)):
    lw = 3 if t == 0 else 1
    ax.plot(range(len(mems)),relativeperformance[t][0], color='black', linewidth=lw, label='Best Performance')
    plt.text(len(mems)-.8,relativeperformance[t][0][-1],"T="+str(turbs[t]))
ax.set_xticks(range(len(mems)))
ax.set_xticklabels(mems)
ax.set_xlim([-0.5,len(mems)+1])
ax.set_ylim([-10,220])
ax.set_ylabel("Performance (relative to M=50)")
ax.set_xlabel("Length of Memory (turns)")
ax.set_title("Attainable Performance as function of Memory\nat several levels of Turbulence (values relative to M=50)")
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=3,label='Performance at T=0')
plt.legend(handles=[performance_line],loc=2)
plt.show()

    

# get data for optimal memory for each turbulence level, holding latency=0
optmemforturb = np.empty(len(turbs))
for t in range(len(turbs)):
    optmemforturb[t] = maxperformance[t][0].argmax()


# now we plot the optimal memory level for each turbulence level
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(range(len(turbs)),optmemforturb,color='black',linewidth=3,label="Best Memory Level")
ax.set_xticks(range(len(turbs)))
ax.set_xticklabels(turbs)
ax.set_xlim([-0.5,len(turbs)-0.5])
ax.set_yticks(range(len(mems)))
ax.set_yticklabels(mems)
ax.set_ylim([-0.5,len(mems)-0.5])
ax.set_ylabel("Time Window of Memory (turns)")
ax.set_xlabel("Turbulence")
ax.set_title("Best Performing Time Window of Memory (M) at\n Each Level of Turbulence")
# now the legend
memory_line = mlines.Line2D([],[],color='black',linewidth=3,label='Memory (turns)')
plt.legend(handles=[memory_line],loc=0)
plt.show()




# now, show the "cost of latency" at a few different memory levels

#ninth figure: "cost of latency" (perf. at latency=16 - perf. at latency=0) at several levels of turbulence
#the data
cost_of_latency = np.empty((len(mems),len(turbs)))
for m in range(len(mems)):
    for t in range(len(turbs)):
        cost_of_latency[m][t] = maxperformance[t][0][m]-maxperformance[t][-1][m]
#the figure
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
for m in [0,3,4,5,9]:
    lw = 3 if m == len(mems)-1 else 1
    ax.plot(range(len(turbs)),cost_of_latency[m], color='black', linewidth=lw, label='Cost of Latency')
    #y = cost_of_latency[m][0]+2 if m==0 else cost_of_latency[m][0]-1.5 # jigger label for M=50 upward so it is readable
    plt.text(-1.1,cost_of_latency[m][0]-1.5,"M="+str(mems[m]))
ax.set_xlim([-1.5,len(turbs)-0.5])
ax.set_xticks(range(len(turbs)))
ax.set_xticklabels(turbs)
ax.set_ylim([-20,90])
ax.set_ylabel("Cost of Latency\n(performance at L=0 - performance at L=16)")
ax.set_xlabel("Turbulence")
ax.set_title("Cost of Latency (or Value of Real-Time Feedback)\nas function of Turbulence at selected Memory levels")
# now the legend
cost_line = mlines.Line2D([],[],color='black',linewidth=3,label='Cost of Latency, M=500')
plt.legend(handles=[cost_line],loc=4)
plt.show()





