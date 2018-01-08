# Zhen Lu, 04/04/2014, <albert.lz07@gmail.com>
# correct the folder name in processor folders
# change the latest time folder
import glob
import os

file_dict={}
for file_name in glob.glob('processor0/0.*'):
    calc_time=file_name[11:]
    file_time=str('{0:.3g}'.format(float(calc_time)))
    if calc_time != file_time:
        file_dict.update({calc_time:file_time})
print(file_dict)

for folder_name in glob.glob('processor*'):
    print(folder_name)
    os.chdir(folder_name)
    for subfolder in file_dict.keys():
        os.rename(subfolder,file_dict[subfolder])
    os.chdir('..')
