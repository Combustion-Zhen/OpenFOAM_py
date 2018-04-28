import numpy as np
import os

# output directory
OUTDIR='sample_lines'

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

t_list = [0.32,0.34,0.36,0.38,0.4]

z_loc = [42,45,50,55,60,65,70,80,90]

TIMDIR='sample_t'

for z in z_loc:
    for i,t in enumerate(t_list):
        file_name = '{0}{1}/z{2:d}.csv'.format(TIMDIR,t,z)
        data = np.genfromtxt(file_name,delimiter=',',skip_header=1)

        if i == 0:
            data_all = data
        else:
            data_all = data_all + data

    with open(file_name,'r') as f:
        data_names = f.readline()

    data_ave = data_all/len(t_list)
    data_names = data_names.replace('\r','').replace('\n','')

    file_name = '{0}/z{1:d}.csv'.format(OUTDIR,z)
    np.savetxt(file_name,data_ave,delimiter=',',header=data_names,comments='')
