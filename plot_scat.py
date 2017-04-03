#Zhen Lu, 03/04/2017 <albert.lz07@gmail.com>
# plot Sandia Flame results, as title, the scatter at different x/D
import glob
from file_read import csv_read, cm2inch, SF_read
# suppress the display of matplotlib.pyplot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# data to plot
# only one var, two columns, left: exp., right: sim. rows for x/D
var  = 'T'

# import data
xD=[]
data={}
expr={}
for filename in glob.glob('scat*.csv'):
    pos = filename.find('.csv')
    z   = float('{0}.{1}'.format(filename[7:9],filename[9:pos]))
    xD.append(z)
    data.update({z:csv_read(filename)})
    expr.update({z:SF_read('D.scat',filename[7:pos],'all')})

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
plot_height     =(subplot_h+space_height)*float(len(xD)) \
                 -space_height+margin_top+margin_bottom
# min and max of axis
xmin = 0.0
xmax = 1.0
xtick= (0.0,0.2,0.4,0.6,0.8)

# generate the figure
fig, axes = plt.subplots(len(xD),2,
                         sharex='col',sharey='all',
                         figsize=cm2inch(plot_width, plot_height))
# generate the axis
for x in xD:
    axes[xD.index(x),0].scatter(expr[x]['Z'],expr[x][var],
                                marker='.',c='k',edgecolor='none')
    axes[xD.index(x),1].scatter(data[x]['Z'],data[x][var],
                                marker='.',c='k',edgecolor='none')
    # ylabel, temperature has a unit
    if var == 'T':
        axes[xD.index(x),0].set_ylabel(r"$\tilde {0}\;(\mathrm{{K}})$".format(var),
                                       fontsize=ftsize)
    else:
        axes[xD.index(x),0].set_ylabel(r"$\tilde Y\;{0}$".format(var),
                                       fontsize=ftsize)
    # location note
    # the text position determined by axes axis
    axes[xD.index(x),1].text(0.7,2000,'$x/D={0:.2g}$'.format(x),
                             fontsize=ftsize)
# ylabel, temperature has a unit
# title and xlabel
axes[0,0].set_title('Exp.',fontsize=ftsize)
axes[0,1].set_title('Sim.',fontsize=ftsize)
for i in range(2):
    axes[len(xD)-1,i].set_xlim(xmin,xmax)
    axes[len(xD)-1,i].set_xticks(xtick)
    axes[len(xD)-1,i].set_xlabel(r'$\tilde Z$',fontsize=ftsize)
axes[len(xD)-1,1].set_xticks(xtick+(xmax,))
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
