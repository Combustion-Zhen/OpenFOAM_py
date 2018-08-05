"""
Zhen Lu 2018/07/12
plot the mean mixture fraction at different z, along x axis
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

locs = np.arange(5,60,15)

# plot
# figure and axes parameters
# total width is fixed
plot_width      =9.0
margin_left     =1.35
margin_right    =0.15
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
subplot_height = subplot_width * 0.18

plot_height = (nrows*subplot_height
              +margin_bottom
              +margin_top
              +(nrows-1)*space_height)

fig, ax = plt.subplots( nrows, ncols, sharex = True, sharey = True,
                        figsize = cm2inch( plot_width, plot_height ) )

for i, loc in enumerate(locs):
    # number for subplot
    j = nrows - 1 - i

    # import simulation data
    file_name = 'sample_lines/z{:d}.csv'.format(loc)
    data = np.genfromtxt(file_name,delimiter=',',names=True)

    x_sim = data['Points0']*1000
    z_sim = data['chiMean_average']

    ax[j].plot(x_sim,z_sim,'r-')

    ax[j].text(-39,0.77,'{:d} mm'.format(loc))

    ax[j].set_ylabel(r'$\langle\tilde{Z}\rangle$')

ax[-1].set_xlabel(r'$r\;(\mathrm{mm})$')

#ax[0].legend(loc=(0.4,0.6),ncol=2,frameon=False)

ax[0].set_xlim(-40,40)
ax[0].set_xticks(np.linspace(-40,40,num=9))
#ax[0].set_ylim(0,1)
#ax[0].set_yticks(np.linspace(0,1,num=3))

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/subplot_width,
        hspace = space_height/subplot_height
        )

#fig.savefig('fig_radial_Z.eps')
#fig.savefig('fig_radial_Z.pdf')
plt.show()
