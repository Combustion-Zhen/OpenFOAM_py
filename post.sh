#!/bin/sh
TIME=-latestTime
SAMPLEDICT="xD xnormal"
## reconstruct from the parallel resutls
reconstructPar $TIME
## convert from binary format to ascii
sed  -e "s/@STARTTIME@/latestTime/g" -e "s/@ENDTIME@/0.25/g"   -e "s/@DELTAT@/1e-6/g" -e  "s/@WRITEINTERVAL@/0.01/g" -e "s/@ENABLED@/true/g"  -e "s/@RESTART@/false/g" -e "s/@RESTARTOUT@/false/g" -e "s/@WRITEFORMAT@/ascii/g" system/controlDict_template > system/controlDict
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
cp ~/OpenFOAM/py_scripts/* .
python radial_mean_digit.py
python radial_cnd_scat.py
python field_inst.py
python field_mean.py
python plot_radial_mean.py
python plot_cond.py
python plot_scat.py
python plot_field.py
