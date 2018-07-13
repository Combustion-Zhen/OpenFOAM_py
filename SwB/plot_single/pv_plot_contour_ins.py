"""

Zhen Lu 2018/07/09

plot instantaneous scalar contour of the swirl burner

domain: z from -60 mm to 120 mm, radius 50 mm

"""
#### import the simple module from the paraview
from paraview.simple import *
import numpy as np

varNames = {'T' : '$\\tilde{T}\;(\mathrm{K})$',
            'Z' : '$\\tilde{Z}$',
            'OH' : '$\\tilde{Y}_{\mathrm{OH}}$'
           }
varRanges = {'T' : [298, 2200],
             'Z' : [0, 1],
             'OH' : [0, 0.003]
            }
varLabels = {'T' : np.linspace(300,2100,num=7),
             'Z' : np.linspace(0,1,num=6),
             'OH' : np.linspace(0,0.003,num=4)
            }
varAutoLabelFormat = {'T' : 1,
                      'Z' : 0,
                      'OH' : 0
                     }
varLabelFormat = {'T' : '%-#4.0f',
                  'Z' : '%-#0.1f',
                  'OH' : '%-#0.3f'
                 }

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
swBfoam = OpenFOAMReader(FileName='./SwB.foam')
swBfoam.MeshRegions = ['internalMesh']
swBfoam.CellArrays = ['T', 'Z', 'OH']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# start at 0.4, plot 0.7
animationScene1.GoToNext()
animationScene1.GoToNext()
animationScene1.GoToNext()

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

# contour of Zst
contour1  = Contour(Input=slice1)
contour1.ContourBy = ['POINTS', 'Z']
contour1.Isosurfaces = [0.055]

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# camera placement for renderView1
renderView1.CameraPosition = [-0.09, 0.0, 0.03]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.03]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraViewAngle = 90

###############################################################################

# get color transfer function/color map for 'T'
varLUT = GetColorTransferFunction('T')

## Rescale transfer function
#tLUT.RescaleTransferFunction(298.0, 2200.0)
#
# show data in view
slice1Display = Show(slice1, renderView1)
# display properties
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'T']
slice1Display.LookupTable = varLUT

## show contour
#contour1Display = Show(contour1, renderView1)
#contour1Display.Representation = 'Surface'
#contour1Display.ColorArrayName = [None,'']
## contour line color and width
#contour1Display.DiffuseColor = [0.0, 0.0, 0.0]
#contour1Display.LineWidth = 4.0

for k, v in varNames.items():
    # set scalar coloring
    ColorBy(slice1Display, ('POINTS', k))

    # Hide previous colorbar
    HideScalarBarIfNotNeeded(varLUT, renderView1)

    varLUT = GetColorTransferFunction(k)
    varLUT.RescaleTransferFunction(varRanges[k][0], varRanges[k][1])

    # show color bar/color legend
    slice1Display.SetScalarBarVisibility(renderView1, True)

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
