"""
Zhen Lu 2018/04/30
plot the mean velocity at different z, with x = y =0
"""

import numpy as np
import glob
import matplotlib as mpl
#mpl.use('Agg')
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

# cases
case_names = {
        'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL2':'Sim 2',
        'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL4':'Sim 4',
        'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL6':'Sim 6',
        'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL8':'Sim 8',
        }
linestyle_sim = ['b--','r-.','g-','c:','k-.']

# u_x, u_z, u_y
var_names = ['u_z','u_t']
var_index_sim = [2, 1]

# import experiment data
data = np.genfromtxt('./Exp/div_15/PIV_138_8_set1.dat',delimiter=',')

x = list(set(data[:,0]))
z = list(set(data[:,1]))
z.sort(reverse=True)

z = np.flipud(z)

data_exp = {}
for i, var in enumerate(var_names):
    u = np.flipud(np.reshape(data[:,i+4],(len(z),len(x))))
    uvar = np.empty(len(z))
    for j in range(len(z)):
        uvar[j] = np.interp(0,x,u[j,:])
    data_exp[var] = uvar

# plot
# figure and axes parameters
# total width is fixed
plot_width      =19.0
margin_left     =1.5
margin_right    =0.3
margin_bottom   =1.2
margin_top      =0.3
space_width     =3.5
space_height    =1.0
ftsize          =12

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = len(var_names)
num_rows = 1

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.9

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

# total height determined by the number of vars
fig, ax = plt.subplots(
        num_rows, num_cols,
        sharex=True,
        figsize=cm2inch(plot_width,plot_height))

# import simulation data
for j, k in enumerate(case_names.keys()):
    file_name = '{0}/sample_lines/axial.csv'.format(k)
    data = np.genfromtxt(file_name,delimiter=',',names=True)
    z_sim = data['Points2']*1000

    for i, var in enumerate(var_names):
        data_sim = data['UMean{:d}'.format(var_index_sim[i])]

        ax[i].plot(z_sim,data_sim,linestyle_sim[j],label=case_names[k])

for i, var in enumerate(var_names):
    ax[i].plot(z,data_exp[var],'k.',label='Exp')

ax[0].set_xlabel(r'$x\;\mathrm{mm}$')
ax[1].set_xlabel(r'$x\;\mathrm{mm}$')
ax[0].set_ylabel(r'$\langle u_z\rangle\;\mathrm{m/s}$')
ax[1].set_ylabel(r'$\langle u_t\rangle\;\mathrm{m/s}$')

ax[0].legend(frameon=False)

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/plot_width,
        hspace = space_height/plot_height
        )

fig.savefig('uzaxial.png')

