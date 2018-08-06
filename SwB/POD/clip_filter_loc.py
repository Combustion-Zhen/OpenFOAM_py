
# coding: utf-8

# In[1]:


# clip and save data in certain region


# In[1]:


import numpy as np


# In[2]:


file_prefix = 'clip_POD0'
file_suffix = 'csv'
file_number = 10


# In[3]:


file_name = 'clip_POD_ave0.csv'
data = np.genfromtxt(file_name, names=True, delimiter=',')

z = data['Points2']
r = np.sqrt( np.square( data['Points0'] ) + np.square( data['Points1'] ) )


# In[4]:


region = np.any( np.array([ z >= 0.04, r <= (13.6+14.4*z/0.04)/1000. ]), axis = 0 )


# In[5]:


data_len = sum(region)


# In[6]:


data_ave = np.empty([data_len, 3])


# In[7]:


for j in range(3):
    data_ave[:,j] = data['U_average{:d}'.format(j)][region]


# In[8]:


np.savetxt('POD_ave.csv',
           data_ave,
           fmt='%12.5e',
           delimiter=','
          )


# In[10]:


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

