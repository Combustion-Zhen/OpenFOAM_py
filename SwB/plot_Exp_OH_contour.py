import math
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as colors

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)

#file_name = 'Exp/div_15/average_OH_8.dat'
# instantaneous profile
file_name = 'Exp/div_15/OH_Inclined_set1_120.dat'

data = np.genfromtxt(file_name,skip_header=3,delimiter=',')

x = list(set(data[:,0]))
z = list(set(data[:,1]))

x.sort()

#xc = 0.7
#x= [ xi - xc for xi in x ]

z.sort(reverse=True)
z = np.flipud(z)

#zc = 2
#z = [ zi - zc for zi in z ]

oh = np.flipud(np.reshape(data[:,2],(len(z),len(x))))

x_min = -40
x_max = 40
z_min = 0
z_max = 100

plot_width      =19.0
margin_left     =1.5
margin_right    =0.3
margin_bottom   =1.2
margin_top      =0.3
space_width     =1.0
space_height    =1.0
ftsize          =12

subplot_width = plot_width - margin_left - margin_right
subplot_height = subplot_width/(x_max-x_min)*(z_max-z_min)

plot_height = subplot_height + margin_bottom + margin_top

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

fig = plt.figure(figsize=cm2inch(plot_width,plot_height))

ax = fig.add_axes([
    margin_left/plot_width,
    margin_bottom/plot_height,
    subplot_width/plot_width,
    subplot_height/plot_height],
    aspect='equal')

ax.contourf(
        x,z,oh,50,
        norm=colors.LogNorm(vmin=0.000000001,vmax=oh.max()),
        cmap='inferno')

# plot wall

# 15 degree
plt.plot([-13.6,-24.3],[0,40],c='g',label='15')
plt.plot([13.6,24.3],[0,40],c='g')

"""
plt.plot([-25.9,-24.3],[40,40],c='g')
plt.plot([24.3,25.9],[40,40],c='g')

plt.plot([-15.2,-25.9],[0,40],c='g')
plt.plot([15.2,25.9],[0,40],c='g')
"""

# out contour
plt.plot([-13.6,-30],[0,40],c='r',label='22')
plt.plot([13.6,30],[0,40],c='r')

# spare
plt.plot([-13.6,-27.3],[0,41.3],c='b',label='18')
plt.plot([13.6,27.3],[0,41.3],c='b')

"""
plt.plot([-29.6,-27.3],[41.3,41.3],c='b')
plt.plot([27.3,29.6],[41.3,41.3],c='b')

plt.plot([-15.9,-29.6],[0,41.3],c='b')
plt.plot([15.9,29.6],[0,41.3],c='b')
"""

quarl_deg = 16
quarl_length = 42
quarl_radius = 13.6+math.tan(quarl_deg)*quarl_length

plt.plot(
        [-13.6,-quarl_radius],[0,quarl_length],
        c='k',label='{:g}'.format(quarl_deg))
plt.plot(
        [13.6,quarl_radius],[0,quarl_length],
        c='k')
plt.legend()

ax.set_xlim(x_min,x_max)
ax.set_ylim(z_min,z_max)

plt.show()
