# Zhen Lu, 12/04/2017
# load and process flameletFoam results
# instantaneous field
import glob
import math
import csv

# print task
print('Process the instantaneous snapshot')
# constant, diameter of the jet
D           = 0.0072
r_criterion = 1.0e-6

# pick the latest time
calc_time=[]
for filename in glob.glob('../[0-9]*[0-9]'):
    calc_time.append(float(filename[3:]))
time=str(max(calc_time))

# extract variable names
var_names=[]
# transfer instantaneous data to csv file
foldername      ='surfaces/{t}/'.format(t=time)
filename_inst   ='_xnormal.raw'
# variables
for filename in glob.glob('{0}*{1}'.format(foldername,filename_inst)):
    if 'Mean' not in filename:
        pos = filename.find(filename_inst)
        var_names.append(filename[len(foldername):pos])
# the velocity has three components, remove it at first
if 'U' in var_names:
    var_names.remove('U')

field_inst      ={'r':[],'z':[]}
for var in var_names:
    field_inst.update({var:[]})
    filename = '{0}{1}{2}'.format(foldername,var,filename_inst)
    print('Reading instantanous data: {0}'.format(var))
    with open(filename,'r') as fid:
        #read two head lines
        fid.readline()
        fid.readline()
        for line in fid:
            line_data = line.strip().split()
            r = float('{:.3g}'.format(float(line_data[1])))
            if abs(r) > r_criterion:
                field_inst[var].append(float(line_data[3]))
                if var is var_names[0]:
                    z = float('{:.3g}'.format(float(line_data[2])))
                    field_inst['r'].append(r/D)
                    field_inst['z'].append(z/D)
# check the number of r and z points
print(len(set(field_inst['r'])))
print(len(set(field_inst['z'])))

# write to csv
with open('inst_field.csv','w') as csvfile:
    writer = csv.DictWriter(csvfile,fieldnames=field_inst.keys())
    writer.writeheader()
    for i in range(len(field_inst['r'])):
        data_row={};
        for var in field_inst.keys():
            data_row.update({var:'{:e}'.format(field_inst[var][i])})
        writer.writerow(data_row)
