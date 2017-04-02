# Zhen Lu, 2017 <albert.lz07@gmail.com>
import csv

# read the csv file in default format, return dict data
def csv_read(filename):
    file_data={}
    with open(filename,'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        var_names = csvreader.next()
        for var in var_names:
            file_data.update({var:[]})
        for row in csvreader:
            for i in range(len(row)):
                file_data[var_names[i]].append(float(row[i]))
    return file_data

# cm inch transfer for matplotlib
def cm2inch(*tupl):
    inch = 2.54
    return tuple(i/inch for i in tupl)
