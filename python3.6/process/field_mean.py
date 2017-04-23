# Zhen Lu, 11/04/2017
# load and process flameletFoam results
# field mean
import glob
import math
import csv
from file_read import comp_read_scalar

# constant, diameter of the jet
D = 0.0072

# pick the latest time
calc_time=[]
for filename in glob.glob('../[0-9]*'):
    calc_time.append(float(filename[3:]))
time=str(max(calc_time))

# extract variable names
var_names=[]
foldername='../{t}/'.format(t=time)
filename_int_var='Mean'
filename_int_rms='Prime2Mean'
# variables
for filename in glob.glob('{0}*{1}'.format(foldername,filename_int_rms)):
    pos = filename.find(filename_int_rms)
    var_names.append(filename[len(foldername):pos])
# the velocity has three components, remove it at first
if 'U' in var_names:
    var_names.remove('U')

# load data
field_data={'r':[],'z':[]}
# load coordinate information
print('Reading coordinates')
x = comp_read_scalar('{0}ccx'.format(foldername))
y = comp_read_scalar('{0}ccy'.format(foldername))
z = comp_read_scalar('{0}ccz'.format(foldername))
rz=[]
for i in range(len(z)):
    r = math.sqrt(x[i]**2+y[i]**2)
    #round the coordinates
    field_data['r'].append(float('{0:.3g}'.format(r)))
    field_data['z'].append(float('{0:.3g}'.format(z[i])))
    rz.append((field_data['r'][i],field_data['z'][i]))
# check the number of r and z points
print(len(set(field_data['r'])))
print(len(set(field_data['z'])))
rz=list(set(rz))

field_mean={}
for loc in rz:
    field_mean.update({loc+('count',):0})
    for var in var_names:
        field_mean.update({loc+(var,):0.0})
        field_mean.update({loc+(var+'rms',):0.0})
# It should be 60 for Sandia Flame case with axisymmetric mesh
for i in range(len(z)):
    field_mean[(field_data['r'][i],field_data['z'][i],'count')]+=1
# read in data
for var in var_names:
    print('Reading avaraged data: {0}'.format(var))
    data_var=comp_read_scalar('{0}{1}{2}'.format(foldername,
                                                 var,
                                                 filename_int_var))
    data_rms=comp_read_scalar('{0}{1}{2}'.format(foldername,
                                                 var,
                                                 filename_int_rms))
    # sum
    for i in range(len(z)):
        field_mean[(field_data['r'][i],field_data['z'][i],var)]+=data_var[i]
        field_mean[(field_data['r'][i],field_data['z'][i],var+'rms')]+=data_rms[i]
    # average
    for loc in rz:
        field_mean[loc+(var,)]      /=float(field_mean[loc+('count',)])
        field_mean[loc+(var+'rms',)]/=float(field_mean[loc+('count',)])
        # garuantee it is large or equal to 0
        field_mean[loc+(var+'rms',)] =math.sqrt(max([field_mean[loc+(var+'rms',)],0.0]))

# write to csv file
with open('mean_field.csv','w') as csvfile:
    field_names=['r','z']
    for var in var_names:
        field_names.append(var)
        field_names.append(var+'rms')
    writer = csv.DictWriter(csvfile,fieldnames=field_names)
    writer.writeheader()
    for loc in rz:
        data_row={'r':'{:e}'.format(loc[0]/D),'z':'{:e}'.format(loc[1]/D)}
        for var in var_names:
            data_row.update({var:'{:e}'.format(field_mean[loc+(var,)])})
            data_row.update({var+'rms':'{:e}'.format(field_mean[loc+(var+'rms',)])})
        writer.writerow(data_row)
