# Zhen Lu, 2017, <albert.lz07@gmail.com>
# plot Sandia Flame results with different numerical settings
import file_read as fr
import numpy as np
import glob
#import file_read
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# data to plot
var = ['Z','T','CO']

# case to plot
# for different settings of Sct and Sc
path_name_pre ='flt_chi_7_inlet_turb_pilot_turb_'
path_name_second ='/postProcessing/'

xD_name = []
xD_value = []
case_name = []
data = {}
for folder_name in glob.glob('{}*'.format(path_name_pre)):
    case = folder_name[len(path_name_pre):]
    case_name.append(case)
    for file_name in glob.glob('{0}{1}mean_xD*.csv'
                               .format(folder_name,
                                       path_name_second)):
        xD = file_name[file_name.find('_xD')+3:-4]
        z = fr.z_str_to_num(xD)
        xD_name.append(xD)
        xD_value.append(z)
        data.update({(case,z):np.genfromtxt(file_name,
                                            delimiter=',',
                                            names=True)})
xD_name = list(set(xD_name))
xD_value = sorted(list(set(xD_value)))

expr = {}
for xD in xD_name:
    file_name = '../pmCDEFarchives/pmD.stat/D{0}.Yave'.format(xD)
    expr.update({fr.z_str_to_num(xD):fr.sf_expr_read(file_name)})

for z in xD_value:
    expr[z]['r'] /= z
    for case in case_name:
        data[(case,z)]['r'] /= z

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
margin_top      =1.0
space_width     =0.0
space_height    =1.0
ftsize          =12
# total height determined by the number of vars
plot_height     =((subplot_h+space_height)*float(len(var))
                 -space_height+margin_top+margin_bottom)
# min and max of axis
xmin = 0.0
xmax = 0.3
xtick= (0.0,0.1,0.2)

# generate the figure
fig, axes = plt.subplots(len(var),len(xD_value),
                         sharex='col',sharey='row',
                         figsize=fr.cm2inch(plot_width, plot_height))
# generate the axis
for i,v in enumerate(var):
    for j,z in enumerate(xD_value):
        axes[i,j].plot(expr[z]['r'],expr[z][v],'ok',
                       label='Exp.',linewidth=1.5)
        for case in case_name:
            pos_sc = case.find('_Sc')
            str_label=("$\mathrm{{Sc}}_t\;{0}\;\mathrm{{Sc}}\;{1}$"
                       .format(case[3:pos_sc],case[pos_sc+3:]))
            axes[i,j].plot(data[(case,z)]['r'],data[(case,z)][v],
                           label=str_label,linewidth=1.5)
    # ylabel, temperature has a unit
    if v == 'T':
        str_label=r"$\langle\tilde{{T}}\rangle\;(\mathrm{{K}})$"
    elif v == 'Z':
        str_label=r"$\langle\tilde{{Z}}\rangle$"
    else:
        str_label=r'$\langle\tilde Y_{\mathrm{'+v+r'}}\rangle$'
    axes[i,0].set_ylabel(str_label,
                         fontsize=ftsize)
# title and xlabel
for j,z in enumerate(xD_value):
    #title
    axes[0,j].set_title('$x/D={0:.2g}$'.format(z),
                        fontsize=ftsize)
    #r/x
    axes[-1,j].set_xlabel('$r/x$',
                          fontsize=ftsize)
    axes[-1,j].set_xlim(xmin,xmax)
    axes[-1,j].set_xticks(xtick)

axes[-1,-1].set_xticks(xtick+(xmax,))

# legend
axes[0,-1].legend(fontsize=ftsize-2,
                  numpoints=1,
                  frameon=False)

# set margins
plt.subplots_adjust(left    =margin_left/plot_width,
                    bottom  =margin_bottom/plot_height,
                    right   =1.0-margin_right/plot_width,
                    top     =1.0-margin_top/plot_height,
                    wspace  =space_width/plot_width,
                    hspace  =space_height/plot_height)

## save plot
plt.savefig('comp_radial_ave.png',dpi=400)
plt.savefig('comp_radial_ave.pdf')
plt.savefig('comp_radial_ave.eps')

# plot the rms
# generate the figure
fig, axes = plt.subplots(len(var),len(xD_value),
                         sharex='col',sharey='row',
                         figsize=fr.cm2inch(plot_width, plot_height))
# generate the axis
for i,v in enumerate(var):
    for j,z in enumerate(xD_value):
        axes[i,j].plot(expr[z]['r'],expr[z][v+'rms'],'ok',
                       label='Exp.',linewidth=1.5)
        for case in case_name:
            pos_sc = case.find('_Sc')
            str_label=("$\mathrm{{Sc}}_t\;{0}\;\mathrm{{Sc}}\;{1}$"
                       .format(case[3:pos_sc],case[pos_sc+3:]))
            axes[i,j].plot(data[(case,z)]['r'],data[(case,z)][v+'rms'],
                           label=str_label,linewidth=1.5)
    # ylabel, temperature has a unit
    if v == 'T':
        str_label=(r'$\langle\tilde{T}^{\prime\prime 2}'
                   r'\rangle^{1/2}\;(\mathrm{{K}})$')
    elif v == 'Z':
        str_label=r'$\langle\tilde{Z}^{\prime\prime 2}\rangle^{1/2}$'
    else:
        str_label=(r'$\langle\tilde Y^{\prime\prime 2}_{\mathrm{'
                   +v+r'}}\rangle^{1/2}$')
    axes[i,0].set_ylabel(str_label,
                         fontsize=ftsize)
# title and xlabel
for j,z in enumerate(xD_value):
    #title
    axes[0,j].set_title('$x/D={0:.2g}$'.format(z),
                        fontsize=ftsize)
    #r/x
    axes[-1,j].set_xlabel('$r/x$',
                          fontsize=ftsize)
    axes[-1,j].set_xlim(xmin,xmax)
    axes[-1,j].set_xticks(xtick)

axes[-1,-1].set_xticks(xtick+(xmax,))

# legend
axes[0,-1].legend(fontsize=ftsize-4,
                  numpoints=1,
                  frameon=False)

# set margins
plt.subplots_adjust(left    =margin_left/plot_width,
                    bottom  =margin_bottom/plot_height,
                    right   =1.0-margin_right/plot_width,
                    top     =1.0-margin_top/plot_height,
                    wspace  =space_width/plot_width,
                    hspace  =space_height/plot_height)

plt.savefig('comp_radial_rms.png',dpi=400)
plt.savefig('comp_radial_rms.pdf')
plt.savefig('comp_radial_rms.eps')
