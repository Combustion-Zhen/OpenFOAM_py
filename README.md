# OpenFOAM_py
scripts for post-processing of OpenFOAM (flameletFoam) results

Most scripts are for Sandia Flames. For journal artworks, you may need specific settings for different variables, such as ylabel, ylim. But it is easy to modify in the scripts.

Execution sequence:

reconstructPar
flameletFoamPost
sample
python radial_mean.py / radial_cnd_scat.py
python plot_radial_mean.py / plot_cond.py / plot_scat.py
