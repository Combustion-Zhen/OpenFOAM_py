"""
Zhen Lu, 10/May/2017 <albert.lz07@gmail.com>
plot Sandia Flame results
"""
import glob
import numpy as np
import file_read as fr
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

U_REF = 49.6

# import data
xd_val = []
simu = {}
expr = {}
for file_name in glob.glob('mean_U_xD*.csv'):
    xd = file_name[9:-4]
    z = fr.z_str_to_num(xd)
    if z <= 5.0:
        xd_val.append(z)

        data = np.genfromtxt(file_name,delimiter=',')
        simu.update({z:np.stack((data[:,0],
                                 data[:,3],
                                 data[:,-1]),
                                axis=1)})
        simu[z][:,2] = np.sqrt(simu[z][:,2])

        if z == 0.0:
            data = np.array([[0.0,62.95,6.13],
                             [0.0694,62.54,6.23],
                             [0.1388,61.36,8.27],
                             [0.2083,59.21,12.45],
                             [0.2777,56.73,15.93],
                             [0.3472,53.34,20.66],
                             [0.4166,48.80,24.50],
                             [0.4861,41.99,37.40],
                             [0.5,0.0,0.0],
                             [0.5555,3.45,0.322],
                             [0.6250,11.46,1.736],
                             [0.6944,15.18,1.484],
                             [0.7638,15.45,1.586],
                             [0.8333,15.15,1.797],
                             [0.9027,15.97,1.36],
                             [0.9722,15.56,1.476],
                             [1.0416,15.42,1.410],
                             [1.1111,15.04,1.546],
                             [1.1805,14.25,1.875],
                             [1.2300,10.96,1.508],
                             [1.2400,0.0,0.0],
                             [1.3194,1.04,0.009],
                             [1.3888,1.01,0.007],
                             [1.4583,1.07,0.007],
                             [2.1041,1.02,0.006]])
        else:
            exp_str = 'TUD_LDV_'
            exp_name = '../../../{0}DEF/{0}D.d{1}'.format(exp_str,xd)
            data = np.genfromtxt(exp_name,skip_header=13)

        expr.update({z:data[:,:3]})
        expr[z][:,2] = np.sqrt(expr[z][:,2])
xd_val.sort()

## plot
# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
# total width is fixed
plot_width      =19.0
subplot_h       =4.0
margin_left     =2.0
margin_right    =0.3
margin_bottom   =1.5
margin_top      =1.0
space_width     =0.0
space_height    =1.0
ftsize          =12
# total height determined by the number of vars
plot_height     =((subplot_h+space_height)*2.0
                  -space_height+margin_top+margin_bottom)
# min and max of axis
xmin = 0.0
xmax = 2.0
xtick= tuple(np.arange(xmin,xmax,0.5))

# generate the figure
fig, axes = plt.subplots(2,len(xd_val),
                         sharex='col',sharey='row',
                         figsize=fr.cm2inch(plot_width, plot_height))
# plot
for i,z in enumerate(xd_val):
    axes[0,i].plot(simu[z][:,0],simu[z][:,1],'-b',
                   label='Sim.',linewidth=1.5)
    axes[0,i].plot(expr[z][:,0],expr[z][:,1],'ok',
                   label='Exp.',linewidth=1.5)
    axes[1,i].plot(simu[z][:,0],simu[z][:,2],'-b',
                   label='Sim.',linewidth=1.5)
    axes[1,i].plot(expr[z][:,0],expr[z][:,2],'ok',
                   label='Exp.',linewidth=1.5)

    #title
    axes[0,i].set_title('$x/D={0:.2g}$'.format(z),
                        fontsize=ftsize)
    #r/x
    axes[-1,i].set_xlabel('$r/D$',
                          fontsize=ftsize)
    axes[-1,i].set_xlim(xmin,xmax)
    axes[-1,i].set_xticks(xtick)

axes[-1,-1].set_xticks(xtick+(xmax,))

# ylabel
axes[0,0].set_ylabel(r'$\langle\tilde u\rangle\;(\mathrm{m/s})$',
                     fontsize=ftsize)
axes[1,0].set_ylabel((r'$\langle\tilde u^{\prime\prime 2}\rangle^{1/2}$'
                      r'$\;(\mathrm{m/s})$'),
                     fontsize=ftsize)

# legend
axes[0,-1].legend(fontsize=ftsize,
                  numpoints=1,
                  frameon=False)

# set margins
plt.subplots_adjust(left    =margin_left/plot_width,
                    bottom  =margin_bottom/plot_height,
                    right   =1.0-margin_right/plot_width,
                    top     =1.0-margin_top/plot_height,
                    wspace  =space_width/plot_width,
                    hspace  =space_height/plot_height)

# save plot
plt.savefig('radial_ave_U_up.png',dpi=400)
plt.savefig('radial_ave_U_up.pdf')
plt.savefig('radial_ave_U_up.eps')
