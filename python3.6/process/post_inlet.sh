#!/bin/bash

STARTTIME=0.01
SIMTIME=0.3

sed -e "s/@STARTFROM@/latestTime/g" -e "s/@STARTTIME@/0.0/g" \
    -e "s/@ENDTIME@/0.005/g" -e "s/@DELTAT@/1e-6/g" \
    -e "s/@WRITEINTERVAL@/1000/g" -e "s/@WRITEFORMAT@/ascii/g" \
    -e "s/@AVE_ENABLED@/false/g" -e "s/@SAMPLE_ENABLED@/false/g" \
    system/controlDict_template > system/controlDict

reconstructPar -time "$STARTTIME:"
writeCellCentres -latestTime

python pipe_transform_time.py $STARTTIME $SIMTIME
