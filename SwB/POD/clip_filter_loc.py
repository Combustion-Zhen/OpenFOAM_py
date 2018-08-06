# clip and save data in certain region

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('N', type=int, help='the number of snapshots')
args = parser.parse_args()

file_number = args.N

file_prefix = 'clip_POD0'
file_suffix = 'csv'

file_name = 'clip_POD_ave0.csv'
data = np.genfromtxt(file_name, names=True, delimiter=',')

z = data['Points2']
r = np.sqrt( np.square( data['Points0'] ) + np.square( data['Points1'] ) )

region = np.any( np.array([ z >= 0.04, r <= (13.6+14.4*z/0.04)/1000. ]), axis = 0 )

data_len = sum(region)

data_ave = np.empty([data_len, 3])

for j in range(3):
    data_ave[:,j] = data['U_average{:d}'.format(j)][region]

np.savetxt('POD_ave.csv',
           data_ave,
           fmt='%12.5e',
           delimiter=','
          )

data = np.empty([data_len,3])
for i in range(file_number):
    file_name = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data_clip = np.genfromtxt(file_name, names=True, delimiter=',')
    for j in range(3):
        data[:,j] = data_clip['U{:d}'.format(j)][region]
    data -= data_ave
    np.savetxt('.'.join(['POD_data','{:d}'.format(i),file_suffix]),
               data,
               fmt='%12.5e',
               delimiter=','
              )
