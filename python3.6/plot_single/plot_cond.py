"""
Zhen Lu, 03/04/2017 <albert.lz07@gmail.com>
modified 23/04/2017
plot Sandia Flame results, as title, 
the conditional mean at different x/D
"""
import glob
import numpy as np
import file_read as fr
# suppress the display of matplotlib.pyplot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# data to plot
# two vars at least, because axes would be 1D vector for one var
var  = ['T','CO2']

# import data
xD_value=[]
data={}
expr={}
for filename in glob.glob('cond_*.csv'):
    pos = filename.find('.csv')
    xD = filename[7:pos]
    z = fr.z_str_to_num(xD)
    xD_value.append(z)
    data.update({z:np.genfromtxt(filename,
                                 delimiter=',',
                                 names=True)})
    exp_name='../../../pmCDEFarchives/pmD.stat/D{}.Ycnd'.format(xD)
    expr.update({z:fr.sf_expr_read(exp_name)})
xD_value.sort()

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
xmax = 1.0
xtick= tuple(np.arange(xmin,xmax,0.2))

# generate the figure
fig, axes = plt.subplots(len(var),len(xD_value),
                         sharex='col',sharey='row',
                         figsize=fr.cm2inch(plot_width, plot_height))
# generate the axis
for i,v in enumerate(var):
    for j,z in enumerate(xD_value):
        axes[i,j].plot(data[z]['Z'],data[z][v],'-b',
                       label='Sim.',linewidth=1.5)
        axes[i,j].plot(expr[z]['Z'],expr[z][v],'.k',
                       label='Exp.',linewidth=1.5)
    # ylabel, temperature has a unit
    if v == 'T':
        str_label=(r"$\langle\tilde{{T}}\vert\tilde Z"
                   r"\rangle\;(\mathrm{{K}})$")
    else:
        str_label=(r"$\langle\tilde Y_{\mathrm{"
                   +v
                   +r"}}\vert\tilde Z\rangle$")
    axes[i,0].set_ylabel(str_label,fontsize=ftsize)
# title and xlabel
for j,z in enumerate(xD_value):
    #title
    axes[0,j].set_title('$x/D={0:.2g}$'.format(z),
                        fontsize=ftsize)
    axes[-1,j].set_xlabel(r'$\tilde Z$',
                          fontsize=ftsize)
    axes[-1,j].set_xlim(xmin,xmax)
    axes[-1,j].set_xticks(xtick)

axes[-1,-1].set_xticks(xtick+(xmax,))

# legend
axes[0,-1].legend(fontsize   =ftsize,
                  loc        ='lower right',
                  numpoints  =1,
                  frameon    =False)

# set margins
plt.subplots_adjust(left    =margin_left/plot_width,
                    bottom  =margin_bottom/plot_height,
                    right   =1.0-margin_right/plot_width,
                    top     =1.0-margin_top/plot_height,
                    wspace  =space_width/plot_width,
                    hspace  =space_height/plot_height)

# save plot
plt.savefig('radial_cnd.png',dpt=400)
plt.savefig('radial_cnd.pdf')
plt.savefig('radial_cnd.eps')
