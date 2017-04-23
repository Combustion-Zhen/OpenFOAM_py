# OpenFOAM_py
scripts for post-processing of OpenFOAM (flameletFoam) results

Most scripts are for Sandia Flames. For journal artworks, you may need specific settings for different variables, such as ylabel, ylim. But it is easy to modify in the scripts.

Execution sequence:

copy post.sh to the case directory, and keep python scripts in OpenFOAM/py_scripts
./post.sh

folder_correct.py to round the folder names of those runtime save

add plot_multi to compare results from different settings

modify the way read in data, using numpy.genfromtxt

follow PEP8 convention
