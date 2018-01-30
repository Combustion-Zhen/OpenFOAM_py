"""
Zhen Lu 2018/01/29
plot the mean velocity along central line

read 
"""

import numpy as np
import glob
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

def value_convert(x):
    try:
        return int(x)
    except ValueError:
        try:
            return float(x)
        except ValueError:
            return x

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)

# import simulation data
data_sim = np.genfromtxt('sample_lines/axial.csv',delimiter=',',names=True)

# import experiment data
data = np.genfromtxt('../Exp/div_15/PIV_138_4_set1.dat',delimiter=',')

x = list(set(data[:,0]))
z = list(set(data[:,1]))
z.sort(reverse=True)

uz = np.reshape(data[:,4],(len(z),len(x)))

uz_exp = np.zeros((len(z),2))
uz_exp[:,0] = z

for i in range(len(z)):
    uz_exp[i,1] = np.interp(0,x,uz[i,:])

# import experiment data
data = np.genfromtxt('../Exp/div_15/PIV_138_8_set1.dat',delimiter=',')

x = list(set(data[:,0]))
z = list(set(data[:,1]))
z.sort(reverse=True)

uz = np.reshape(data[:,4],(len(z),len(x)))

uz_exp2 = np.zeros((len(z),2))
uz_exp2[:,0] = z

for i in range(len(z)):
    uz_exp2[i,1] = np.interp(0,x,uz[i,:])

# plot
# figure and axes parameters
# total width is fixed
plot_width      =9.0
margin_left     =1.2
margin_right    =0.3
margin_bottom   =1.2
margin_top      =0.3
space_width     =4.5
space_height    =1.5
ftsize          =12

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = 1
num_rows = 1

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.8

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

# total height determined by the number of vars
fig, ax = plt.subplots(figsize=cm2inch(plot_width,plot_height))

ax.plot(data_sim['Points2']*1000,data_sim['UMean2'],'r-',label='Sim',lw=1)
ax.plot(uz_exp[:,0],uz_exp[:,1],'b.',label='Exp 4')
ax.plot(uz_exp2[:,0],uz_exp2[:,1],'k.',label='Exp 8')

ax.set_xlim(0,125)
ax.set_ylim(-4,16)

ax.set_xlabel(r'$z\;\mathrm{mm}$')
ax.set_ylabel(r'$u_z\;\mathrm{m/s}$')

ax.legend()

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/plot_width,
        hspace = space_height/plot_height
        )

#plt.show()
fig.savefig('uz_zaxis.pdf')
