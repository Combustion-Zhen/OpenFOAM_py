"""
Zhen Lu, 03/05/2017, <albert.lz07@gmail.com>

Transform the x-direction pipe flow calculation for OpenFOAM inlet
boundary condition timeVaryingMappedFixedValue
"""

import glob
import numpy as np
import file_read as fr

# direction of flow x: +/- 1 y: +/- 2 z: +/- 3
flow_direct = 3
flow_base_point = 0.0

patch_dir = 'inlet_jet/'
data_dir = 'surfaces/'
data_loc = 'xD02/'

calc_time = []
for file_name in glob.glob('{}*'.format(data_dir)):
    calc_time.append(float(file_name[len(data_dir):]))
# only take one time now
time = str(max(calc_time))

# file for points
file_name = '{0}{1}/{2}points'.format(data_dir,time,data_loc)
points = fr.foam_read_vector(file_name,3)

# file for velocity
file_name = '{0}{1}/{2}/vectorField/U'.format(data_dir,time,data_loc)
velo = fr.foam_read_vector(file_name,3)

# transform axis
normal_dir = np.sign(flow_direct)
axis = -flow_direct-1 if flow_direct < 0 else flow_direct-1

points[:,0] = points[:,flow_direct-1]
points[:,flow_direct-1] = flow_base_point

velo[:,0], velo[:,axis] = velo[:,axis], velo[:,0].copy()*normal_dir

# write points
fr._mkdir(patch_dir)
file_name = '{}points'.format(patch_dir)
fr.foam_write_vector(file_name,'points',points)

# write velocity
fr._mkdir('{0}{1}'.format(patch_dir,'0'))
file_name = '{0}{1}/U'.format(patch_dir,'0')
fr.foam_write_vector(file_name,'values',velo)
