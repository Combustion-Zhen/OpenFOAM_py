"""
Zhen Lu, 30/04/2017 <albert.lz07@gmail.com>
plot mean and rms of velocity of a pipe flow, for the inlet of Flame D
"""
import glob
import numpy as np
import file_read as fr
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# import data
xd_val = []
simu = {}
for file_name in glob.glob('mean_U_xD*.csv'):
    xd = file_name[9:-4]
    z = fr.z_str_to_num(xd)
    xd_val.append(z)

    data = np.genfromtxt(file_name,delimiter=',')
    simu.update({z:np.stack((data[:,0],data[:,1],data[:,4]),axis=1)})
    #simu.update({z:np.stack((data[:,0],data[:,3],data[:,-1]),axis=1)})

    simu[z][:,2] = np.sqrt(simu[z][:,2])
    #simu[z][:,1:] /= U_REF
xd_val.sort()

# Experiment data
expr = np.array([[0.0,62.95,6.13],
                 [0.0694,62.54,6.23],
                 [0.1388,61.36,8.27],
                 [0.2083,59.21,12.45],
                 [0.2777,56.73,15.93],
                 [0.3472,53.34,20.66],
                 [0.4166,48.80,24.50],
                 [0.4861,41.99,37.40],
                 [0.5,0.0,0.0]])
expr[:,2] = np.sqrt(expr[:,2])

## plot
# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
# total width is fixed
plot_width      =19.0
margin_left     =1.5
margin_right    =0.3
margin_bottom   =1.2
margin_top      =0.2
space_width     =4.0
space_height    =1.0
ftsize          =12
# total height determined by the number of vars
plot_height = ((plot_width-margin_left-margin_right-space_width)/2.0
               * 0.8 + margin_bottom + margin_top)

# generate the figure
fig, axes = plt.subplots(1,2,
                         figsize=fr.cm2inch(plot_width, plot_height))

for z in xd_val:
    axes[0].plot(simu[z][:,0],simu[z][:,1],
                 label=r"$\mathrm{{Sim.}}\quad x/D={:.2g}$".format(z),
                 linewidth=1.5)
    axes[1].plot(simu[z][:,0],simu[z][:,2],
                 label=r"$\mathrm{{Sim.}}\quad x/D={:.2g}$".format(z),
                 linewidth=1.5)

axes[0].plot(expr[:,0],expr[:,1],'ok',
             label='Exp.',linewidth=1.5)
axes[1].plot(expr[:,0],expr[:,2],'ok',
             label='Exp.',linewidth=1.5)

# xlabel
axes[0].set_xlabel('$r/D$',fontsize=ftsize)
axes[1].set_xlabel('$r/D$',fontsize=ftsize)
#ylabel
axes[0].set_ylabel(r'$\langle\tilde u\rangle\;\mathrm{(m/s)}$',
                   fontsize=ftsize)
axes[1].set_ylabel((r'$\langle\tilde u^{\prime\prime 2}\rangle^{1/2}$'
                    '$\;\mathrm{(m/s)}$'),
                   fontsize=ftsize)
# legend
axes[0].legend(loc='lower left',
               fontsize=ftsize,
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
plt.savefig('radial_ave_U.png',dpi=400)
plt.savefig('radial_ave_U.pdf')
plt.savefig('radial_ave_U.eps')
