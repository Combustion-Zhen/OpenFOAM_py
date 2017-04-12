# Zhen Lu, 03/04/2017 <albert.lz07@gmail.com>
# load and process flameletFoam results
# scatter data and conditional mean
import glob
import csv
import math

# bin size for mixture fraction, it is 0.02 for experiment
bin_num     = 100
bin_size    = 1.0/bin_num
rx_limit    = 0.3

# pick the latest time automatically
calc_time=[]
for filename in glob.glob('surfaces/*'):
    calc_time.append(float(filename[9:]))
time=str(max(calc_time))

# extract variable and location names
var_names   = []
loc_names   = []
foldername  = 'surfaces/{t}/'.format(t=time)
str_mean    = 'Mean'
# variables
for filename in glob.glob('{0}*.raw'.format(foldername)):
    if str_mean not in filename and '_xD' in filename:
        var_names.append(filename[len(foldername):filename.find('_xD')])
var_names=list(set(var_names))
# must have mixture fraction Z
if 'Z' not in var_names:
    raise
for filename in glob.glob('{0}{1}_xD*.raw'.format(foldername,'Z')):
    loc_names.append(filename[filename.find('_xD')+3:filename.find('.raw')])

for loc in loc_names:
    # load data
    loc_data={}
    loc_cond={}
    loc_cond.update({'Nave':[]})
    for var in var_names:
        loc_data.update({var:[]})
        loc_cond.update({var:[]})
        filename= '{0}{1}_xD{2}.raw'.format(foldername,var,loc)
        with open(filename,'r') as file_loc:
            # read the head lines
            file_loc.readline()
            file_loc.readline()
            for line in file_loc:
                [x, y, z, data]=line.strip().split()
                r = math.sqrt(float(x)**2+float(y)**2)
                if r/float(z) < rx_limit:
                    loc_data[var].append(float(data))
    # conditional mean
    # initialization
    for i in range(bin_num):
        loc_cond['Nave'].append(0)
        for var in var_names:
            loc_cond[var].append(0.0)
    # sum
    for i in range(len(loc_data['Z'])):
        Z_idx = int(loc_data['Z'][i]//bin_size)
        loc_cond['Nave'][Z_idx] += 1
        for var in var_names:
            loc_cond[var][Z_idx] += loc_data[var][i]
    # average and remove empty entry
    for i in range(bin_num-1,-1,-1):
        if loc_cond['Nave'][i] != 0:
            for var in var_names:
                loc_cond[var][i] /= float(loc_cond['Nave'][i])
        else:
            del loc_cond['Nave'][i]
            for var in var_names:
                del loc_cond[var][i]
    # write data
    # scatter
    with open('scat_xD{0}.csv'.format(loc),'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=loc_data.keys())
        writer.writeheader()
        for i in range(len(loc_data['Z'])):
            data_row={}
            for var in loc_data.keys():
                data_row.update({var:'{:e}'.format(loc_data[var][i])})
            writer.writerow(data_row)
    # conditional average
    with open('cond_xD{0}.csv'.format(loc),'w') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=loc_cond.keys())
        writer.writeheader()
        for i in range(len(loc_cond['Z'])):
            data_row={}
            data_row.update({'Nave':'{:d}'.format(loc_cond['Nave'][i])})
            for var in var_names:
                data_row.update({var:'{:e}'.format(loc_cond[var][i])})
            writer.writerow(data_row)
