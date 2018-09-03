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

# get data size and coordinate information
file_name = '.'.join([file_prefix,'0',file_suffix])
data_raw = np.genfromtxt(file_name, names=True, delimiter=',')

z = data_raw['Points2']
r = np.sqrt( np.square( data_raw['Points0'] ) + np.square( data_raw['Points1'] ) )

region = np.any( np.array([ z >= 0.04, z < 0., r <= (13.6+14.4*z/0.04)/1000. ]), axis = 0 )

data_len = sum(region)

data_ave = np.zeros((data_len,len(var_names)))

# save the coordinate
data = np.empty((data_len,3))
for j in range(3):
    data[:,j] = data_raw['Points{:d}'.format(j)][region]
np.savetxt('clip_xyz.csv',
           data,
           fmt='%12.6e',
           delimiter=',',
           header=','.join([ 'Points{:d}'.format(j) for j in range(3) ]),
           comments=''
          )

# save each snapshot
data = np.empty((data_len,len(var_names)))
for i in range(file_number):
    file_name = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data_raw = np.genfromtxt(file_name, names=True, delimiter=',')
    
    for j, var in enumerate(var_names):
        data[:,j] = data_raw[var][region]

    np.savetxt('.'.join([file_prefix,'{:d}'.format(i),file_suffix]),
               data,
               fmt='%12.6e',
               delimiter=',',
               header = names,
               comments = ''
              )

    # sum
    data_ave += data

# save average
data_ave /= float( file_number )
np.savetxt('clip_ave.csv',
           data_ave,
           fmt='%12.6e',
           delimiter=',',
           header = names,
           comments = ''
          )
           
    
