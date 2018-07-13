"""

Zhen Lu 2018/07/09

plot contour of the swirl burner

domain: z from -60 mm to 120 mm, radius 50 mm

"""

#### import the simple module from the paraview
from paraview.simple import *
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

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# camera placement for renderView1
renderView1.CameraPosition = [-0.09, 0.0, 0.03]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.03]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraViewAngle = 90

###############################################################################

# get color transfer function/color map for 'T'
tLUT = GetColorTransferFunction('T')

# Rescale transfer function
tLUT.RescaleTransferFunction(298.0, 2200.0)

# show data in view
slice1Display = Show(slice1, renderView1)
# display properties
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'T']
slice1Display.LookupTable = tLUT

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color legend/bar for tLUT in view renderView1
tLUTColorBar = GetScalarBar(tLUT, renderView1)
tLUTColorBar.WindowLocation = 'LowerRightCorner'
# remove up and low range labels with different format
tLUTColorBar.AddRangeLabels = 0

tLUTColorBar.ScalarBarLength = 0.3
tLUTColorBar.ScalarBarThickness = 48

tLUTColorBar.UseCustomLabels = 1
tLUTColorBar.CustomLabels = [300,600,900,1200,1500,1800,2100]

tLUTColorBar.Title = '$\\tilde{T}$'
tLUTColorBar.TitleFontSize = 48
tLUTColorBar.TitleFontFamily = 'Times'
tLUTColorBar.TitleColor = [0.0, 0.0, 0.0]

tLUTColorBar.LabelFontSize = 48
tLUTColorBar.LabelFontFamily = 'Times'
tLUTColorBar.LabelColor = [0.0, 0.0, 0.0]

# save
SaveScreenshot('snapshot_T.jpg',
               renderView1,
               ImageResolution=[900, 1800],
               OverrideColorPalette='WhiteBackground')

SaveScreenshot('snapshot_T.png',
               renderView1,
               ImageResolution=[900, 1800],
               OverrideColorPalette='WhiteBackground')
