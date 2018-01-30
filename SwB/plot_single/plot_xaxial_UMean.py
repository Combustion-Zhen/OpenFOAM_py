"""
Zhen Lu 2018/01/10
plot the mean velocity at different z, along x axis
42 45 50 55 60 65 70 80 90
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

z_loc = [42,45,50,55,60,65,70,80,90]

# import experiment data
data = np.genfromtxt('../Exp/div_15/PIV_138_4_set1.dat',delimiter=',')

x = list(set(data[:,0]))
z = list(set(data[:,1]))
z.sort(reverse=True)

z = np.flipud(z)

ur1 = np.flipud(np.reshape(data[:,3],(len(z),len(x))))
uz1 = np.flipud(np.reshape(data[:,4],(len(z),len(x))))
ut1 = np.flipud(np.reshape(data[:,5],(len(z),len(x))))

# import experiment data
data = np.genfromtxt('../Exp/div_15/PIV_138_8_set1.dat',delimiter=',')

ur2 = np.flipud(np.reshape(data[:,3],(len(z),len(x))))
uz2 = np.flipud(np.reshape(data[:,4],(len(z),len(x))))
ut2 = np.flipud(np.reshape(data[:,5],(len(z),len(x))))

u1 = np.empty(len(x))
u2 = np.empty(len(x))

#uz_exp[i,1] = np.interp(0,x,uz[i,:])

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
        
        # import simulation data
        file_name = 'sample_lines/z{:d}.csv'.format(z_loc[k])
        data = np.genfromtxt(file_name,delimiter=',',names=True)

        x_sim = data['Points0']*1000
        uz_sim = data['UMean2']
        ur_sim = data['UMean0']
        ut_sim = data['UMean1']

        # axial
        for m in range(len(x)):
            u1[m] = np.interp(z_loc[k],z,uz1[:,m])
            u2[m] = np.interp(z_loc[k],z,uz2[:,m])

        axz[i,j].plot(x,u1,'k.',label='Exp 4')
        axz[i,j].plot(x,u2,'b.',label='Exp 8')
        axz[i,j].plot(x_sim,uz_sim,'r-',label='Sim')

        # radial
        for m in range(len(x)):
            u1[m] = np.interp(z_loc[k],z,ur1[:,m])
            u2[m] = np.interp(z_loc[k],z,ur2[:,m])

        axr[i,j].plot(x,u1,'k.',label='Exp 4')
        axr[i,j].plot(x,u2,'b.',label='Exp 8')
        axr[i,j].plot(x_sim,ur_sim,'r-',label='Sim')

        # tangential
        for m in range(len(x)):
            u1[m] = np.interp(z_loc[k],z,ut1[:,m])
            u2[m] = np.interp(z_loc[k],z,ut2[:,m])

        axt[i,j].plot(x,-u1,'k.',label='Exp 4')
        axt[i,j].plot(x,-u2,'b.',label='Exp 8')
        axt[i,j].plot(x_sim,ut_sim,'r-',label='Sim')

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

figz.savefig('uz.png')
figr.savefig('ur.png')
figt.savefig('ut.png')
