"""

Zhen Lu 2018/07/09

plot instantaneous scalar contour of the swirl burner

domain: z from -60 mm to 120 mm, radius 50 mm

"""
#### import the simple module from the paraview
from paraview.simple import *
import numpy as np

varNames = {'TMean' : '$\langle\\tilde{T}\\rangle\;(\mathrm{K})$',
            'ZMean' : '$\langle\\tilde{Z}\\rangle$',
            'OHMean' : '$\langle\\tilde{Y}_{\mathrm{OH}}\\rangle$'
           }
varRanges = {'TMean' : [298, 2200],
             'ZMean' : [0, 1],
             'OHMean' : [0, 0.003]
            }
varLabels = {'TMean' : np.linspace(300,2100,num=7),
             'ZMean' : np.linspace(0,1,num=6),
             'OHMean' : np.linspace(0,0.003,num=4)
            }
varAutoLabelFormat = {'TMean' : 1,
                      'ZMean' : 0,
                      'OHMean' : 0
                     }
varLabelFormat = {'TMean' : '%-#4.0f',
                  'ZMean' : '%-#0.1f',
                  'OHMean' : '%-#0.3f'
                 }

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
swBfoam = OpenFOAMReader(FileName='./SwB.foam')
swBfoam.MeshRegions = ['internalMesh']
swBfoam.CellArrays = ['TMean', 'ZMean', 'OHMean']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# view size
# default ppi in paraview is 96
renderView1.ViewSize = [900, 1800]
# Turn off the small axes
renderView1.OrientationAxesVisibility = 0
# Set background color as white
renderView1.Background = [1.0, 1.0, 1.0]

###############################################################################

# create a new 'Clip' Cut the bottom
clip1 = Clip(Input=swBfoam)
clip1.ClipType = 'Plane'

# Properties modified on clip1.ClipType
clip1.ClipType.Origin = [0.0, 0.0, -0.06]
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
clip3.ClipType.Radius = 0.05

# create a new 'Slice'
slice1 = Slice(Input=clip3)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.0, 0.0, 0.0]
slice1.SliceType.Normal = [1.0, 0.0, 0.0]

# Temporal Statistics
temporalStatistics1 = TemporalStatistics(Input=slice1)

# Properties modified on temporalStatistics1
temporalStatistics1.ComputeMinimum = 0
temporalStatistics1.ComputeMaximum = 0
temporalStatistics1.ComputeStandardDeviation = 0

# contour of Zst
contour1  = Contour(Input=temporalStatistics1)
contour1.ContourBy = ['POINTS', 'ZMean_average']
contour1.Isosurfaces = [0.055]

# camera placement for renderView1
renderView1.CameraPosition = [-0.09, 0.0, 0.03]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.03]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraViewAngle = 90

###############################################################################

# get color transfer function/color map for 'T'
varLUT = GetColorTransferFunction('TMean_average')

# show data in view
temporalStatistics1Display = Show(temporalStatistics1, renderView1)
# display properties
temporalStatistics1Display.Representation = 'Surface'
temporalStatistics1Display.ColorArrayName = ['POINTS', 'TMean_average']
temporalStatistics1Display.LookupTable = varLUT

# show contour
contour1Display = Show(contour1, renderView1)
contour1Display.Representation = 'Surface'
contour1Display.ColorArrayName = [None,'']
# contour line color and width
contour1Display.DiffuseColor = [0.0, 0.0, 0.0]
contour1Display.LineWidth = 4.0

for k, v in varNames.items():
    varName = '{}_average'.format(k)
    # set scalar coloring
    ColorBy(temporalStatistics1Display, ('POINTS', varName))

    # Hide previous colorbar
    HideScalarBarIfNotNeeded(varLUT, renderView1)

    varLUT = GetColorTransferFunction(varName)
    varLUT.RescaleTransferFunction(varRanges[k][0], varRanges[k][1])

    # show color bar/color legend
    temporalStatistics1Display.SetScalarBarVisibility(renderView1, True)

    # get color legend/bar for varLUT in view renderView1
    varLUTColorBar = GetScalarBar(varLUT, renderView1)
    varLUTColorBar.WindowLocation = 'LowerRightCorner'
    # remove up and low range labels with different format
    varLUTColorBar.AddRangeLabels = 0

    varLUTColorBar.ScalarBarLength = 0.3
    varLUTColorBar.ScalarBarThickness = 48

    varLUTColorBar.UseCustomLabels = 1
    varLUTColorBar.CustomLabels = varLabels[k]
    varLUTColorBar.AutomaticLabelFormat = varAutoLabelFormat[k]
    varLUTColorBar.LabelFormat = varLabelFormat[k]

    varLUTColorBar.Title = v
    varLUTColorBar.TitleFontSize = 48
    varLUTColorBar.TitleFontFamily = 'Times'
    varLUTColorBar.TitleColor = [0.0, 0.0, 0.0]

    varLUTColorBar.LabelFontSize = 48
    varLUTColorBar.LabelFontFamily = 'Times'
    varLUTColorBar.LabelColor = [0.0, 0.0, 0.0]

    # save
    SaveScreenshot('fig_contour_{}.jpg'.format(k),
                   renderView1,
                   ImageResolution=[900, 1800],
                   OverrideColorPalette='WhiteBackground')

    SaveScreenshot('fig_contour_{}.png'.format(k),
                   renderView1,
                   ImageResolution=[900, 1800],
                   OverrideColorPalette='WhiteBackground')

