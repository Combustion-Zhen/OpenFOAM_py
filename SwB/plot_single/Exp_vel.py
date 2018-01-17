"""
Zhen Lu 2018/01/09

Read and organize averaged velocity PIV data
"""

import numpy as np

data = np.genfromtxt('PIV_138_4_set1.dat',delimiter=',')

x = list(set(data[:,0]))
z = list(set(data[:,1]))
z.sort(reverse=True)

ur = np.reshape(data[:,3],(len(z),len(x)))
uz = np.reshape(data[:,4],(len(z),len(x)))
ut = np.reshape(data[:,5],(len(z),len(x)))

