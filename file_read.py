# Zhen Lu, 2017 <albert.lz07@gmail.com>
import csv

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)

# read the csv file in default format, return dict data
def csv_read(filename):
    file_data={}
    with open(filename,'r') as csvfile:
        csvreader = csv.reader(csvfile)
        var_names = csvreader.next()
        for var in var_names:
            file_data.update({var:[]})
        for row in csvreader:
            for i in range(len(row)):
                file_data[var_names[i]].append(float(row[i]))
    return file_data

# read the experimental results of Sandia Flames
# input:
#   flame   D/E/F.stat/scat
#   xD      location 075/15/30/45
#   data_type   ave/fav/all/cnd
def SF_read(flame,xD,data_type):
    expr={}
    filename='../../../pmCDEFarchives/pm{0}/D{1}.Y{2}'.format(flame,xD,data_type)
    if data_type == 'cnd':
        head = 2
    else:
        head = 3
    with open(filename,'r') as file_exp:
        for i in range(head):
            file_exp.readline()
        #read in variable names
        var_names = file_exp.readline().strip().split()
        for i in range(len(var_names)):
            # use r for simplicity
            if var_names[i] == 'r/d':
                var_names[i] = 'r'
            # remove the unit for T
            elif var_names[i] == 'T(K)' or var_names[i] == 'Tray':
                var_names[i] = 'T'
            # using Z for mixture fraction, replace F
            elif var_names[i][0] == 'F':
                var_names[i] = 'Z'+var_names[i][1:]
            # remove Y before species
            elif var_names[i][0] == 'Y':
                var_names[i] = var_names[i][1:]
            # for duplicates like CO
            if var_names[i] in var_names[:i]:
                var_names[i] += '_'
            expr.update({var_names[i]:[]})
        for line in file_exp:
            exp_data=line.strip().split()
            for i in range(len(var_names)):
                expr[var_names[i]].append(float(exp_data[i]))
    return expr
