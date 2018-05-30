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
data = np.genfromtxt('./Exp/div_15/PIV_138_8_set1.dat',delimiter=',')

x = list(set(data[:,0]))
z = list(set(data[:,1]))
z.sort(reverse=True)

z = np.flipud(z)

ur = np.flipud(np.reshape(data[:,3],(len(z),len(x))))
uz = np.flipud(np.reshape(data[:,4],(len(z),len(x))))
ut = np.flipud(np.reshape(data[:,5],(len(z),len(x))))

u = np.empty(len(x))

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
        case_name = 'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL8'

        file_name = '{0}/sample_lines/z{1:d}.csv'.format(case_name,z_loc[k])
        data = np.genfromtxt(file_name,delimiter=',',names=True)

        x_sim = data['Points0']*1000
        uz_sim = data['UMean2']
        ur_sim = data['UMean0']
        ut_sim = data['UMean1']

        case_name = 'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL6'

        file_name = '{0}/sample_lines/z{1:d}.csv'.format(case_name,z_loc[k])
        data = np.genfromtxt(file_name,delimiter=',',names=True)

        x_sim2 = data['Points0']*1000
        uz_sim2 = data['UMean2']
        ur_sim2 = data['UMean0']
        ut_sim2 = data['UMean1']

        case_name = 'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL4'

        file_name = '{0}/sample_lines/z{1:d}.csv'.format(case_name,z_loc[k])
        data = np.genfromtxt(file_name,delimiter=',',names=True)

        x_sim3 = data['Points0']*1000
        uz_sim3 = data['UMean2']
        ur_sim3 = data['UMean0']
        ut_sim3 = data['UMean1']

        case_name = 'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL2'

        file_name = '{0}/sample_lines/z{1:d}.csv'.format(case_name,z_loc[k])
        data = np.genfromtxt(file_name,delimiter=',',names=True)

        x_sim4 = data['Points0']*1000
        uz_sim4 = data['UMean2']
        ur_sim4 = data['UMean0']
        ut_sim4 = data['UMean1']

        # axial
        for m in range(len(x)):
            u[m] = np.interp(z_loc[k],z,uz[:,m])

        axz[i,j].plot(x,u,'k.',label='Exp 8')
        axz[i,j].plot(x_sim,uz_sim,'b-.',label='Sim 8')
        axz[i,j].plot(x_sim2,uz_sim2,'r--',label='Sim 6')
        axz[i,j].plot(x_sim3,uz_sim3,'g-',label='Sim 4')
        axz[i,j].plot(x_sim4,uz_sim4,'m-',label='Sim 2')

        # radial
        for m in range(len(x)):
            u[m] = np.interp(z_loc[k],z,ur[:,m])

        axr[i,j].plot(x,u,'k.',label='Exp 8')
        axr[i,j].plot(x_sim,ur_sim,'b-.',label='Sim 8')
        axr[i,j].plot(x_sim2,ur_sim2,'r--',label='Sim 6')
        axr[i,j].plot(x_sim3,ur_sim3,'g-',label='Sim 4')
        axr[i,j].plot(x_sim4,ur_sim4,'m-',label='Sim 2')

        # tangential
        for m in range(len(x)):
            u[m] = np.interp(z_loc[k],z,ut[:,m])

        axt[i,j].plot(x,-u,'k.',label='Exp 8')
        axt[i,j].plot(x_sim,ut_sim,'b-.',label='Sim 8')
        axt[i,j].plot(x_sim2,ut_sim2,'r--',label='Sim 6')
        axt[i,j].plot(x_sim3,ut_sim3,'g-',label='Sim 4')
        axt[i,j].plot(x_sim4,ut_sim4,'m-',label='Sim 2')

        axz[i,j].text(5,10,'z={:g} mm'.format(z_loc[k]))
        axr[i,j].text(5,3,'z={:g} mm'.format(z_loc[k]))
        axt[i,j].text(5,8,'z={:g} mm'.format(z_loc[k]))

axz[0,0].legend(
        ncol=1,frameon=False)
axr[0,0].legend(
        ncol=1,frameon=False)
axt[0,0].legend(
        ncol=1,frameon=False)

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
    axz[i,0].set_ylabel(r'$\langle u_z\rangle\;\mathrm{m/s}$')
    axr[i,0].set_ylabel(r'$\langle u_r\rangle\;\mathrm{m/s}$')
    axt[i,0].set_ylabel(r'$\langle u_t\rangle\;\mathrm{m/s}$')

for i in range(num_cols):
    axz[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')
    axr[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')
    axt[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')

axz[0,0].set_xlim(0,50)
axt[0,0].set_xlim(0,50)
axr[0,0].set_xlim(0,50)

axz[0,0].set_ylim(-5,20)
axt[0,0].set_ylim(-1,11)
axr[0,0].set_ylim(-5,5)

figz.savefig('uz.png')
figr.savefig('ur.png')
figt.savefig('ut.png')
