"""
Zhen Lu, 12/04/2017 <albert.lz07@gmail.com>
plot Sandia Flame results, the 2D contour
"""
from file_read import cm2inch
import numpy as np
# suppress the display of matplotlib.pyplot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# variable to be plot
var = 'T'
vmin = 200.0
vmax = 2100.0
clmp = 'jet'

xD_limit=25.0
rD_limit=5.0

# import data average
field_mean=np.genfromtxt('mean_field.csv',
                         delimiter=',',
                         names=True)
# convert from 1D to 2D array
r = sorted(list(set(field_mean['r'])))
z = sorted(list(set(field_mean['z'])))
v = np.reshape(field_mean[var],(len(z),len(r)))
Z = np.reshape(field_mean['Z'],(len(z),len(r)))

# import data instantaneous
field_inst=np.genfromtxt('inst_field.csv',
                         delimiter=',',
                         names=True)
# convert from 1D to 2D array
ri= sorted(list(set(field_inst['r'])))
zi= sorted(list(set(field_inst['z'])))
vi= [[0.0 for rD in ri ] for zD in zi ]
Zi= [[0.0 for rD in ri ] for zD in zi ]
for i in range(len(field_inst[var])):
    vi[zi.index(field_inst['z'][i])] \
      [ri.index(field_inst['r'][i])]=field_inst[var][i]
    Zi[zi.index(field_inst['z'][i])] \
      [ri.index(field_inst['r'][i])]=field_inst['Z'][i]

# plot
# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
# total width is fixed, for one column plot
plot_width      =9.0
margin_left     =1.5
margin_right    =2.0
margin_bottom   =1.2
margin_top      =1.0
space_width     =0.3
space_height    =1.0
ftsize          =12
# parameters for subplots
subplot_width   =(plot_width
                  -margin_left
                  -margin_right
                  -space_width)/3.0
# equal aspect ratio for r, x
subplot_height  =subplot_width*xD_limit/rD_limit
plot_height     =subplot_height+margin_bottom+margin_top
# parameters for colorbar
clb_left        =0.4
clb_right       =1.2
clb_bottom      =3.0
clb_width       =margin_right-clb_left-clb_right
clb_height      =subplot_height-clb_bottom
# min and max of axis

fig = plt.figure(figsize=cm2inch(plot_width,plot_height))

# create the first axes for instantaneous plot
ax0 = fig.add_axes([margin_left/plot_width,
                    margin_bottom/plot_height,
                    2.0*subplot_width/plot_width,
                    subplot_height/plot_height],
                    aspect='equal')
ax0.contourf(ri,zi,vi,60,
             vmin=vmin,vmax=vmax,
             cmap=clmp)
ax0.contour(ri,zi,Zi,[0.351,],
            linewidths=2.0)
# limits
ax0.set_xlim(-rD_limit,rD_limit)
ax0.set_ylim(0.0,xD_limit)
# lables
ax0.set_xlabel('$r/D$',fontsize=ftsize)
ax0.set_ylabel('$x/D$',fontsize=ftsize)
# title
ax0.set_title(r'$\tilde {0}$'.format(var),fontsize=ftsize)

# second axes, harf in r for mean plot
ax1 = plt.axes([(margin_left+2.0*subplot_width+space_width)/plot_width,
                margin_bottom/plot_height,
                subplot_width/plot_width,
                subplot_height/plot_height],
                aspect='equal')
cf1=ax1.contourf(r,z,v,60,
                 vmin=vmin,vmax=vmax,
                 cmap=clmp)
ax1.contour(r,z,Z,[0.351,],
            linewidths=2.0)
# limits
ax1.set_xlim(0.0,rD_limit)
ax1.set_ylim(0.0,xD_limit)
# labels
ax1.set_yticks([])
ax1.set_xlabel('$r/D$',fontsize=ftsize)
# title
ax1.set_title(r'$\langle\tilde {0}\rangle$'.format(var),fontsize=ftsize)

# colorbar
# specify the location for the color bar
cax = plt.axes([(plot_width-margin_right+clb_left)/plot_width,
                (margin_bottom+clb_bottom)/plot_height,
                clb_width/plot_width,
                clb_height/plot_height])
cbar=plt.colorbar(cf1,cax=cax,ticks=np.arange(300,2200,200))

# save plot
plt.savefig('field.png',dpi=400)
plt.savefig('field.pdf')
plt.savefig('field.eps')
#plt.show()
