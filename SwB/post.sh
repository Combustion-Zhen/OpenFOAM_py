#!/bin/sh
TIME=-latestTime
SAMPLEDICT="axial xaxis xD xnormal"
## convert from binary format to ascii
sed -e "s/@STARTTIME@/latestTime/g" -e "s/@ENDTIME@/0.25/g" \
    -e "s/@DELTAT@/1e-6/g" -e "s/@WRITEINTERVAL@/0.01/g" \
    -e "s/@WRITEFORMAT@/ascii/g" \
    -e "s/@ENABLED@/true/g" \
    -e "s/@RESTART@/false/g" -e "s/@RESTARTOUT@/false/g" \
    system/controlDict_template > system/controlDict
### reconstruct from the parallel resutls
#reconstructPar $TIME
## get the cell coordinates
writeCellCentres $TIME
## flameletFoam reconstruction of the fields
flameletFoamPost $TIME -fields '(CH4 O2 H2O CO2 CO OH H2 NO)'
## sample the results
cp $HOME/$WM_PROJECT/OpenFOAM_py/sampleDict_SwB/sampleDict* system/
for i in $SAMPLEDICT
do
    sample $TIME -dict system/sampleDict_$i
done
### copy the python post-processing scripts
#cd postProcessing
#cp $HOME/$WM_PROJECT/py_scripts/python3.6/file_read.py .
#cp $HOME/$WM_PROJECT/py_scripts/python3.6/process/radial* .
#cp $HOME/$WM_PROJECT/py_scripts/python3.6/process/field* .
#cp $HOME/$WM_PROJECT/py_scripts/python3.6/plot_single/* .
### with python3 alias as py
#python3 radial_mean_digit.py
#python3 radial_mean_U.py
#python3 radial_cnd_scat.py
#python3 field_inst.py
#python3 field_mean.py
#python3 plot_radial_mean.py
#python3 plot_radial_mean_U.py
#python3 plot_radial_mean_U_up.py
#python3 plot_cond.py
#python3 plot_scat.py
#python3 plot_field.py
#python3 plot_axial.py
