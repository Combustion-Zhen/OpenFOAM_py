# data from shaheen/paraview include meanless variables
# pick U, Z, p only

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('N', type=int, help='the number of snapshots')
args = parser.parse_args()

file_number = args.N
file_prefix = 'clip_POD0'
file_suffix = 'csv'

var_names = ['U0', 'U1', 'U2', 'p', 'Z']
names = ','.join(var_names)

for i in range(file_number):
    file_name = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data_raw = np.genfromtxt(file_name, names=True, delimiter=',')
    
    data = np.empty((data_raw.size,len(var_names)))
    for j, var in enumerate(var_names):
        data[:,j] = data_raw[var]
    
    np.savetxt('.'.join([file_prefix,'{:d}'.format(i),file_suffix]),
               data,
               fmt='%12.5e',
               delimiter=',',
               header = names,
               comments = ''
              )

