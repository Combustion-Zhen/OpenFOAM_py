# Zhen Lu, 12/04/2017 <albert.lz07@gmail.com>
# plot Sandia Flame results, the 2D contour
from file_read import csv_read, cm2inch
# suppress the display of matplotlib.pyplot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# variable to be plot
var = 'Z'

xD_limit=25.0
rD_limit=5.0

# import data
field_data=csv_read('mean_field.csv')

# plot
# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',family='serif')
# figure and axes parameters
# total width is fixed
plot_width      =9.0
plot_height     =9.0
margin_left     =2.0
margin_right    =0.3
margin_bottom   =1.5
margin_top      =1.0
space_width     =0.0
space_height    =1.0
ftsize          =12
# min and max of axis


# legend

# set margins
#plt.subplots_adjust(left    =margin_left/plot_width,
#                    bottom  =margin_bottom/plot_height,
#                    right   =1.0-margin_right/plot_width,
#                    top     =1.0-margin_top/plot_height,
#                    wspace  =space_width/plot_width,
#                    hspace  =space_height/plot_height)

