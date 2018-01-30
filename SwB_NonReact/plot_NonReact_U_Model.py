"""
Zhen Lu 2017/01/11

Compare the results of non-reacting flow from FLUENT and OpenFOAM

FLUENT: Smagorinski, Dynamic Smagorinski, WALE
OpenFOAM: Smagorinski

figures have two column, one for the mean velocity, the other for the rms
"""

import numpy as np
import glob
import matplotlib as mpl
#mpl.use('Agg')
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

cas_pre = 'SwBd_L-400_20M_'

OF_cas = 'PISO_Bulk'
FLUENT_cas = ['Smag','DynS','WALE']
line_style = ['--','-.',':']
line_color = ['tab:red','tab:green','tab:blue']
line_width = 1.5

#z_loc = [-350,-300,-250,-200,-150,-100]
z_loc = [-80,-70,-60,-50,-30,-10]
#z_loc = [5,10,20,30]
#z_loc = [42,45,50,55]
#z_loc = [60,65,70,80,90]

OF_folder = ''.join([cas_pre,OF_cas,'/sample_lines'])

# import FLUENT data
FLUENT_dat = {}
for model in FLUENT_cas:
    file_name = '{0}FLUENT_{1}/{0}{1}_ave_vel.dat'.format(cas_pre,model)
    data = np.genfromtxt(file_name,delimiter=',',names=True)

    data['zcoordinate'] = np.rint(data['zcoordinate']*1000)

    FLUENT_dat[model]=data

# figure settings
plot_width      =19.0
margin_left     =1.2
margin_right    =0.3
margin_bottom   =1.2
margin_top      =0.3
space_width     =1.5
space_height    =0.0
ftsize          =11

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = 2
num_rows = len(z_loc)

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.3

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

################################################################################

    # import OF data
    OF_file = 'z{:d}.csv'.format(z_loc[i])
    file_name = '/'.join([OF_folder,OF_file])
    OF_data = np.genfromtxt(file_name,delimiter=',',names=True)
    OF_data = OF_data[np.isfinite(OF_data['p'])]

################################################################################

    axz[i,0].plot(OF_data['Points0'],OF_data['UMean2'],'k-',
            label='OpenFOAM',lw=line_width)
    axz[i,1].plot(OF_data['Points0'],np.sqrt(OF_data['UPrime2Mean2']),'k-',
            label='OpenFOAM',lw=line_width)

    for j, model in enumerate(FLUENT_cas):
        data=FLUENT_dat[model]
        data=data[data['zcoordinate']==z_loc[i]]

        data.sort(order='xcoordinate')

        axz[i,0].plot(data['xcoordinate'],data['meanzvelocity'],
                label=model,lw=line_width,ls=line_style[j],c=line_color[j])
        axz[i,1].plot(data['xcoordinate'],data['rmsezvelocity'],
                label=model,lw=line_width,ls=line_style[j],c=line_color[j])

################################################################################

    axr[i,0].plot(OF_data['Points0'],OF_data['UMean0'],'k-',
            label='OpenFOAM',lw=line_width)
    axr[i,1].plot(OF_data['Points0'],np.sqrt(OF_data['UPrime2Mean0']),'k-',
            label='OpenFOAM',lw=line_width)

    for j, model in enumerate(FLUENT_cas):
        data=FLUENT_dat[model]
        data=data[data['zcoordinate']==z_loc[i]]

        data.sort(order='xcoordinate')

        axr[i,0].plot(data['xcoordinate'],data['meanxvelocity'],
                label=model,lw=line_width,ls=line_style[j],c=line_color[j])
        axr[i,1].plot(data['xcoordinate'],data['rmsexvelocity'],
                label=model,lw=line_width,ls=line_style[j],c=line_color[j])

################################################################################

    axt[i,0].plot(OF_data['Points0'],OF_data['UMean1'],'k-',
            label='OpenFOAM',lw=line_width)
    axt[i,1].plot(OF_data['Points0'],np.sqrt(OF_data['UPrime2Mean1']),'k-',
            label='OpenFOAM',lw=line_width)

    for j, model in enumerate(FLUENT_cas):
        data=FLUENT_dat[model]
        data=data[data['zcoordinate']==z_loc[i]]

        data.sort(order='xcoordinate')

        axt[i,0].plot(data['xcoordinate'],data['meanyvelocity'],
                label=model,lw=line_width,ls=line_style[j],c=line_color[j])
        axt[i,1].plot(data['xcoordinate'],data['rmseyvelocity'],
                label=model,lw=line_width,ls=line_style[j],c=line_color[j])

################################################################################

for i in range(num_rows):
    axz[i,0].set_ylabel(r'$u_z\;\mathrm{m/s}$')
    axz[i,1].set_ylabel(r'$\mathrm{rms}\;u_z\;\mathrm{m/s}$')
    axz[i,1].text(0,5,'z={:g} mm'.format(z_loc[i]))

    axr[i,0].set_ylabel(r'$u_x\;\mathrm{m/s}$')
    axr[i,1].set_ylabel(r'$\mathrm{rms}\;u_x\;\mathrm{m/s}$')
    axr[i,1].text(0,5,'z={:g} mm'.format(z_loc[i]))

    axt[i,0].set_ylabel(r'$u_y\;\mathrm{m/s}$')
    axt[i,1].set_ylabel(r'$\mathrm{rms}\;u_y\;\mathrm{m/s}$')
    axt[i,1].text(0,5,'z={:g} mm'.format(z_loc[i]))

for i in range(num_cols):
    axz[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')
    axr[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')
    axt[-1,i].set_xlabel(r'$x\;\mathrm{mm}$')

axz[0,0].legend(
        ncol=2,frameon=False)
axr[0,0].legend(
        ncol=2,frameon=False)
axt[0,0].legend(
        ncol=2,frameon=False)

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

figz.savefig('velz_z{:d}.eps'.format(z_loc[0]))
figr.savefig('velr_z{:d}.eps'.format(z_loc[0]))
figt.savefig('velt_z{:d}.eps'.format(z_loc[0]))

figz.savefig('velz_z{:d}.pdf'.format(z_loc[0]))
figr.savefig('velr_z{:d}.pdf'.format(z_loc[0]))
figt.savefig('velt_z{:d}.pdf'.format(z_loc[0]))
