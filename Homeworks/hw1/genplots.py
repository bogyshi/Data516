import numpy as np
mins1= np.array([0.511,0.366,0.442,0.406,0.452])
maxs1 = np.array([0.650,0.555,0.759,0.604,0.507])
means1 = np.array([0.561,0.462,0.5705,0.4685,0.483])
arnum = len(maxs1)
plt.errorbar(np.arange(arnum), means1, [means1 - mins1, maxs1 - means1],fmt='.k', ecolor='gray', lw=1)
plt.xlabel('query number')
plt.ylabel('time (s)')
plt.title('min,max, and avg time per query (1)')

plt.savefig('/home/bdvr/DATA516/avanroi1/Homeworks/hw1/q1graph.jpg')
mins4= np.array([0.393,1.725])
maxs4 = np.array([0.509,2.60])
means4 = np.array([0.4475,2.294])
arnum = len(maxs1)
plt.errorbar(np.arange(arnum), means1, [means1 - mins1, maxs1 - means1],fmt='.k', ecolor='gray', lw=1)
plt.xlabel('standard (0) vs python udf (1)')
plt.ylabel('time (s)')
plt.title('min,max, and avg time per query type (4)')
plt.savefig('/home/bdvr/DATA516/avanroi1/Homeworks/hw1/q4graph.jpg')


mins2= np.array([1.70,0.412,0.937,0.439,2.936])
maxs2 = np.array([1.892,0.488,1.717,0.505,3.826])
means2 = np.array([1.77,0.446,1.465,0.467,3.37])
arnum = len(maxs1)
plt.errorbar(np.arange(arnum), means2, [means2 - mins2, maxs2 - means2],fmt='.k', ecolor='gray', lw=1)
plt.xlabel('query number')
plt.ylabel('time (s)')
plt.title('min,max, and avg time per query (2)')
plt.savefig('/home/bdvr/DATA516/avanroi1/Homeworks/hw1/q2graph.jpg')

mins3= np.array([0.832,0.374,1.417,0.386,1.997])
maxs3 = np.array([1.732,0.433,1.861,0.586,3.40])
means3 = np.array([1.3655,0.394,1.714,0.466,2.7505])
arnum = len(maxs1)
plt.errorbar(np.arange(arnum), means3, [means3 - mins3, maxs3 - means3],fmt='.k', ecolor='gray', lw=1)
plt.xlabel('query number')
plt.ylabel('time (s)')
plt.title('min,max, and avg time per query (3)')
plt.savefig('/home/bdvr/DATA516/avanroi1/Homeworks/hw1/q3graph.jpg')


mins5= np.array([7.760,1.256,7.455,3.781,18.529])
maxs5 = np.array([9.453,1.621,7.868,4.62,19.479])
means5 = np.array([8.54,1.41,7.64,4.19,18.78])
arnum = len(maxs5)
plt.errorbar(np.arange(arnum), means5, [means5 - mins5, maxs5 - means5],fmt='.k', ecolor='gray', lw=1)
plt.xlabel('query number')
plt.ylabel('time (s)')
plt.title('min,max, and avg time per query (5)')
plt.savefig('/home/bdvr/DATA516/avanroi1/Homeworks/hw1/q5graph.jpg')
