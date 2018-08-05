
# coding: utf-8

# In[1]:


# clip and save data in certain region


# In[2]:


import numpy as np


# In[3]:


file_prefix = 'clip_POD0'
file_suffix = 'csv'


# In[4]:


file_name = '.'.join([file_prefix,'0',file_suffix])

data = np.genfromtxt(file_name, names=True, delimiter=',')

z = data['Points2']
r = np.sqrt( np.square( data['Points0'] ) + np.square( data['Points1'] ) )


# In[5]:


names = ','.join(data.dtype.names[:-3])


# In[6]:


region = np.any( np.array([ z >= 0.04, r <= (13.6+14.4*z/0.04)/1000. ]), axis = 0 )


# In[7]:


file_name = 'clip_POD_ave0.csv'
data_clip = np.genfromtxt(file_name, skip_header=1, delimiter=',')
data_ave = data_clip[region,:]
np.savetxt('POD_ave.csv',
           data_ave,
           fmt='%10.5f',
           delimiter=',',
           header=','.join(data.dtype.names),
           comments=''
          )


# In[8]:


for i in range(2):
    file_name = '.'.join([file_prefix,'{:d}'.format(i),file_suffix])
    data_clip = np.genfromtxt(file_name, skip_header=1, delimiter=',')
    data = data_clip[region,:-3] - data_ave[:,:-3]
    np.savetxt('.'.join(['POD_series','{:d}'.format(i),file_suffix]),
               data,
               fmt='%10.5f',
               delimiter=',',
               header=names,
               comments=''
              )

