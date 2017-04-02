# Zhen Lu, 2017 <albert.lz07@gmail.com>
# plot Sandia Flame results, this version is only for browse, specific settings for different variables are required for journal artworks
import glob
import csv
from file_read import csv_read, cm2inch, SF_read
# suppress the display of matplotlib.pyplot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# data to plot
# two vars at least, because axes would be 1D vector for one var
var  = ['Z','T']
ymin = 0.0
ymax = 1.0

# import data
xD=[]
data={}
expr={}
for filename in glob.glob('mean_xD*.csv'):
    pos = filename.find('.csv')
    z   = float('{0}.{1}'.format(filename[7:9],filename[9:pos]))
    xD.append(z)
    data.update({z:csv_read(filename)})
    expr.update({z:SF_read('D.stat',filename[7:pos],'ave')})
for x in xD:
    for i in range(len(data[x]['r'])):
        data[x]['r'][i]/=x
    for i in range(len(expr[x]['r'])):
        expr[x]['r'][i]/=x

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
plot_height     =(subplot_h+space_height)*float(len(var))-space_height+margin_top+margin_bottom
# min and max of axis
xmin = 0.0
xmax = 0.3

# generate the figure
fig, axes = plt.subplots(len(var),len(xD),
                         sharex='all',sharey='row',
                         figsize=cm2inch(plot_width, plot_height))
# generate the axis
for v in var:
    for x in xD:
        axes[var.index(v),xD.index(x)].plot(data[x]['r'],data[x][v],'-b',
                                            expr[x]['r'],expr[x][v],'ok',
                                            linewidth=1.5)
    #temperature has a unit
    if v == 'T':
        axes[var.index(v),0].set_ylabel(r"$\langle\tilde {0}\rangle\;(\mathrm{{K}})$".format(v),
                                        fontsize=ftsize)
    elif v == 'Z':
        axes[var.index(v),0].set_ylabel(r"$\langle\tilde {0}\rangle$".format(v),
                                        fontsize=ftsize)
    else:
        axes[var.index(v),0].set_ylabel(r"$\langle\tilde Y\rangle\;{0}$".format(v),
                                        fontsize=ftsize)
# title and xlabel
for x in xD:
    #title
    axes[0,xD.index(x)].set_title('$x/D={0:.2g}$'.format(x),
                                  fontsize=ftsize)
    #r/x
    axes[len(var)-1,xD.index(x)].set_xlabel('$r/x$',
                                            fontsize=ftsize)

plt.xlim(xmin, xmax)
plt.xticks((0.0,0.1,0.2))

# set margins
plt.subplots_adjust(left    =margin_left/plot_width,
                    bottom  =margin_bottom/plot_height,
                    right   =1.0-margin_right/plot_width,
                    top     =1.0-margin_top/plot_height,
                    wspace  =space_width/plot_width,
                    hspace  =space_height/plot_height)

# labels
#plt.xlabel("$r/x$",fontsize=ftsize)
#plt.ylabel("$T\;(\mathrm{K})$",fontsize=ftsize)

# axis limits, ticks, and labels
#plt.axis([xmin, xmax, ymin, ymax])
#plt.xticks((0.0,0.2,0.4,0.6,0.8,1.0))
#plt.yticks(range(300,2301,500))
plt.savefig('radial_ave.eps')

# plot the rms
# generate the figure
#fig, axes = plt.subplots(len(var),len(xD),
#                         sharex='all',sharey='row',
#                         figsize=cm2inch(plot_width, plot_height))
#plt.savefig('radial_rms.eps')
