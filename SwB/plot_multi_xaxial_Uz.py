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

# marked number in simulation and experimental data
sim_index = 2
exp_index = 4

# cases
case_names = {
        'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL2':'Sim 2',
        'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL4':'Sim 4',
        'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL6':'Sim 6',
        'SwBd_Dq56_44M_FLAMELET_LUST_Linear_Sct07_FUEL8':'Sim 8',
        }
linestyle_sim = ['b--','r-.','g-','m:','k-.']

# import experiment data
data = np.genfromtxt('./Exp/div_15/PIV_138_8_set1.dat',delimiter=',')

x = list(set(data[:,0]))
z = list(set(data[:,1]))
z.sort(reverse=True)

z = np.flipud(z)
u = np.flipud(np.reshape(data[:,exp_index],(len(z),len(x))))

u_exp = np.empty(len(x))

z_loc = [50,70,90]

# plot
# figure and axes parameters
# total width is fixed
plot_width      =19
margin_left     =1.5
margin_right    =0.1
margin_bottom   =1.2
margin_top      =0.3
space_width     =0.1
space_height    =0.1
ftsize          =12

font = {'family':'serif',
        'weight':'normal',
        'size':ftsize}

# use TEX for interpreter
plt.rc('text',usetex=True)
# use serif font
plt.rc('font',**font)

num_cols = len(z_loc)
num_rows = 1

subplot_width = (plot_width
                -margin_left
                -margin_right
                -(num_cols-1)*space_width)/num_cols
subplot_height = subplot_width * 0.8

plot_height = (num_rows*subplot_height
              +margin_bottom
              +margin_top
              +(num_rows-1)*space_height)

fig, ax = plt.subplots(num_rows, num_cols,
        sharex=True, sharey = True,
        figsize=cm2inch(plot_width,plot_height))

for i, loc in enumerate(z_loc):
    for j in range(len(x)):
        u_exp[j] = np.interp( loc, z, u[:,j] )
    ax[i].plot( x, u_exp, 'k.', label = 'Exp 8' )

    ax[i].text(30,-4,'z={} mm'.format(loc))
    ax[i].set_xlabel(r'$r\;\mathrm{mm}$')

for k, v in enumerate(case_names.keys()):
    for i, loc in enumerate(z_loc):
        file_name = '{0}/sample_lines/z{1:d}.csv'.format(v,loc)
        data = np.genfromtxt(file_name,delimiter=',',names=True)

        x_sim = data['Points0']*1000
        u_sim = data['UMean{:d}'.format(sim_index)]

        ax[i].plot(x_sim,u_sim,linestyle_sim[k],label=case_names[v])

ax[0].set_xlim([0, 50])
ax[0].set_ylim([-5, 20])

ax[0].set_ylabel(r'$\langle u_z\rangle\;\mathrm{m/s}$')
ax[-1].legend(ncol=2,frameon=False)

fig.subplots_adjust(
        left = margin_left/plot_width,
        bottom = margin_bottom/plot_height,
        right = 1.0-margin_right/plot_width,
        top = 1.0-margin_top/plot_height,
        wspace = space_width/subplot_width,
        hspace = space_height/subplot_height
        )

fig.savefig('uz_radial.png')
