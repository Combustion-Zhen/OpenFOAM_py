"""
Zhen Lu, 29/04/2017 <albert.lz07@gmail.com>
apply numpy to load and process data
load and process flameletFoam results
mean and rms versus r/D for velocity
"""
import glob
import numpy as np

# print task
print('Take radial mean for *_xD.raw files')
# constant for files
# bin for average
rx_limit    = 0.3
# 'r' in the unit of mm
# diameter of the inlet jet
D           = 0.0072
rms         = 'rms'

# pick the latest time automatically
calc_time=[]
for filename in glob.glob('surfaces/*'):
    calc_time.append(float(filename[9:]))
time=str(max(calc_time))

# extract variable and location names
file_loc=[]
foldername='surfaces/{t}/U'.format(t=time)

# variables
file_str='{0}Mean_xD'.format(foldername)
for filename in glob.glob('{0}*.raw'.format(file_str)):
    file_loc.append(filename[len(file_str):-4])

# load data
for length in file_loc:
    file_ave = '{f}Mean_xD{loc}.raw'.format(f=foldername,
                                             loc=length)
    file_rms = '{f}Prime2Mean_xD{loc}.raw'.format(f=foldername,
                                                  loc=length)

    ave_tmp = np.genfromtxt(file_ave,skip_header=2)
    rms_tmp = np.genfromtxt(file_rms,skip_header=2)

    r = np.sqrt(np.square(ave_tmp[:,0])
                +np.square(ave_tmp[:,1])) / D
    for i,r_val in enumerate(r):
        r[i] = float('{:.3g}'.format(r_val))
    r_set = sorted(list(set(r)))
    print(len(r_set))

    data = np.column_stack((r,ave_tmp[:,3:]))
    data = np.hstack((data,rms_tmp[:,3:]))
    # print(data.shape)

    data_ave = np.zeros((len(r_set),10))
    data_ave[:,0] = r_set
    for i,r_val in enumerate(r_set):
        data_ave[i,1:]=np.average(data[:,1:],axis=0,weights=(r==r_val))
    np.savetxt('mean_U_xD{0}.csv'.format(length),
               data_ave)
