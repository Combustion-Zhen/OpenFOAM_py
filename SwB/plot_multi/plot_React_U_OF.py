"""
Zhen Lu 2017/01/23

Compare the results of non-reacting flow from FLUENT and OpenFOAM

FLUENT: Smagorinski
OpenFOAM: Smagorinski, different boundary conditions

figures have two column, one for the mean velocity, the other for the rms
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

z_loc = [42,45,50,55,60,65,70,80,90]

cas_pre = 'SwBd_L-400_20M_FLAMELET_'

OF_cas = ['Bulk_SFCD','Bulk']
OF_label = ['SFCD','linear']

line_style = ['-','--','-.',':','-']
line_color = ['tab:red','tab:green','tab:blue','tab:orange','tab:purple']
line_width = 1.5

# import experiment data
data = np.genfromtxt('Exp/div_15/PIV_138_4_set1.dat',delimiter=',')

x = list(set(data[:,0]))
z = list(set(data[:,1]))
z.sort(reverse=True)

z = np.flipud(z)

ur1 = np.flipud(np.reshape(data[:,3],(len(z),len(x))))
uz1 = np.flipud(np.reshape(data[:,4],(len(z),len(x))))
ut1 = np.flipud(np.reshape(data[:,5],(len(z),len(x))))

# import experiment data
data = np.genfromtxt('Exp/div_15/PIV_138_8_set1.dat',delimiter=',')

ur2 = np.flipud(np.reshape(data[:,3],(len(z),len(x))))
uz2 = np.flipud(np.reshape(data[:,4],(len(z),len(x))))
ut2 = np.flipud(np.reshape(data[:,5],(len(z),len(x))))

u1 = np.empty(len(x))
u2 = np.empty(len(x))

# figure settings
plot_width      =19.0
margin_left     =1.5
margin_right    =0.3
margin_bottom   =1.2
margin_top      =0.3
space_width     =1.0
space_height    =1.0
ftsize          =11

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = 3
num_rows = 3

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
figz, axz = plt.subplots(num_rows, num_cols,
        sharex=True, sharey = True,
        figsize=cm2inch(plot_width,plot_height))

figr, axr = plt.subplots(num_rows, num_cols,
        sharex=True, sharey = True,
        figsize=cm2inch(plot_width,plot_height))

figt, axt = plt.subplots(num_rows, num_cols,
        sharex=True, sharey = True,
        figsize=cm2inch(plot_width,plot_height))

for i in range(num_rows):
    for j in range(num_cols):
        k = num_cols*i+j

        # import OF data
        OF_file = 'z{:d}.csv'.format(z_loc[k])
        for l, case in enumerate(OF_cas):
            OF_folder = ''.join([cas_pre,case,'/sample_lines'])
            file_name = '/'.join([OF_folder,OF_file])

            OF_data = np.genfromtxt(file_name,delimiter=',',names=True)
            OF_data = OF_data[np.isfinite(OF_data['p'])]

            axz[i,j].plot(OF_data['Points0']*1000,OF_data['UMean2'],
                    label=OF_label[l],
                    lw=line_width,
                    ls=line_style[l],
                    c=line_color[l])

            axr[i,j].plot(OF_data['Points0']*1000,OF_data['UMean0'],
                    label=OF_label[l],
                    lw=line_width,
                    ls=line_style[l],
                    c=line_color[l])

            axt[i,j].plot(OF_data['Points0']*1000,OF_data['UMean1'],
                    label=OF_label[l],
                    lw=line_width,
                    ls=line_style[l],
                    c=line_color[l])

        # plot experiment
        # axial
        for m in range(len(x)):
            u1[m] = np.interp(z_loc[k],z,uz1[:,m])
            u2[m] = np.interp(z_loc[k],z,uz2[:,m])

        axz[i,j].plot(x,u1,'k.',label='Exp 4')
        axz[i,j].plot(x,u2,'b.',label='Exp 8')

        # radial
        for m in range(len(x)):
            u1[m] = np.interp(z_loc[k],z,ur1[:,m])
            u2[m] = np.interp(z_loc[k],z,ur2[:,m])

        axr[i,j].plot(x,u1,'k.',label='Exp 4')
        axr[i,j].plot(x,u2,'b.',label='Exp 8')

        # tangential
        for m in range(len(x)):
            u1[m] = np.interp(z_loc[k],z,ut1[:,m])
            u2[m] = np.interp(z_loc[k],z,ut2[:,m])

        axt[i,j].plot(x,-u1,'k.',label='Exp 4')
        axt[i,j].plot(x,-u2,'b.',label='Exp 8')

        axz[i,j].text(5,5,'z={:g} mm'.format(z_loc[k]))
        axr[i,j].text(5,5,'z={:g} mm'.format(z_loc[k]))
        axt[i,j].text(5,5,'z={:g} mm'.format(z_loc[k]))

################################################################################

for i in range(num_rows):
    axz[i,0].set_ylabel(r'$u_z\;\mathrm{m/s}$')
    axr[i,0].set_ylabel(r'$u_x\;\mathrm{m/s}$')
    axt[i,0].set_ylabel(r'$u_y\;\mathrm{m/s}$')

for i in range(num_cols):
    axz[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')
    axr[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')
    axt[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')

axz[0,0].set_xlim(0,50)
axt[0,0].set_xlim(0,50)
axr[0,0].set_xlim(0,50)

axz[0,0].legend(
        ncol=2,frameon=False)
axr[0,0].legend(
        ncol=2,frameon=False)
axt[0,0].legend(
        ncol=2,frameon=False)

figz.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/plot_width,
        hspace = space_height/plot_height
        )

figr.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/plot_width,
        hspace = space_height/plot_height
        )

figt.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/plot_width,
        hspace = space_height/plot_height
        )

figz.savefig('velz_react_z{:d}.png'.format(z_loc[0]))
figr.savefig('velr_react_z{:d}.png'.format(z_loc[0]))
figt.savefig('velt_react_z{:d}.png'.format(z_loc[0]))
