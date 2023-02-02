import matplotlib.pyplot as plt

import numpy as np

# Data for plotting

#================== Plotting convergence of the graphs ================================================



alpha = 0.9999
beta = 0.5
GT= 0.9


#GT
y_range0 = [0.9, 0.9, 0.9, 0.9,0.9]
#lone researcher (unbiased, precise)
y_range1 = [0.75, 0.8333333333333334, 0.8983050847457628, 0.8993288590604027, 0.8946015424164524]

x_range = [5,10,20,50,100]
# 2 researchers (unbiased, precise)
y_range2 = [0.8571428571428571, 0.8999999999999999, 0.8994082840236686, 0.8997613365155132,  0.899909008189263]

# lone researcher, biased but precise
y_range3 = [0.5,0.8, 0.8888888888888888, 0.8992805755395683, 0.8997134670487106]

#lone researcher, unbiased but unprecise (alpha = 0.9)
y_range4 = [0.75, 0.8333333333333334, 0.84, 0.6133333333333333, 0.4775943474025188]
#lone researcher, unbiased but unprecise (alpha = 0.95)
y_range5 = [0.5,0.75,0.8333333333333334, 0.8873494969487052, 0.7979685293355728]

fig, ax = plt.subplots()
ax.plot(x_range, y_range0)
ax.plot(x_range, y_range1, label = "1 agent. alpha = 0.99999, beta = 0.5")
ax.plot(x_range, y_range2, label = "2 agents. alpha = 0.99999, beta = 0.5")
ax.plot(x_range, y_range3, label = "1 agent. alpha = 0.99999, beta = 0.75")
#ax.plot(x_range, y_range4, label = "1 agent. alpha = 0.9, beta = 0.5")
#ax.plot(x_range, y_range5, label = "1 agent. alpha = 0.95, beta = 0.5")

ax.set(xlabel='Number of iterations', ylabel='Value of the PSG')
ax.grid()

#fig.savefig("test.png")
plt.legend()
plt.show()