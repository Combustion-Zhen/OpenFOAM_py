# Zhen Lu, 12/04/2017 <albert.lz07@gmail.com>
# plot Sandia Flame results, the 2D contour
from file_read import csv_read, cm2inch
# suppress the display of matplotlib.pyplot
#import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

# variable to be plot
var = 'T'
vmin = 100.0;
vmax = 2200.0;

xD_limit=25.0
rD_limit=5.0

# import data
field_mean=csv_read('mean_field.csv')
# convert from 1D to 2D array
r = sorted(list(set(field_mean['r'])))
z = sorted(list(set(field_mean['z'])))
v = [[0.0 for rD in r ] for zD in z ]
Z = [[0.0 for rD in r ] for zD in z ]
for i in range(len(field_mean[var])):
    v[z.index(field_mean['z'][i])][r.index(field_mean['r'][i])]=field_mean[var][i]
    Z[z.index(field_mean['z'][i])][r.index(field_mean['r'][i])]=field_mean['Z'][i]

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
subplot_width   =(plot_width-margin_left-margin_right-space_width)/3.0
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
ax0 = plt.axes([margin_left/plot_width,
                margin_bottom/plot_height,
                2.0*subplot_width/plot_width,
                subplot_height/plot_height],
                aspect='equal')
ax0.contourf(r,z,v,60,
             vmin=vmin,vmax=vmax)
ax0.contour(r,z,Z,[0.351,],
            linewidths=2.0)
# limits
ax0.set_xlim(0.0,2.0*rD_limit)
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
                 vmin=vmin,vmax=vmax)
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
cbar=plt.colorbar(cf1,cax=cax,ticks=[300,500,700,900,1100,1300,1500,1700,1900,2100])


# set margins
#plt.subplots_adjust(left    =margin_left/plot_width,
#                    bottom  =margin_bottom/plot_height,
#                    right   =1.0-margin_right/plot_width,
#                    top     =1.0-margin_top/plot_height,
#                    wspace  =space_width/plot_width,
#                    hspace  =space_height/plot_height)


plt.show()
