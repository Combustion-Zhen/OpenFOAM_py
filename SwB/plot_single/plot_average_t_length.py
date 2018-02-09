"""
Zhen Lu 2018/02/09

plot sample lines from the swirl burner
check the minimum average time for the swirl burner
"""

import numpy as np
import glob
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)

# up limit of the average time, 0.1 s
t_ul = 10

# get the time list
t_list = []

line_style=[':','--','-.',':','-.','--',':','-.',':','-']

for folder in glob.glob('[0-9]*'):
    time = float(folder)
    t_list.append(time)

t_list.sort()

z_loc = [42,45,50,55,60,65,70,80,90]

# plot
# figure and axes parameters
# total width is fixed
plot_width      =19.0
margin_left     =1.5
margin_right    =0.3
margin_bottom   =1.2
margin_top      =0.3
space_width     =1.0
space_height    =1.0
ftsize          =12

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

ncols = 3
nrows = 3

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(ncols-1)*space_width)/ncols
subplot_height = subplot_width * 0.8

plot_height = (nrows*subplot_height
              +margin_bottom
              +margin_top
              +(nrows-1)*space_height)

# total height determined by the number of vars
figz, axz = plt.subplots(nrows, ncols,
        sharex=True, sharey = True,
        figsize=cm2inch(plot_width,plot_height))

figr, axr = plt.subplots(nrows, ncols,
        sharex=True, sharey = True,
        figsize=cm2inch(plot_width,plot_height))

figt, axt = plt.subplots(nrows, ncols,
        sharex=True, sharey = True,
        figsize=cm2inch(plot_width,plot_height))

for i in range(nrows):
    for j in range(ncols):
        k = ncols*i+j
        
        for l in range(t_ul):
            time = t_list[-1-l]
            folder = 'sample_t{:g}'.format(time)

            # import simulation data
            file_name = '{0}/z{1:d}.csv'.format(folder,z_loc[k])
            data = np.genfromtxt(file_name,delimiter=',',names=True)

            x_sim = data['Points0']*1000
#            uz_sim = data['UPrime2Mean2']
#            ur_sim = data['UPrime2Mean0']
#            ut_sim = data['UPrime2Mean1']
            uz_sim = data['ZPrime2Mean']
            ur_sim = data['O2Prime2Mean']
            ut_sim = data['COPrime2Mean']

            if l != 0:
#                uz_sim = (data['UPrime2Mean2']+l*uz_old)/(l+1)
#                ur_sim = (data['UPrime2Mean0']+l*ur_old)/(l+1)
#                ut_sim = (data['UPrime2Mean1']+l*ut_old)/(l+1)
                uz_sim = (data['ZPrime2Mean']+l*uz_old)/(l+1)
                ur_sim = (data['O2Prime2Mean']+l*ur_old)/(l+1)
                ut_sim = (data['COPrime2Mean']+l*ut_old)/(l+1)

            uz_old = uz_sim
            ur_old = ur_sim
            ut_old = ut_sim

            # axial
            axz[i,j].plot(x_sim,uz_sim,ls=line_style[l],label='{:d}'.format(l))

            # radial
            axr[i,j].plot(x_sim,ur_sim,ls=line_style[l],label='{:d}'.format(l))

            # tangential
            axt[i,j].plot(x_sim,ut_sim,ls=line_style[l],label='{:d}'.format(l))

            axz[i,j].text(5,5,'z={:g} mm'.format(z_loc[k]))
            axr[i,j].text(5,5,'z={:g} mm'.format(z_loc[k]))
            axt[i,j].text(5,5,'z={:g} mm'.format(z_loc[k]))

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

for i in range(nrows):
    axz[i,0].set_ylabel(r'$u_z\;\mathrm{m/s}$')
    axr[i,0].set_ylabel(r'$u_x\;\mathrm{m/s}$')
    axt[i,0].set_ylabel(r'$u_y\;\mathrm{m/s}$')

for i in range(ncols):
    axz[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')
    axr[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')
    axt[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')

axz[0,0].set_xlim(0,50)
axt[0,0].set_xlim(0,50)
axr[0,0].set_xlim(0,50)

figz.savefig('uz.pdf')
figr.savefig('ur.pdf')
figt.savefig('ut.pdf')
