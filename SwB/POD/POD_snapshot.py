# proper orthogonal decomposition with the snapshot implementation
# Sirovich, 1987 and Taira et al., 2017

import numpy as np
from scipy import linalg
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('N', type=int, help='the number of snapshots')
parser.add_argument('M', type=int, help='the number of modes to be presented')
args = parser.parse_args()

file_number = args.N
mode_number = args.M

file_prefix = 'POD_data'
file_suffix = 'csv'

matrix_cov = np.empty((file_number, file_number))

for i in range(file_number):
    file_name = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data_i = np.genfromtxt(file_name, delimiter=',')
    
    matrix_cov[i,i] = np.sum( np.square(data_i) )
    
    for j in range(i+1,file_number):
        file_name = '.'.join([file_prefix,'{:d}'.format(j),file_suffix])
        data_j = np.genfromtxt(file_name, delimiter=',')
        
        matrix_cov[i,j] = np.sum( np.multiply( data_i, data_j ) )
        matrix_cov[j,i] = matrix_cov[i,j]

e, v = linalg.eig(matrix_cov)

eig = np.real(e)

sigma = np.sqrt(eig)

data_shape = data_j.shape
data_size = data_j.size

modes = np.zeros([data_size, mode_number])

for i in range(file_number):
    file_name = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data = np.genfromtxt(file_name, delimiter=',').flatten()
    
    for j in range(mode_number):
        modes[:,j] += data*v[i,j]
        
for j in range(mode_number):
    modes[:,j] /= sigma[j]

# save the modes
for j in range(mode_number):
    file_name = '.'.join(['POD_mode','{:d}'.format(j),file_suffix])
    np.savetxt(file_name,
               modes[:,j].reshape(data_shape),
               fmt='%12.5e',
               delimiter=','
              )

# coefficients, eigenvalues, sigma, and the Vij of the first X modes
data = np.concatenate((eig.reshape((-1,1)), sigma.reshape((-1,1)), v[:,:mode_number]),axis=1)

var_names = [ 'V{:d}'.format(i) for i in range(mode_number) ]
var_names.insert(0, 'sigma')
var_names.insert(0, 'eigval')

np.savetxt('POD_coef.csv',
           data,
           fmt = '%12.5e',
           delimiter = ',',
           header = ','.join(var_names),
           comments = ''
          )

