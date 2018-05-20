"""
Zhen Lu 2018/02/09

sample at different time output
"""

import glob
import math
import os
#### import the simple module from the paraview
from paraview.simple import *

# output directory
OUTDIR='sample_t'

# start time for sampling
t_strt = 0.4

# get the time list
t_list = []

for folder in glob.glob('[0-9]*'):
    time = float(folder)
    t_list.append(time)

t_list.sort()
del t_list[0]

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
swBfoam = OpenFOAMReader(FileName='SwB.foam')
swBfoam.MeshRegions = ['internalMesh']
swBfoam.CellArrays = ['U', 'U_0', 'nuSgs', 'p']

# get animation scene
animationScene1 = GetAnimationScene()

# get data time step
animationScene1.UpdateAnimationUsingDataTimeSteps()

swBfoam.SkipZeroTime = 0

# go to the first time
animationScene1.GoToFirst()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# show data in view
swBfoamDisplay = Show(swBfoam, renderView1)

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(Input=swBfoam,
    Source='High Resolution Line Source')

# sampling locations
loc = [-350,-300,-250,-200,-150,-100,
       -80,-70,-60,-50,-30,-10,
       5,10,20,30,
       42,45,50,55,
       60,65,70,80,90]

for i in range(len(t_list)):
    time = t_list[i]
    # get the next time
    animationScene1.GoToNext()

    print(time,t_strt)
    if time < t_strt:
        continue

    # Properties modified
    swBfoam.CellArrays = ['T', 'U', 'Z', 'alphaSgs', 'chi', 'muSgs', 'p', 'rho', 'thermo:alpha', 'thermo:mu', 'thermo:psi', 'varZ', 'CH4Mean', 'CH4Prime2Mean', 'CO2Mean', 'CO2Prime2Mean', 'COMean', 'COPrime2Mean', 'H2Mean', 'H2OMean', 'H2OPrime2Mean', 'H2Prime2Mean', 'N2Mean', 'N2Prime2Mean', 'NOMean', 'NOPrime2Mean', 'O2Mean', 'O2Prime2Mean', 'OHMean', 'OHPrime2Mean', 'TMean', 'TPrime2Mean', 'UMean', 'UPrime2Mean', 'ZMean', 'ZPrime2Mean', 'chiMean', 'chiPrime2Mean', 'varZMean', 'varZPrime2Mean']

    # set the folder
    folder = '{0}{1:g}'.format(OUTDIR,time)
    if not os.path.exists(folder):
        os.makedirs(folder)

    # axial line
    plotOverLine1.Source.Point1 = [0.0, 0.0, 0.]
    plotOverLine1.Source.Point2 = [0.0, 0.0, 0.12]
    plotOverLine1.Source.Resolution = 1000
    SaveData('{}/axial.csv'.format(folder), proxy=plotOverLine1)
    
    for z in loc:
        if z < 0:
            r = 0.0135
        elif z < 40:
            r = 0.0135+z/1000.*math.sin(math.pi/12.)
        else:
            r = 0.06

        # Properties modified on plotOverLine1.Source
        plotOverLine1.Source.Point1 = [-r, 0.0, z/1000.]
        plotOverLine1.Source.Point2 = [r, 0.0, z/1000.]
        plotOverLine1.Source.Resolution = 1000

        # save data
        SaveData('{0}/z{1:d}.csv'.format(folder,z), proxy=plotOverLine1)
