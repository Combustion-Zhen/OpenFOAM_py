"""
Zhen Lu 2018/01/29

python script to call paraview for sampling
"""
import math
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
swBfoam = OpenFOAMReader(FileName='SwB.foam')
swBfoam.MeshRegions = ['internalMesh']
swBfoam.CellArrays = ['U', 'U_0', 'nuSgs', 'p']

# get animation scene
animationScene1 = GetAnimationScene()

animationScene1.GoToLast()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [3248, 1905]

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# show data in view
swBfoamDisplay = Show(swBfoam, renderView1)

# Properties modified on swBd_L400_20M_FLAMELET_Bulk_SFCDfoam
swBfoam.CellArrays = ['T', 'U', 'Z', 'alphaSgs', 'chi', 'muSgs', 'p', 'rho', 'thermo:alpha', 'thermo:mu', 'thermo:psi', 'varZ', 'CH4Mean', 'CH4Prime2Mean', 'CO2Mean', 'CO2Prime2Mean', 'COMean', 'COPrime2Mean', 'H2Mean', 'H2OMean', 'H2OPrime2Mean', 'H2Prime2Mean', 'N2Mean', 'N2Prime2Mean', 'NOMean', 'NOPrime2Mean', 'O2Mean', 'O2Prime2Mean', 'OHMean', 'OHPrime2Mean', 'TMean', 'TPrime2Mean', 'UMean', 'UPrime2Mean', 'ZMean', 'ZPrime2Mean', 'chiMean', 'chiPrime2Mean', 'varZMean', 'varZPrime2Mean']

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(Input=swBfoam,
    Source='High Resolution Line Source')

loc = [-350,-300,-250,-200,-150,-100,
       -80,-70,-60,-50,-30,-10,
       5,10,20,30,
       42,45,50,55,
       60,65,70,80,90]

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

    # save data
    SaveData('sample_lines/z{:d}.csv'.format(z), proxy=plotOverLine1)

# axial line
plotOverLine1.Source.Point1 = [0.0, 0.0, 0.]
plotOverLine1.Source.Point2 = [0.0, 0.0, 0.12]
SaveData('sample_lines/axial.csv', proxy=plotOverLine1)
