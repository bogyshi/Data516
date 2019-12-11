import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

font = {'family' : 'normal',
        'size'   : 18}

matplotlib.rc('font', **font)

eightNodePerf = np.array([177741.5,348590.0146018982, 255813])
eightNodeStds = np.array([1,41448,1])
twoNodePerf = np.array([206196,216386,367735])
twoNodeStds = np.array([1,1,1])

numIters = np.array([1,2,4])

arnum = len(eightNodePerf)
plt.figure(figsize=(12,8))
plt.errorbar(np.arange(3), eightNodePerf, [eightNodeStds,eightNodeStds],fmt='.k', lw=1,ecolor='green',markeredgecolor='red',markersize='15',markerfacecolor ='red')
plt.errorbar(np.arange(3), twoNodePerf, [twoNodeStds,twoNodeStds],fmt='.k', ecolor='red', lw=1,markeredgecolor='green',markersize='15',markerfacecolor ='green')

plt.xlabel('Number of iterations')
plt.ylabel('Time in ms')
plt.title('avg cost for LR on spark with varying nodes and iterations')
custom_lines = [Line2D([0], [0], color='green', lw=4),
                Line2D([0], [0], color='red', lw=4)]
plt.legend(custom_lines, ['two nodes','eight nodes'],loc='upper left')
plt.xticks(np.arange(3),labels=numIters.astype(str))
#plt.show()
plt.savefig('sparkResults.jpg',quality = 95)
