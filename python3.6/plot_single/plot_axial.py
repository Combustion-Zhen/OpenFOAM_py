"""
Zhen Lu, 27/April/2017, <albert.lz07@gmail.com>
plot axial distribution of velocity, mixture fraction, and temperature
"""
import numpy as np
import file_read as fr
import glob
import matplotlib as mpl
#mpl.use('Agg')
import matplotlib.pyplot as plt

print('Plot axial distributions')

D = 0.0072
U_REF = 49.6

# pick the latest time
calc_time=[]
for file_name in glob.glob('sets/*'):
    calc_time.append(float(file_name[5:]))
time=str(max(calc_time))

# import simulation data
# velocity mean
file_name = 'sets/{}/axis_UMean.xy'.format(time)
data_tmp = np.genfromtxt(file_name)
data = np.column_stack((data_tmp[:,0],data_tmp[:,-1]))
# velocity rms
file_name = 'sets/{}/axis_UPrime2Mean.xy'.format(time)
data_tmp = np.genfromtxt(file_name)
data = np.column_stack((data,data_tmp[:,-1]))

# Z and T
file_name = 'sets/{0}/axis_T{1}_T{2}_Z{1}_Z{2}.xy'.format(time,
                                                          'Mean',
                                                          'Prime2Mean')
data_tmp = np.genfromtxt(file_name)
data = np.hstack((data,data_tmp[:,1:]))

data[:,0] /= D

loc_rms = np.arange(2,data.shape[1],2)
data_tmp = np.maximum(data[:,loc_rms],0.0)
data[:,loc_rms] = np.sqrt(data_tmp)

data[:,1:3] /= U_REF

# experiment scalar
folder_exp = '../../../pmCDEFarchives/pmD.stat/D'
scalar_name = ['T', 'Z']
expr = {'z':[]}
for name in scalar_name:
    expr.update({name:[]})
    expr.update({name+'rms':[]})
for file_name in glob.glob('{}*.Yave'.format(folder_exp)):
    data_tmp = fr.sf_expr_read(file_name)
    if file_name[len(folder_exp):-5].isdigit():
        if 0.0 in data_tmp['r']:
            expr['z'].append(fr.z_str_to_num(file_name[len(folder_exp):-5]))
            i = np.where(data_tmp['r'] == 0.0)[0]
            """
            elif -0.04 in data_tmp['r']:
                i = np.where(data_tmp['r'] == -0.04)[0]
            """
            for name in scalar_name:
                expr[name].append(data_tmp[name][i])
                expr[name+'rms'].append(data_tmp[name+'rms'][i])

# experiment velocity
file_name = '../../../TUD_LDV_DEF/TUD_LDV_D.axial'
expu = np.genfromtxt(file_name,skip_header=13)
expu[:,2] = np.sqrt(expu[:,2])
expu[:,1:3] /= U_REF

# plot
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
margin_top      =0.3
space_width     =4.5
space_height    =1.5
ftsize          =12
# total height determined by the number of vars
plot_height     =((subplot_h+space_height)*3.0
                  -space_height+margin_top+margin_bottom)

fig, axes = plt.subplots(3,2,sharex='col',
                         figsize=fr.cm2inch(plot_width,plot_height))

# plot velocity
axes[0,0].plot(data[:,0],data[:,1],'-b',
               label='Sim.',linewidth=1.5)
axes[0,0].plot(expu[:,0],expu[:,1],'ok',
               label='Sim.',linewidth=1.5)
axes[0,0].set_ylabel(r'$\langle\tilde u\rangle/U_{\mathrm{ref}}$',
                     fontsize=ftsize)
axes[0,0].set_ylim(0,1.5)

axes[0,1].plot(data[:,0],data[:,2],'-b',
               label='Sim.',linewidth=1.5)
axes[0,1].plot(expu[:,0],expu[:,2],'ok',
               label='Sim.',linewidth=1.5)
axes[0,1].set_ylabel(r'$\langle\tilde u^{\prime\prime 2}\rangle^{1/2}$'
                     r'$/U_{\mathrm{ref}}$',
                     fontsize=ftsize)
axes[0,1].set_ylim(0,0.2)

for i,var in enumerate(scalar_name,start=1):
    axes[i,0].plot(data[:,0],data[:,2*i+1],'-b',
                   label='Sim.',linewidth=1.5)
    axes[i,0].plot(expr['z'],expr[var],'ok',
                   label='Sim.',linewidth=1.5)
    axes[i,1].plot(data[:,0],data[:,2*i+2],'-b',
                   label='Sim.',linewidth=1.5)
    axes[i,1].plot(expr['z'],expr[var+'rms'],'ok',
                   label='Sim.',linewidth=1.5)

axes[1,0].set_ylabel(r'$\langle\tilde T\rangle\;(\mathrm K)$',
                     fontsize=ftsize)
axes[1,0].set_ylim(0,2200)

axes[1,1].set_ylabel(r'$\langle\tilde T^{\prime\prime 2}\rangle^{1/2}$'
                     r'$\;(\mathrm K)$',
                     fontsize=ftsize)
axes[1,1].set_ylim(0,400)

axes[2,0].set_ylabel(r'$\langle\tilde Z\rangle$',
                     fontsize=ftsize)
axes[2,0].set_ylim(0,1.0)

axes[2,1].set_ylabel(r'$\langle\tilde Z^{\prime\prime 2}\rangle^{1/2}$',
                     fontsize=ftsize)
axes[2,1].set_ylim(0,0.2)

for i in range(2):
    axes[-1,i].set_xlabel('$x/D$',fontsize=ftsize)
    axes[-1,i].set_xlim(0.0,80.0)
    axes[-1,i].set_xticks(np.arange(0,81,20))

# legend
axes[0,0].legend(fontsize=ftsize,
                  numpoints=1,
                  frameon=False)

plt.subplots_adjust(left    =margin_left/plot_width,
                    bottom  =margin_bottom/plot_height,
                    right   =1.0-margin_right/plot_width,
                    top     =1.0-margin_top/plot_height,
                    wspace  =space_width/plot_width,
                    hspace  =space_height/plot_height)

# save plot
plt.savefig('axial_ave.png',dpi=400)
plt.savefig('axial_ave.pdf')
plt.savefig('axial_ave.eps')
