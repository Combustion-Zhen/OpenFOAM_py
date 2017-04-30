#!/bin/sh
TIME=-latestTime
SAMPLEDICT="axial xD xnormal"
## reconstruct from the parallel resutls
reconstructPar $TIME
## convert from binary format to ascii
sed -e "s/@STARTTIME@/latestTime/g" -e "s/@ENDTIME@/0.25/g" \
    -e "s/@DELTAT@/1e-6/g" -e "s/@WRITEINTERVAL@/0.01/g" \
    -e "s/@WRITEFORMAT@/ascii/g" \
    -e "s/@ENABLED@/true/g" \
    -e "s/@RESTART@/false/g" -e "s/@RESTARTOUT@/false/g" \
    system/controlDict_template > system/controlDict
foamFormatConvert $TIME
## get the cell coordinates
writeCellCentres $TIME
## flameletFoam reconstruction of the fields
flameletFoamPost $TIME -fields '(CH4 O2 N2 H2O CO2 CO OH H2 NO)'
## sample the results
for i in $SAMPLEDICT
do
    sample $TIME -dict system/sampleDict_$i
done
## copy the python post-processing scripts
cd postProcessing
cp $HOME/$WM_PROJECT/py_scripts/python3.6/file_read.py .
cp $HOME/$WM_PROJECT/py_scripts/python3.6/process/* .
cp $HOME/$WM_PROJECT/py_scripts/python3.6/plot_single/* .
## with python3 alias as py
py radial_mean_digit.py
py radial_mean_U.py
py radial_cnd_scat.py
py field_inst.py
py field_mean.py
py plot_radial_mean.py
py plot_radial_mean_U.py
py plot_cond.py
py plot_scat.py
py plot_field.py
py plot_axial.py
