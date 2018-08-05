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

tdiff = -0.5

for folder in time:
    os.rename('{:g}'.format(folder),'{:g}'.format(folder+tdiff))
