# Zhen Lu, 31/03/2017
# load and process flameletFoam results
# mean and rms versus r/D
import glob
import math
import csv

# some constants
# time
time        = '0.25'
# constant for files
# bin for average
rx_limit    = 0.3
bin_num     = 100
# 'r' in the unit of mm
bin_size    = 0.001/bin_num
# diameter of the inlet jet
D           = 0.0072
rms         = 'rms'

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
    loc_data={'r':[]}
    loc_file={}
    #line_num=0
    for var in var_names:
        filename_mean = '{f}{v}Mean_xD{loc}.raw'.format(f=foldername,v=var,loc=length)
        filename_rms  = '{f}{v}Prime2Mean_xD{loc}.raw'.format(f=foldername,v=var,loc=length)
        fid_m = open(filename_mean,'r')
        fid_r = open(filename_rms,'r')
        # two lines of comments
        line=fid_r.readline()
        line=fid_m.readline()
        if var is var_names[0]:
            line_num=int(line.strip().split()[3])
        fid_r.readline()
        fid_m.readline()
        # file
        loc_file.update({var:fid_m})
        loc_file.update({var+rms:fid_r})
        # data
        loc_data.update({var:[]})
        loc_data.update({var+rms:[]})
    # update the bin number
    x_pos=float('{0}.{1}'.format(length[:2],length[2:]))*D
    bin_num=int(x_pos*rx_limit/bin_size)
    #print(bin_num)
    # make the initial values
    data_names=loc_data.keys()
    data_names.remove('r')
    for i in range(bin_num):
        # it is firstly used to store the point count
        loc_data['r'].append(0)
        for var in data_names:
            loc_data[var].append(0.0)
    # read in and calculate the sum
    for i in range(line_num):
        for var in data_names:
            line=loc_file[var].readline()
            line=line.strip()
            [x, y, z, data]=line.split()
            # data of radius
            if var is data_names[0]:
                #calculate the radius
                r=math.sqrt(float(x)**2+float(y)**2)
            if r/x_pos < rx_limit:
                r_idx=int(r//bin_size)
                # to be divided by the number of vars
                loc_data['r'][r_idx]+=1
                loc_data[var][r_idx]+=float(data)
    # calculate the average
    for i in range(bin_num-1,-1,-1):
        loc_data['r'][i]/=len(data_names)
        if loc_data['r'][i] != 0:
            # it should be the number of grids in \theta
            #print(loc_data['r'][i])
            for var in data_names:
                loc_data[var][i]/=float(loc_data['r'][i])
                #square root for the rms
                if 'rms' in var:
                    loc_data[var][i]=math.sqrt(loc_data[var][i])
            loc_data['r'][i]=(float(i)*bin_size+bin_size/2.0)/D
        else:
            for var in data_names:
                del loc_data[var][i]
            del loc_data['r'][i]
    loc_data['r'][0]=0.0
    # close files
    for var in data_names:
        loc_file[var].close()

    # write data to .csv
    with open('mean_xD{loc}.csv'.format(loc=length),'w') as csvfile:
        # make the output ordered
        fieldnames=['r',]
        for var in var_names:
            fieldnames.append(var)
            fieldnames.append(var+rms)
        # writer = csv.DictWriter(csvfile,fieldnames=loc_data.keys())
        writer = csv.DictWriter(csvfile,fieldnames=fieldnames)
        writer.writeheader()
        for i in range(len(loc_data['r'])):
            data_row={}
            for var in loc_data.keys():
                data_row.update({var:'{:e}'.format(loc_data[var][i])})
            writer.writerow(data_row)
