"""
Zhen Lu, 11/04/2017, <albert.lz07@gmail.com>
modified 24/04/2017, making the r, z ordered
load and process flameletFoam results
field mean
"""
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
for filename in glob.glob('{0}*{1}'.format(foldername,
                                           filename_int_rms)):
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
for i in range(len(z)):
    r = math.sqrt(x[i]**2+y[i]**2)
    #round the coordinates
    field_data['r'].append(float('{0:.3g}'.format(r)))
    field_data['z'].append(float('{0:.3g}'.format(z[i])))
del x, y, z
# check the number of r and z points
rd=sorted(list(set(field_data['r'])))
xd=sorted(list(set(field_data['z'])))
print(len(rd))
print(len(xd))

field_mean={}
for z in xd:
    for r in rd:
        field_mean.update({(z,r,'count'):0})
        for var in var_names:
            field_mean.update({(z,r,var):0.0})
            field_mean.update({(z,r,var+'rms'):0.0})
# It should be 60 for Sandia Flame case with axisymmetric mesh
for i,z in enumerate(field_data['z']):
    field_mean[(z,field_data['r'][i],'count')]+=1
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
    for i,z in enumerate(field_data['z']):
        field_mean[(z,field_data['r'][i],var)]+=data_var[i]
        field_mean[(z,field_data['r'][i],var+'rms')]+=data_rms[i]
    # average
    for z in xd:
        for r in rd:
            field_mean[(z,r,var)] \
                /= float(field_mean[(z,r,'count')])
            field_mean[(z,r,var+'rms')] \
                /= float(field_mean[(z,r,'count')])
            # garuantee it is large or equal to 0
            field_mean[(z,r,var+'rms')] \
                = math.sqrt(max([field_mean[(z,r,var+'rms')],0.0]))

# write to csv file
with open('mean_field.csv','w') as csvfile:
    field_names=['r','z']
    for var in var_names:
        field_names.append(var)
        field_names.append(var+'rms')
    writer = csv.DictWriter(csvfile,fieldnames=field_names)
    writer.writeheader()
    for z in xd:
        for r in rd:
            data_row={'r':'{:e}'.format(r/D),'z':'{:e}'.format(z/D)}
            for var in var_names:
                data_row.update({var:
                    '{:e}'.format(field_mean[(z,r,var)])})
                data_row.update({var+'rms':
                    '{:e}'.format(field_mean[(z,r,var+'rms')])})
            writer.writerow(data_row)
