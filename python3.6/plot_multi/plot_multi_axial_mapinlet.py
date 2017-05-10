"""
Zhen Lu, 10/May/2017, <albert.lz07@gmail.com>
plot axial distribution of velocity, mixture fraction, and temperature
compared between different settings of the mapped inlet
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

# case to plot
path_name_pre ='flt_chi_7_inlet_'
path_name_mid ='map'
path_name_second ='/postProcessing/sets/'

case_name = []
simu = {}
for folder_name in glob.glob('{0}*{1}*'.format(path_name_pre,
                                               path_name_mid)):
    case = folder_name[len(path_name_pre)
                       :folder_name.find(path_name_mid)]
    case_name.append(case)

    # pick the latest time
    folder_full = folder_name+path_name_second
    calc_time=[]
    for file_name in glob.glob('{}*'.format(folder_full)):
        calc_time.append(float(file_name[len(folder_full):]))
    time=str(max(calc_time))

    # velocity
    file_name = '{0}{1}/axis_UMean.xy'.format(folder_full,time)
    data_tmp = np.genfromtxt(file_name)
    data = np.column_stack((data_tmp[:,0],data_tmp[:,-1]))

    # velocity rms
    file_name = '{0}{1}/axis_UPrime2Mean.xy'.format(folder_full,time)
    data_tmp = np.genfromtxt(file_name)
    data = np.column_stack((data,data_tmp[:,-1]))

    # Z and T
    file_name = (folder_full
                 + time
                 +'/axis_T{0}_T{1}_Z{0}_Z{1}.xy'.format('Mean',
                                                        'Prime2Mean'))
    data_tmp = np.genfromtxt(file_name)
    data = np.hstack((data,data_tmp[:,1:]))

    data[:,0] /= D

    loc_rms = np.arange(2,data.shape[1],2)
    data_tmp = np.maximum(data[:,loc_rms],0.0)
    data[:,loc_rms] = np.sqrt(data_tmp)

    data[:,1:3] /= U_REF

    simu.update({case:data})

# experiment scalar
folder_exp = '../pmCDEFarchives/pmD.stat/D'
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
file_name = '../TUD_LDV_DEF/TUD_LDV_D.axial'
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
margin_bottom   =1.2
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
axes[0,0].plot(expu[:,0],expu[:,1],'ok',
               label='Exp.',linewidth=1.5)
for case in case_name:
    axes[0,0].plot(simu[case][:,0],simu[case][:,1],
                   label=case,linewidth=1.5)
axes[0,0].set_ylabel(r'$\langle\tilde u\rangle/U_{\mathrm{ref}}$',
                     fontsize=ftsize)
axes[0,0].set_ylim(0,1.5)

axes[0,1].plot(expu[:,0],expu[:,2],'ok',
               label='Exp.',linewidth=1.5)
for case in case_name:
    axes[0,1].plot(simu[case][:,0],simu[case][:,2],
                   label=case,linewidth=1.5)
axes[0,1].set_ylabel(r'$\langle\tilde u^{\prime\prime 2}\rangle^{1/2}$'
                     r'$/U_{\mathrm{ref}}$',
                     fontsize=ftsize)
axes[0,1].set_ylim(0,0.2)

for i,var in enumerate(scalar_name,start=1):
    axes[i,0].plot(expr['z'],expr[var],'ok',
                   label='Exp.',linewidth=1.5)
    axes[i,1].plot(expr['z'],expr[var+'rms'],'ok',
                   label='Exp.',linewidth=1.5)
    for case in case_name:
        axes[i,0].plot(simu[case][:,0],simu[case][:,2*i+1],
                       label=case,linewidth=1.5)
        axes[i,1].plot(simu[case][:,0],simu[case][:,2*i+2],
                       label=case,linewidth=1.5)

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
plt.savefig('comp_inlet_axial_ave.png',dpi=400)
plt.savefig('comp_inlet_axial_ave.pdf')
plt.savefig('comp_inlet_axial_ave.eps')
