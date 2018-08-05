"""
Zhen Lu 2018/07/16

plot scattering with the conditional average of T versus Z
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

# pick the latest time automatically
calc_time=[]
for filename in glob.glob('postProcessing/surfaces/*'):
    calc_time.append(float(filename[24:]))
time=str(max(calc_time))

locs = np.arange(5,60,15)

# plot
# figure and axes parameters
# total width is fixed
plot_width      =9.0
margin_left     =1.5
margin_right    =0.2
margin_bottom   =1.0
margin_top      =0.1
space_width     =.5
space_height    =.3
ftsize          =9

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
plt.rc('text.latex', preamble=[r'\usepackage{amsmath}',r'\usepackage{bm}'])
# use serif font
plt.rc('font',**font)
# make the axis the lowest layer
plt.rc('axes', axisbelow = True )

ncols = 1
nrows = locs.size

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(ncols-1)*space_width)/ncols
subplot_height = subplot_width * 0.4

plot_height = (nrows*subplot_height
              +margin_bottom
              +margin_top
              +(nrows-1)*space_height)

fig, ax = plt.subplots( nrows, ncols, sharex = True, sharey = True,
                        figsize = cm2inch( plot_width, plot_height ) )

for i, loc in enumerate(locs):
    # number for subplot
    j = nrows - 1 - i

    # scatter
    filename = 'postProcessing/surfaces/{0}/scat_z{1}.csv'.format(time,loc)
    data = np.genfromtxt(filename,delimiter=',',names=True)

    ax[j].scatter( data['Z'], data['T'], s=4, c='k', marker='.' )

    # conditional average
    filename = 'postProcessing/cond_z{}.csv'.format(loc)
    data = np.genfromtxt(filename,delimiter=',',names=True)

    ax[j].plot( data['Z'], data['T'], 'r-', lw=1 )

    ax[j].text(0.8,2000,'{:d} mm'.format(loc))

    ax[j].set_ylabel(r'$\tilde{T}\;(\mathrm{K})$')

ax[-1].set_xlabel(r'$\tilde{Z}$')

ax[0].set_xlim(0,1)
ax[0].set_xticks(np.linspace(0,1,num=6))
ax[0].set_ylim(298,2300)
ax[0].set_yticks(np.linspace(500,2000,num=4))

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/subplot_width,
        hspace = space_height/subplot_height
        )

fig.savefig('fig_scat_cond_ZT.eps')
fig.savefig('fig_scat_cond_ZT.pdf')
 
