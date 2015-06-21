import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
 
N = 5
ind = np.arange(N)
fig, ax = plt.subplots()
menMeans = (20, 35, 30, 35, 27)
menStd =   (2, 3, 4, 1, 2)
width = 0.35       # the width of the bars
rects1 = ax.bar(ind, menMeans, width, color='r', yerr=menStd)
 
plt.show()
