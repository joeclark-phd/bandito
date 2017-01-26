# -*- coding: utf-8 -*-
"""
This file replicates figure 1 from Posen & Levinthal (2012) using my simulation output.
It also calculates the optimum strategy, predicts performance at that strategy, and 
calculates the 2nd derivative at that strategy.  These will be used to replicate fig.3.
"""

import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import matplotlib.pyplot as plt
import matplotlib.lines as mlines

# read the summary data
df = pd.read_csv("PLfig1-summary.csv")

# attempts at plots
#plt.plot(df.MEAN_SCORE)
#plt.plot(df.STRATEGY,df.MEAN_SCORE)



# fit the 3rd order polynomial
poly = np.poly1d(np.polyfit(df.STRATEGY,df.MEAN_SCORE,3))
# find the roots of the derivative
optima = poly.deriv().r
# maxima are optima where 2nd derivative is negative 
optimumstrategy = optima[poly.deriv().deriv()(optima)<0][0]
maxperformance = poly(optimumstrategy)
secondderiv = poly.deriv().deriv()(optimumstrategy)



# this code block replicates P+L(2012) figure 1
fig = plt.figure()
ax = fig.add_subplot(1,1,1)
ax.plot(df.STRATEGY, df.MEAN_SCORE, color='black',linewidth=2,label='Performance')
#these next three lines add the fitted 3rd degree polynomial as a red line with a dot at the optimum
#xp = np.linspace(0,1)
#ax.plot(xp,poly(xp),'r')
#ax.plot(optimumstrategy,maxperformance,'ro')
ax.set_title('P+L (2012) Figure 1. Choice, Performance, and\nKnowledge Across Strategies in Stable Environment')
ax.set_xlabel('Strategy (tau)')
ax.set_ylabel('Performance')
# now the plots that use the right y-axis
ax2=ax.twinx()
ax2.plot(df.STRATEGY, df.MEAN_PROBEXPLORE, linewidth=2, linestyle='--', color='black',label='Choice (prob. exploring)')
ax2.plot(df.STRATEGY, df.MEAN_KNOWLEDGE, linestyle=':', color='black',label='Knowledge')
ax2.set_ylabel('Fraction')
# put this last because it was disappearing when done earlier
ax.set_xticks([0,0.25,0.5,0.75,1])
# now the legend
performance_line = mlines.Line2D([],[],color='black',linewidth=2,label='Performance')
choice_line = mlines.Line2D([],[],color='black',linewidth=2,linestyle='--',label='Choice (prob. exploring)')
knowledge_line = mlines.Line2D([],[],color='black',linestyle=':',label='Knowledge')
#these commented-out lines squash the chart a bit to make the legend seem to fit better
#box = ax.get_position()
#ax.set_position([box.x0, box.y0, box.width, box.height*0.8])
#ax2.set_position([box.x0, box.y0, box.width, box.height*0.8])
plt.legend(handles=[performance_line,choice_line,knowledge_line],loc=8,ncol=3,bbox_to_anchor=(0.5,-0.3),fontsize='medium')
plt.show()


print("The optimum strategy is tau = "+str(optimumstrategy))
print("The predicted performance is: "+str(maxperformance))
print("The 2nd derivative of performance at the optimum is: "+str(secondderiv))

