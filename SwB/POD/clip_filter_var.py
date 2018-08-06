
# coding: utf-8

# In[ ]:


# data from shaheen/paraview include meanless variables
# pick U, Z, p only


# In[2]:


import numpy as np


# In[3]:


file_prefix = 'clip_POD0'
file_suffix = 'csv'
file_number = 10

var_names = ['U0', 'U1', 'U2', 'p', 'Z']
names = ','.join(var_names)


# In[4]:


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

