# Zhen Lu, 2017 <albert.lz07@gmail.com>
import csv
import numpy as np

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)

# read the experimental results of Sandia Flames
def sf_expr_read(filename):
    data_type = filename[-3:]
    head = 2 if data_type == 'cnd' else 3
    data = np.genfromtxt(filename,skip_header=head,names=True)
    names = list(data.dtype.names)
    for i in range(len(names)):
        # use r for simplicity
        if names[i] == 'rd':
            names[i] = 'r'
        # remove the unit for T
        elif names[i] == 'TK' or names[i] == 'Tray':
            names[i] = 'T'
        # using Z for mixture fraction, replace F
        elif names[i][0] == 'F':
            names[i] = 'Z'+names[i][1:]
            if names[i] == 'Zmass':
                names[i] = 'Z'
        # remove Y before species
        elif names[i][0] == 'Y':
            names[i] = names[i][1:]
    data.dtype.names = tuple(names)
    return data

def comp_read_scalar(filename):
    data=[]
    with open(filename,'r') as file_OF:
        line=''
        while 'internalField' not in line:
            #skip head lines
            line=file_OF.readline().strip()
        num_data=int(file_OF.readline().strip())
        file_OF.readline()
        for i in range(num_data):
            data.append(float(file_OF.readline().strip()))
    return data

def z_str_to_num(xD):
    return float('{0}.{1}'.format(xD[:2],xD[2:]))
