
# coding: utf-8

# In[1]:


# proper orthogonal decomposition with the snapshot implementation
# Sirovich, 1987 and Taira et al., 2017


# In[16]:


import numpy as np
from scipy import linalg


# In[35]:


file_prefix = 'POD_data'
file_suffix = 'csv'
file_number = 10
mode_number = 7


# In[4]:


matrix_cov = np.empty((file_number, file_number))


# In[14]:


for i in range(file_number):
    file_name = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data_i = np.genfromtxt(file_name, delimiter=',')
    
    matrix_cov[i,i] = np.sum( np.square(data_i) )
    
    for j in range(i+1,file_number):
        file_name = '.'.join([file_prefix,'{:d}'.format(j),file_suffix])
        data_j = np.genfromtxt(file_name, delimiter=',')
        
        matrix_cov[i,j] = np.sum( np.multiply( data_i, data_j ) )
        matrix_cov[j,i] = matrix_cov[i,j]


# In[26]:


e, v = linalg.eig(matrix_cov)


# In[28]:


eig = np.real(e)


# In[30]:


sigma = np.sqrt(eig)


# In[47]:


data_shape = data_j.shape
data_size = data_j.size


# In[52]:


modes = np.zeros([data_size, mode_number])


# In[53]:


for i in range(file_number):
    file_name = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data = np.genfromtxt(file_name, delimiter=',').flatten()
    
    for j in range(mode_number):
        modes[:,j] += data*v[i,j]
        
for j in range(mode_number):
    modes[:,j] /= sigma[j]


# In[60]:


# save the modes
for j in range(mode_number):
    file_name = '.'.join(['POD_mode','{:d}'.format(j),file_suffix])
    np.savetxt(file_name,
               modes[:,j].reshape(data_shape),
               fmt='%12.5e',
               delimiter=','
              )


# In[74]:


# coefficients, eigenvalues, sigma, and the Vij of the first X modes
data = np.concatenate((eig.reshape((-1,1)), sigma.reshape((-1,1)), v[:,:mode_number]),axis=1)


# In[80]:


var_names = [ 'V{:d}'.format(i) for i in range(mode_number) ]
var_names.insert(0, 'sigma')
var_names.insert(0, 'eigval')


# In[81]:


np.savetxt('POD_coef.csv',
           data,
           fmt = '%12.5e',
           delimiter = ',',
           header = ','.join(var_names),
           comments = ''
          )

