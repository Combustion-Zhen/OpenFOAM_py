# Zhen Lu, 13/04/2017 <albert.lz07@gmail.com>
# load and process flameletFoam results
# mean and rms versus r/D
import glob
import math
import csv

# print task
print('Take radial mean for *_xD*.raw files')
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
var_names=[]
file_loc=[]
foldername='surfaces/{t}/'.format(t=time)
filename_int_var='Mean_xD'
filename_int_rms='Prime2Mean_xD'
# variables
for filename in glob.glob('{0}*{1}*.raw'.format(foldername,filename_int_rms)):
    pos = filename.find('Prime2Mean_xD')
    var_names.append(filename[len(foldername):pos])
var_names=list(set(var_names))
# the velocity has three components, remove it at first
if 'U' in var_names:
    var_names.remove('U')
# x/D
file_str='{0}{1}{2}'.format(foldername,var_names[0],filename_int_var)
for filename in glob.glob('{0}*.raw'.format(file_str)):
    pos = filename.find('.raw')
    file_loc.append(filename[len(file_str):pos])

# load data
for length in file_loc:
    # get the x by x/D
    xD_val  =float('{0}.{1}'.format(length[:2],length[2:]))
    x_pos   =xD_val*D
    r       =[]
    loc_file={}
    loc_mean={}
    for var in var_names:
        filename_ave = '{f}{v}Mean_xD{loc}.raw'.format(f=foldername,v=var,loc=length)
        filename_rms = '{f}{v}Prime2Mean_xD{loc}.raw'.format(f=foldername,v=var,loc=length)
        # store file names
        loc_file.update({var:filename_ave})
        loc_file.update({var+rms:filename_rms})
        # read radius information in the first variable file
        if var is var_names[0]:
            with open(loc_file[var],'r') as var_file:
                var_file.readline()
                var_file.readline()
                for line in var_file:
                    x=float(line.strip().split()[0])
                    y=float(line.strip().split()[1])
                    r.append(float('{:.3g}'.format(math.sqrt(x**2+y**2)/D)))
    # check the number of points to be averaged
    r_set=sorted(list(set(r)))
    print('{0} points on radial direction for x/D: {1}'.format(len(r_set),xD_val))
    #print(sorted(list(r_set)))
    for r_val in r_set:
        loc_mean.update({(r_val,'count'):0})
        for var in loc_file.keys():
            loc_mean.update({(r_val,var):0.0})
    for r_val in r:
        loc_mean[(r_val,'count')]+=1
    #print(loc_mean)
    # read in data, sum, average
    for var in loc_file.keys():
        with open(loc_file[var]) as var_file:
            var_file.readline()
            var_file.readline()
            # sum
            for i in range(len(r)):
                loc_mean[(r[i],var)]+=float(var_file.readline().strip().split()[3])
            # average
            for r_val in r_set:
                loc_mean[(r_val,var)]/=float(loc_mean[(r_val,'count')])
                if 'rms' in var:
                    loc_mean[(r_val,var)]=math.sqrt(max([loc_mean[(r_val,var)],0.0]))
    # write to csv file
    with open('mean_xD{0}.csv'.format(length),'w') as csvfile:
        field_names=['r']
        for var in loc_file.keys():
            field_names.append(var)
        writer=csv.DictWriter(csvfile,fieldnames=field_names)
        writer.writeheader()
        for r_val in r_set:
            data_row={'r':'{:e}'.format(r_val)}
            for var in loc_file.keys():
                data_row.update({var:'{:e}'.format(loc_mean[(r_val,var)])})
            writer.writerow(data_row)
