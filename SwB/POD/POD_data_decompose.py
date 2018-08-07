# select data for POD, do the decomposition of u = \bar{u} + u'

import numpy as np
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('N', type=int, help='the number of snapshots')
args = parser.parse_args()

file_number = args.N
file_prefix = 'clip_POD0'
file_suffix = 'csv'

var_names = ['U0', 'U1', 'U2']
names = ','.join(var_names)

# load the average data first
data_ave = np.genfromtxt('clip_ave.csv',names=True,delimiter=',')

data = np.empty((data_ave.size,len(var_names)))

#

for i in range(file_number):
    file_name = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data_ins = np.genfromtxt(file_name, names=True, delimiter=',')

    for j, var in enumerate(var_names):
        data[:,j] = data_ins[var] - data_ave[var]

    np.savetxt('.'.join(['POD_data','{:d}'.format(i),file_suffix]),
               data,
               fmt='%12.5e',
               delimiter=',',
               header=names,
               comments=''
              )
