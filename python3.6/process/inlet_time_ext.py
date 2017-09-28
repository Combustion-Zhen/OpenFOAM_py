"""
Zhen Lu 2017/09/28
Extension of time for the timeVaryingMappedFixedValue BCs
"""
import os
import glob
import numpy as np

# get the folder list
time_list = []
for folder_name in glob.glob('[0-9]*'):
    time_list.append(float(folder_name))

time_list.sort()
time = np.array(time_list)

tdiff = time[-1]+time[1]-2*time[0]

for folder in time[:-1]:
    os.rename('{:g}'.format(folder),'{:g}'.format(folder+tdiff))
