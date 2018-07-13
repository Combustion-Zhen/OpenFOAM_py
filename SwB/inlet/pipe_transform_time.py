"""
Zhen Lu, 04/05/2017, <albert.lz07@gmail.com>

Transform the x-direction pipe flow calculation for OpenFOAM inlet
boundary condition timeVaryingMappedFixedValue

System argument should be the start time of the pipe flow, say 0.01

Variables in the python script to be changed based on user's need:
    flow_direct     direction of flow x: +/- 1 y: +/- 2 z: +/- 3
    flow_base_point location of the inlet boundary condition at the
                    direction of flow_direct
    bulk_vel        bulk velocity, same as Ubar
    patch_dir       patch name for the inlet boundary condition
    sim_time        physical time for simulation
    dt              time step between each mapping plane
"""

import os
import sys
import glob
import numpy as np
import file_read as fr

# direction of flow x: +/- 1 y: +/- 2 z: +/- 3
flow_direct = 3
bulk_vel = 21.96
patch_dir = 'fuel/'
sim_time = 0.1
center_loc = [0.0, 0.0, 0.0]
dt = 1e-5

if len(sys.argv) < 2:
    raise RuntimeError('Please provide start_time')

start_time = float(sys.argv[1])

# get the latest time
calc_time=[]
for file_name in glob.glob('[0-9]*[0-9]'):
    time = float(file_name)
    if time >= start_time:
        calc_time.append(time)
calc_time.sort()

print('Taking pipe flow simulation results '
      'from {0} s to {1:g} s '.format(sys.argv[1],calc_time[-1]))
print('to construct timeVaryingMappedFixedValue '
        'from 0.0 s to {0:g} s '.format(sim_time))

# read the cell center information
x = fr.comp_read_scalar('{:g}/ccx'.format(calc_time[-1]))
y = fr.comp_read_scalar('{:g}/ccy'.format(calc_time[-1]))
z = fr.comp_read_scalar('{:g}/ccz'.format(calc_time[-1]))

x_loc = list(set(x))
x_num = len(x_loc)
pts_num = int(len(x)/x_num)
vel_num = len(calc_time)*x_num
print(x_num,pts_num,vel_num)

# check the matching of points on each x location
for i in range(x_num):
    if (list(y[i*pts_num:(i+1)*pts_num]) != list(y[:pts_num])
        or list(z[i*pts_num:(i+1)*pts_num]) != list(z[:pts_num])):
        raise RuntimeError('Points does not match on each plane')

# axis information for transform
normal_dir = np.sign(flow_direct)
axis = -flow_direct-1 if flow_direct < 0 else flow_direct-1

# transform cordinates
pts = np.empty([pts_num,3])
pts[:,1] = y[:pts_num]
pts[:,2] = z[:pts_num]
pts[:,0] = pts[:,axis]
pts[:,axis] = 0.0

for j, loc in enumerate(center_loc):
    pts[:,j] = pts[:,j] + loc

# velocity
# read in all velocity information
vel = np.empty([vel_num,pts_num,3])
for j,time in enumerate(calc_time):
    v = fr.comp_read_vector('{:g}/U'.format(time),3)
    # disordered inlet
    #for i,pos in enumerate(x_loc):
    # ordered inlet
    for i,pos in enumerate(sorted(x_loc)):
        k = x_loc.index(pos)
        vel[j*x_num+i,:,:] = v[k*pts_num:(k+1)*pts_num,:]

# transform cordinate
vel[:,:,0], vel[:,:,axis] = vel[:,:,axis], vel[:,:,0].copy()*normal_dir

# output to patch name folder
fr._mkdir(patch_dir)

# comment line
str_comment = ' *'*30

# write points
file_name = '{}points'.format(patch_dir)
with open(file_name,'w') as foamfile:
    foamfile.write('FoamFile\n{\n'
                   '    version        2.0;\n'
                   '    format         ascii;\n'
                   '    class          vectorField;\n'
                   '    object         points;\n}\n')
    foamfile.write('//' + str_comment + ' //\n')
    foamfile.write('\n(\n')
    for i in range(pts_num):
        foamfile.write('(')
        foamfile.write(("{} "*len(pts[i,:]))[:-1].format(*pts[i,:]))
        foamfile.write(')\n')
    foamfile.write(')\n')
    foamfile.write('//' + str_comment + ' //\n')

# write velocity
vel_ave = np.zeros(3)
vel_ave[axis] = normal_dir*bulk_vel
time_series = np.append(np.arange(0,sim_time,dt),sim_time)
for j,time in enumerate(time_series):
    i = j % vel_num

    fr._mkdir('{0}{1:g}'.format(patch_dir,time))
    file_name = '{0}{1:g}/U'.format(patch_dir,time)

    with open(file_name,'w') as foamfile:
        foamfile.write('FoamFile\n{\n'
                       '    version        2.0;\n'
                       '    format         ascii;\n'
                       '    class          vectorAverageField;\n'
                       '    object         values;\n}\n')
        foamfile.write('//' + str_comment + ' //\n')

        foamfile.write('(')
        foamfile.write(("{} "*len(vel_ave))[:-1].format(*vel_ave))
        foamfile.write(')\n')

        foamfile.write(str(pts_num))

        foamfile.write('\n(\n')
        for k in range(pts_num):
            foamfile.write('(')
            foamfile.write(("{} "*len(vel[i,k,:]))[:-1]
                            .format(*vel[i,k,:]))
            foamfile.write(')\n')
        foamfile.write(')\n')

        foamfile.write('//' + str_comment + ' //\n')
