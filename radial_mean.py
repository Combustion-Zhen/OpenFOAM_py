# Zhen Lu, 31/03/2017
# load and process flameletFoam results
# mean and rms versus r/x
import math
import string
import csv
# suppress the display of matplotlib.pyplot
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt

# time and variable
time        = 0.16
var_names   = ('Z','T')
rms         = 'rms'
# constant for files
file_loc    = ('075','15','30','45')
# bin for average, bin number means the number of bins on the range rx_limit
rx_limit    = 0.5
bin_num     = 100
bin_size    = rx_limit/bin_num
# diameter of the inlet jet
D           = 0.0072
# 'r' is in the unit of r/x

# load data
for length in file_loc:
    loc_data={'r':[]}
    loc_file={}
    #line_num=0
    for var in var_names:
        filename_mean = 'surfaces/{t}/{v}Mean_xD{loc}.raw'.format(t=str(time),v=var,loc=length)
        filename_rms  = 'surfaces/{t}/{v}Prime2Mean_xD{loc}.raw'.format(t=str(time),v=var,loc=length)
        fid_m = open(filename_mean,'r')
        fid_r = open(filename_rms,'r')
        # two lines of comments
        line=fid_r.readline()
        line=fid_m.readline()
        if var is var_names[0]:
            line_num=int(line[line.find('FACE_DATA')+9:])
        fid_r.readline()
        fid_m.readline()
        # file
        loc_file.update({var:fid_m})
        loc_file.update({var+rms:fid_r})
        # data
        loc_data.update({var:[]})
        loc_data.update({var+rms:[]})
    # make the initial values
    for i in range(bin_num):
        # it is firstly used to store the point count
        for var in loc_data.keys():
            loc_data[var].append(0.0)
    data_names=loc_data.keys()
    data_names.remove('r')
    # read in and calculate the sum
    for i in range(line_num):
        for var in data_names:
            line=loc_file[var].readline()
            line=line.strip()
            [x, y, z, data]=line.split()
            # data of radius
            if var is data_names[0]:
                #calculate the nondimensional radius
                r=math.sqrt(float(x)**2+float(y)**2)/float(z)
            if r < rx_limit:
                r_idx=int(r//bin_size)
                # to be divided by the number of vars
                loc_data['r'][r_idx]+=1
                loc_data[var][r_idx]+=float(data)
    # calculate the average
    for i in range(bin_num-1,-1,-1):
        loc_data['r'][i]/=len(data_names)
        if loc_data['r'][i] != 0:
            for var in data_names:
                loc_data[var][i]/=loc_data['r'][i]
            loc_data['r'][i]=float(i)*bin_size+bin_size/2.0
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

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)
