"""
Zhen Lu 2018/07/12

python script to call paraview for sampling
"""
import numpy as np
import math
import os
#### import the simple module from the paraview
from paraview.simple import *

# output directory
OUTDIR='sample_lines'

if not os.path.exists(OUTDIR):
    os.makedirs(OUTDIR)

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
swBfoam = OpenFOAMReader(FileName='SwB.foam')
swBfoam.MeshRegions = ['internalMesh']
swBfoam.CellArrays = ['CH4Mean', 'CH4Prime2Mean',
                      'CO2Mean', 'CO2Prime2Mean', 
                      'O2Mean', 'O2Prime2Mean', 
                      'OHMean', 'OHPrime2Mean', 
                      'TMean', 'TPrime2Mean', 
                      'UMean', 'UPrime2Mean', 
                      'ZMean', 'ZPrime2Mean', 
                      'chiMean', 'chiPrime2Mean', 
                      'varZMean', 'varZPrime2Mean']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

###############################################################################

# create a new 'Clip' Cut the bottom
clip1 = Clip(Input=swBfoam)
clip1.ClipType = 'Plane'

# Properties modified on clip1.ClipType
clip1.ClipType.Origin = [0.0, 0.0, -0.05]
clip1.ClipType.Normal = [0.0, 0.0, 1.0]

# create a new 'Clip' Cut the head
clip2 = Clip(Input=clip1)
clip2.ClipType = 'Plane'

# Properties modified on clip2.ClipType
clip2.ClipType.Origin = [0.0, 0.0, 0.12]
clip2.ClipType.Normal = [0.0, 0.0, -1.0]

# create a new 'Clip' Cylinder
clip3 = Clip(Input=clip2)
clip3.ClipType = 'Cylinder'
clip3.InsideOut = 1

# Properties modified on clip3.ClipType
clip3.ClipType.Axis = [0.0, 0.0, 1.0]
clip3.ClipType.Radius = 0.04

# Temporal Statistics
temporalStatistics1 = TemporalStatistics(Input=clip3)

# Properties modified on temporalStatistics1
temporalStatistics1.ComputeMinimum = 0
temporalStatistics1.ComputeMaximum = 0
temporalStatistics1.ComputeStandardDeviation = 0

###############################################################################

# get color tranfer function for 'T'
tLUT = GetColorTransferFunction('TMean_average')

# show data in view
temporalStatistics1Display = Show(temporalStatistics1, renderView1)
# display properties
temporalStatistics1Display.Representation = 'Surface'
temporalStatistics1Display.ColorArrayName = ['POINTS', 'TMean_average']
temporalStatistics1Display.LookupTable = tLUT

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(
        Input=temporalStatistics1,
        Source='High Resolution Line Source'
        )

plotOverLine1.Source.Resolution = 1000

loc = np.arange(-40,90,15)

for z in loc:
    if z < 0:
        r = 0.0135
    elif z < 40:
        r = 0.0135+z/1000.*math.sin(math.pi/9.)
    else:
        r = 0.04

    # Properties modified on plotOverLine1.Source
    plotOverLine1.Source.Point1 = [-r, 0.0, z/1000.]
    plotOverLine1.Source.Point2 = [r, 0.0, z/1000.]

    # save data
    SaveData('{0}/z{1:d}.csv'.format(OUTDIR,z), proxy=plotOverLine1)

# axial line
plotOverLine1.Source.Point1 = [0.0, 0.0, 0.]
plotOverLine1.Source.Point2 = [0.0, 0.0, 0.12]
plotOverLine1.Source.Resolution = 1000
SaveData('{}/axial.csv'.format(OUTDIR), proxy=plotOverLine1)
