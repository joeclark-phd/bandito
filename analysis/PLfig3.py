# -*- coding: utf-8 -*-
"""
This file replicates figure 3 from Posen & Levinthal (2012) using my simulation output.
"""

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# read the summary data
df = pd.read_csv("PLfig3-summary.csv")

# attempts at plots
#plt.plot(df.MEAN_SCORE)
#plt.plot(df.STRATEGY,df.MEAN_SCORE)

turbs = df.TURBULENCE.unique()
strategies = df.STRATEGY.unique()
# data structures to eventually plot
opts = np.empty_like(turbs) # optimum strategies
secondds = np.empty_like(turbs) # second derivatives

for t in turbs:
    #print(t)
    #print(df.MEAN_SCORE[df.TURBULENCE==t])
    # fit the 3rd order polynomial
    poly = np.poly1d(np.polyfit(strategies,df.MEAN_SCORE[df.TURBULENCE==t],3))
    # find the roots of the derivative
    optima = poly.deriv().r
    # maxima are optima where 2nd derivative is negative 
    optimumstrategy = optima[poly.deriv().deriv()(optima)<0][0]
    maxperformance = poly(optimumstrategy)
    secondderiv = poly.deriv().deriv()(optimumstrategy)
    #print("The optimum strategy is tau = "+str(optimumstrategy))
    #print("The predicted performance is: "+str(maxperformance))
    #print("The 2nd derivative of performance at the optimum is: "+str(secondderiv))
    opts[np.argmax(turbs==t)]=optimumstrategy
    secondds[np.argmax(turbs==t)]=secondderiv


# Now, plot "opts" and "secondds" against turbulence. 
# Remember the x axis is not to scale.

# this code block replicates P+L(2012) figure 3
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(opts, color='black', linewidth=2, label='Optimal')
ax.set_ylim([0.3,0.7])
ax.set_xlim([-.5,7.5])
ax2=ax.twinx()
ax2.plot(secondds, color='black', linestyle="--", linewidth=2, label="2nd deriv. at optimal")
ax2.set_ylim([-350,0])
ax.set_xlim([-.5,7.5])
# labels
ax.set_title('P+L (2012) Figure 3. Optimal Exploration\nStrategy (tau) Across Turbulence Levels')
ax.set_xlabel('Turbulence')
ax.set_ylabel('Strategy (tau)')
ax2.set_ylabel('2nd derivative')
ax.set_xticks(np.arange(len(turbs)))
ax.set_xticklabels(turbs)
# now the legend
opts_line = mlines.Line2D([],[],color='black',linewidth=2,label='Optimal')
secondd_line = mlines.Line2D([],[],color='black',linewidth=2,linestyle='--',label='2nd deriv. at optimal')
plt.legend(handles=[opts_line,secondd_line],loc='best')
plt.show()
