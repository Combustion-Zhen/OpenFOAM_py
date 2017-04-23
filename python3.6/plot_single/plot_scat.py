"""
Zhen Lu, 03/04/2017 <albert.lz07@gmail.com>
plot Sandia Flame results, as title, the scatter at different x/D
"""
import glob
import numpy as np
import file_read as fr
# suppress the display of matplotlib.pyplot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# data to plot
# only one var, two columns, left: exp., right: sim. rows for x/D
var  = 'T'

# import data
xD_value=[]
data={}
expr={}
for filename in glob.glob('scat*.csv'):
    pos = filename.find('.csv')
    xD = filename[7:pos]
    z = fr.z_str_to_num(xD)
    xD_value.append(z)
    data.update({z:np.genfromtxt(filename,
                                 delimiter=',',
                                 names=True)})
    exp_name='../../../pmCDEFarchives/pmD.scat/D{}.Yall'.format(xD)
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
plot_height     =((subplot_h+space_height)*float(len(xD))
                  -space_height+margin_top+margin_bottom)
# min and max of axis
xmin = 0.0
xmax = 1.0
xtick= tuple(np.arange(xmin,xmax,0.2))

# generate the figure
fig, axes = plt.subplots(len(xD_value),2,
                         sharex='col',sharey='all',
                         figsize=fr.cm2inch(plot_width, plot_height))
# generate the axis
for j,z in enumerate(xD_value):
    axes[j,0].scatter(expr[z]['Z'],expr[z][var],
                      marker='.',c='k',edgecolor='none')
    axes[j,1].scatter(data[z]['Z'],data[z][var],
                      marker='.',c='k',edgecolor='none')
    # ylabel, temperature has a unit
    if var == 'T':
        str_label=r"$\tilde T\;(\mathrm{{K}})$"
    else:
        str_label=r"$\tilde Y_{\mathrm{"+var+r"}}$"
    axes[j,0].set_ylabel(str_label,
                         fontsize=ftsize)
    # location note
    # the text position determined by axes axis
    axes[j,1].text(0.7,2000,'$x/D={0:.2g}$'.format(z),
                   fontsize=ftsize)
# ylabel, temperature has a unit
# title and xlabel
axes[0,0].set_title('Exp.',fontsize=ftsize)
axes[0,1].set_title('Sim.',fontsize=ftsize)
for i in range(2):
    axes[-1,i].set_xlim(xmin,xmax)
    axes[-1,i].set_xticks(xtick)
    axes[-1,i].set_xlabel(r'$\tilde Z$',fontsize=ftsize)
axes[-1,1].set_xticks(xtick+(xmax,))
# legend

# set margins
plt.subplots_adjust(left    =margin_left/plot_width,
                    bottom  =margin_bottom/plot_height,
                    right   =1.0-margin_right/plot_width,
                    top     =1.0-margin_top/plot_height,
                    wspace  =space_width/plot_width,
                    hspace  =space_height/plot_height)

# save plot
plt.savefig('radial_scat.png',dpi=400)
plt.savefig('radial_scat.pdf')
plt.savefig('radial_scat.eps')
