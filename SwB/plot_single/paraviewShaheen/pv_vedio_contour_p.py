"""
Zhen Lu 2018
make video with iso-contour of pressure
"""
#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
swBfoam = OpenFOAMReader(FileName='SwB.foam')
swBfoam.MeshRegions = ['internalMesh']
swBfoam.CellArrays = ['T', 'p']
swBfoam.CaseType = 'Decomposed Case'

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# default ppi in paraview is 96
renderView1.ViewSize = [1800, 1800]
# Turn off the small axes
renderView1.OrientationAxesVisibility = 0
# Set background color as white
renderView1.Background = [1.0, 1.0, 1.0]

######################################################################

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
clip3.ClipType.Radius = 0.04

# make pressure contour
contour1 = Contour(Input=clip3)
contour1.ContourBy = ['POINTS', 'p']
contour1.Isosurfaces = [101290.]
contour1.PointMergeMethod = 'Uniform Binning'

######################################################################

# show data in view
contour1Display = Show(contour1, renderView1)
# trace defaults for the display properties.
contour1Display.Representation = 'Surface'
contour1Display.ColorArrayName = [None, 'T']
contour1Display.SetScaleArray = ['POINTS', 'T']
contour1Display.ScaleTransferFunction = 'PiecewiseFunction'
contour1Display.OpacityArray = ['POINTS', 'T']
contour1Display.OpacityTransferFunction = 'PiecewiseFunction'

# set scalar coloring
ColorBy(contour1Display, ('POINTS', 'T'))

# get color transfer function/color map for 'T'
tLUT = GetColorTransferFunction('T')
tLUT.RescaleTransferFunction(298., 2200.)
tLUT.ApplyPreset('2hot', True)

# create a new 'OpenFOAMReader'
swBWall = OpenFOAMReader(FileName='SwB.foam')
swBWall.MeshRegions = ['WALL_TUBE_LOW_OUT', 'WALL_QUARL_IN', 'WALL_TUBE_UP']
swBWall.CellArrays = []
swBWall.CaseType = 'Decomposed Case'

# show data in view
swBWallDisplay = Show(swBWall, renderView1)
# trace defaults for the display properties.
swBWallDisplay.Representation = 'Surface'
swBWallDisplay.ColorArrayName = [None, '']

# set scalar coloring
ColorBy(swBWallDisplay, ('FIELD', 'casePath'))

# Properties modified
swBWallDisplay.Opacity = 0.2

# get color legend/bar for tLUT in view renderView1
tLUTColorBar = GetScalarBar(tLUT, renderView1)

tLUTColorBar.WindowLocation = 'UpperLeftCorner'
# remove up and low range labels with different format
tLUTColorBar.AddRangeLabels = 0

tLUTColorBar.ScalarBarLength = 0.5
tLUTColorBar.ScalarBarThickness = 48

tLUTColorBar.UseCustomLabels = 1
tLUTColorBar.CustomLabels = [300., 600., 900., 1200., 1500., 1800., 2100.]
tLUTColorBar.AutomaticLabelFormat = 1
#tLUTColorBar.LabelFormat = '%-#4.0f'

tLUTColorBar.Title = 'T (K)'
tLUTColorBar.ComponentTitle = ''
tLUTColorBar.TitleFontSize = 60
tLUTColorBar.TitleFontFamily = 'Times'
tLUTColorBar.TitleColor = [0.0, 0.0, 0.0]

tLUTColorBar.LabelFontSize = 60
tLUTColorBar.LabelFontFamily = 'Times'
tLUTColorBar.LabelColor = [0.0, 0.0, 0.0]

# create a new 'Annotate Time Filter'
annotateTimeFilter1 = AnnotateTimeFilter(Input=clip3)

# Properties modified on annotateTimeFilter1
annotateTimeFilter1.Format = 'Time: %.4f s'

# Properties modified on annotateTimeFilter1
annotateTimeFilter1.Shift = -1.4002

# Properties modified on annotateTimeFilter1
annotateTimeFilter1.Scale = 1.0

# show data in view
annotateTimeFilter1Display = Show(annotateTimeFilter1, renderView1)

# Properties modified on annotateTimeFilter1Display
annotateTimeFilter1Display.Color = [0.0, 0.0, 0.0]

# Properties modified on annotateTimeFilter1Display
annotateTimeFilter1Display.FontSize = 48

# Properties modified on annotateTimeFilter1Display
#annotateTimeFilter1Display.WindowLocation = 'UpperCenter'
annotateTimeFilter1Display.WindowLocation = 'LowerRightCorner'

# camera placement for renderView1
renderView1.CameraPosition = [-0.08, 0.0, 0.07]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.05]
renderView1.CameraViewUp = [0.0, 1.0, 1.0]
renderView1.CameraViewAngle = 75

#SaveScreenshot('fig_p.png', 
#               renderView1, 
#               ImageResolution=[1800, 1800], 
#               OverrideColorPalette='WhiteBackground')
#
#save animation
SaveAnimation('vedio_p.png', 
              renderView1,
              ImageResolution=[1800, 1800],
              OverrideColorPalette='WhiteBackground',
              FrameRate=24,
              FrameWindow=[0, 499])
