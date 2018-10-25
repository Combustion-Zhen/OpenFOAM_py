"""
Zhen Lu 2018/07/23
plot the mean velocity at different z, with x = y =0
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

# cases
flowrate = np.array([4,8,10,12,16,20])

D = 0.0044

casename = 'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL'
linecolor = ['tab:blue', 'tab:red', 'tab:green', 'tab:orange', 'm', 'k']
linestyle = ['--','-.',':','--','-.','-']
linewidth = [1.8, 1.8, 1.8, 1, 1, 1]

varnames = np.array([['UMean_average2','UPrime2Mean_average2'],
                    ['ZMean_average','ZPrime2Mean_average']])

varlimits = np.array([[(-0.5, 2),(0,0.9)],
                      [(0,1),(0,0.3)]])

varticks = np.array([[np.linspace(-0.5,2,num=6),
                      np.linspace(0,0.9,num=7)],
                     [np.linspace(0,1,num=6),
                      np.linspace(0,0.3,num=7)]])

# plot
# figure and axes parameters
# total width is fixed

# manuscript
plot_width      =19.0
margin_left     =1.8
margin_right    =0.3
margin_bottom   =1.2
margin_top      =0.3
space_width     =2.1
space_height    =0.5
ftsize          =11

## slides
#plot_width      =24.0
#margin_left     =2.8
#margin_right    =0.3
#margin_bottom   =1.8
#margin_top      =0.3
#space_width     =3.2
#space_height    =0.8
#ftsize          =20

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
plt.rc('text.latex', preamble=[r'\usepackage{amsmath}',r'\usepackage{bm}'])
# use serif font
plt.rc('font',**font)

nrows, ncols = varnames.shape

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(ncols-1)*space_width)/ncols
subplot_height = subplot_width * 0.7

plot_height = (nrows*subplot_height
              +margin_bottom
              +margin_top
              +(nrows-1)*space_height)

# total height determined by the number of vars
fig, ax = plt.subplots(
        nrows, ncols,
        sharex=True,
        figsize=cm2inch(plot_width,plot_height))

for l, k in enumerate(flowrate):
    # calculate the bulk flow velocity
    v = k * 28. / ( 22. * np.square(D) * 60000. )

    filename = '{0}{1:g}/sample_lines/axial.csv'.format(casename,k)
    data = np.genfromtxt(filename, delimiter=',', names=True)
    z_sim = data['Points2']*1000

    for i in range(nrows):
        for j in range(ncols):

            data_sim = data[varnames[i,j]]
            if j == 1 :
                data_sim[data_sim<0.] = 0.
                data_sim = np.sqrt(data[varnames[i,j]])

            if i == 0 :
                data_sim /= v

            ax[i,j].plot(z_sim, data_sim, 
                         ls=linestyle[l],
                         lw=linewidth[l], c=linecolor[l],
                         label='{:g} SLPM'.format(k))

            ax[i,j].set_ylim(varlimits[i,j])
            ax[i,j].set_yticks(varticks[i,j])

ax[0,0].set_xlim(0,120)
ax[0,0].legend(handlelength=3,frameon=False,loc=1)

ax[0,0].set_ylabel(r'$\langle\widetilde{u}_z\rangle/U_{\mathrm{ref}}$')
ax[0,1].set_ylabel(r'$\sqrt{\langle\widetilde{u_z^{\prime\prime 2}}\rangle}/U_{\mathrm{ref}}$')
ax[1,0].set_ylabel(r'$\langle\widetilde{Z}\rangle$')
ax[1,1].set_ylabel(r'$\sqrt{\langle\widetilde{Z^{\prime\prime 2}}\rangle}$')

ax[1,0].set_xlabel(r'$z\;(\mathrm{mm})$')
ax[1,1].set_xlabel(r'$z\;(\mathrm{mm})$')

#ax[0,0].plot([0,120],[0,0],'c-')

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/subplot_width,
        hspace = space_height/subplot_height
        )

fig.align_labels()

fig.savefig('fig_axial.eps')
fig.savefig('fig_axial.png')
