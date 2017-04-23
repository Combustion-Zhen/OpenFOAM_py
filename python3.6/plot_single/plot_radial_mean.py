# Zhen Lu, 2017 <albert.lz07@gmail.com>
# plot Sandia Flame results, this version is only for browse, specific
# settings for different variables are required for journal artworks
import glob
import numpy as np
import file_read as fr
# suppress the display of matplotlib.pyplot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# data to plot
# two vars at least, because axes would be 1D vector for one var
var  = ['Z','T','CO']

# import data
xD_value=[]
data={}
expr={}
for filename in glob.glob('mean_xD*.csv'):
    pos = filename.find('.csv')
    xD_name = filename[7:pos]
    z   = fr.z_str_to_num(xD_name)
    xD_value.append(z)
    data.update({z:np.genfromtxt(filename,
                                 delimiter=',',
                                 names=True)})
    exp_name='../../../pmCDEFarchives/pmD.stat/D{}.Yave'.format(xD_name)
    expr.update({z:fr.sf_expr_read(exp_name)})
xD_value.sort()
for z in xD_value:
    data[z]['r'] /= z
    expr[z]['r'] /= z

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
xtick= tuple(np.arange(xmin,xmax,0.1))

# generate the figure
fig, axes = plt.subplots(len(var),len(xD_value),
                         sharex='col',sharey='row',
                         figsize=fr.cm2inch(plot_width, plot_height))
# generate the axis
for i,v in enumerate(var):
    for j,z in enumerate(xD_value):
        axes[i,j].plot(data[z]['r'],data[z][v],'-b',
                       label='Sim.',linewidth=1.5)
        axes[i,j].plot(expr[z]['r'],expr[z][v],'ok',
                       label='Exp.',linewidth=1.5)
    # ylabel, temperature has a unit
    if v == 'T':
        str_label=r"$\langle\tilde{{T}}\rangle\;(\mathrm{{K}})$"
    elif v == 'Z':
        str_label=r"$\langle\tilde{{Z}}\rangle$"
    else:
        str_label=r'$\langle\tilde Y_{\mathrm{'+v+r'}}\rangle$'
    axes[i,0].set_ylabel(str_label,fontsize=ftsize)
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
axes[0,-1].legend(fontsize=ftsize,
                  numpoints=1,
                  frameon=False)

# set margins
plt.subplots_adjust(left    =margin_left/plot_width,
                    bottom  =margin_bottom/plot_height,
                    right   =1.0-margin_right/plot_width,
                    top     =1.0-margin_top/plot_height,
                    wspace  =space_width/plot_width,
                    hspace  =space_height/plot_height)

# save plot
plt.savefig('radial_ave.png',dpi=400)
plt.savefig('radial_ave.pdf')
plt.savefig('radial_ave.eps')

# plot the rms
# generate the figure
fig, axes = plt.subplots(len(var),len(xD_value),
                         sharex='col',sharey='row',
                         figsize=fr.cm2inch(plot_width, plot_height))
# generate the axis
for i,v in enumerate(var):
    for j,z in enumerate(xD_value):
        axes[i,j].plot(data[z]['r'],data[z][v+'rms'],'-b',
                       label='Sim.',linewidth=1.5)
        axes[i,j].plot(expr[z]['r'],expr[z][v+'rms'],'ok',
                       label='Exp.',linewidth=1.5)
    # ylabel, temperature has a unit
    if v == 'T':
        str_label=(r"$\langle\tilde{{T}}^{{\prime\prime 2}}"
                   r"\rangle\;(\mathrm{{K}})$")
    elif v == 'Z':
        str_label=r"$\langle\tilde{{Z}}^{{\prime\prime 2}}\rangle$"
    else:
        str_label=(r'$\langle\tilde Y^{{\prime\prime 2}}_{\mathrm{'
                   +v+r'}}\rangle$')
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
axes[0,-1].legend(fontsize=ftsize,
                  numpoints=1,
                  frameon=False)

# set margins
plt.subplots_adjust(left    =margin_left/plot_width,
                    bottom  =margin_bottom/plot_height,
                    right   =1.0-margin_right/plot_width,
                    top     =1.0-margin_top/plot_height,
                    wspace  =space_width/plot_width,
                    hspace  =space_height/plot_height)

plt.savefig('radial_rms.png',dpi=400)
plt.savefig('radial_rms.pdf')
plt.savefig('radial_rms.eps')
