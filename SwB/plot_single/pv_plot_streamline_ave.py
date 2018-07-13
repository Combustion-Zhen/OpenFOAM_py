"""

Zhen Lu 2018/07/12

plot instantaneous velocity streamlines for the swirl burner

domain: z from -60 mm to 120 mm, radius 50 mm

"""
#### import the simple module from the paraview
from paraview.simple import *
import numpy as np

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
swBfoam = OpenFOAMReader(FileName='./SwB.foam')
swBfoam.MeshRegions = ['internalMesh']
swBfoam.CellArrays = ['UMean']

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

# create a new 'Surface Vectors'
surfaceVectors1 = SurfaceVectors(Input=temporalStatistics1)
surfaceVectors1.SelectInputVectors = ['POINTS', 'UMean_average']

# create a new 'Mask Points'
maskPoints1 = MaskPoints(Input=surfaceVectors1)

# Properties modified on maskPoints1
maskPoints1.OnRatio = 50

# create a new 'Stream Tracer With Custom Source'
streamTracerWithCustomSource1 = StreamTracerWithCustomSource(
        Input=surfaceVectors1,
        SeedSource=maskPoints1)
streamTracerWithCustomSource1.Vectors = ['POINTS', 'UMean_average']
streamTracerWithCustomSource1.MaximumStreamlineLength = 0.18

# camera placement for renderView1
renderView1.CameraPosition = [-0.09, 0.0, 0.03]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.03]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraViewAngle = 90

###############################################################################

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('UMean_average')

# show data in view
streamTracerWithCustomSource1Display = Show(
        streamTracerWithCustomSource1,
        renderView1)
# trace defaults for the display properties.
streamTracerWithCustomSource1Display.Representation = 'Surface'
streamTracerWithCustomSource1Display.ColorArrayName = ['POINTS', 'UMean_average']
streamTracerWithCustomSource1Display.LookupTable = uLUT

# show color bar/color legend
streamTracerWithCustomSource1Display.SetScalarBarVisibility(renderView1, True)

# Apply a preset using its name. Note this may not work as expected when presets have duplicate names.
uLUT.ApplyPreset('jet', True)

# Rescale transfer function
uLUT.RescaleTransferFunction(0.0, 30.0)

# get color legend/bar for varLUT in view renderView1
uLUTColorBar = GetScalarBar(uLUT, renderView1)
uLUTColorBar.WindowLocation = 'LowerRightCorner'
# remove up and low range labels with different format
uLUTColorBar.AddRangeLabels = 0

uLUTColorBar.ScalarBarLength = 0.3
uLUTColorBar.ScalarBarThickness = 48

uLUTColorBar.UseCustomLabels = 1
uLUTColorBar.CustomLabels = np.linspace(0,30,num=7)

uLUTColorBar.Title = '$v\;(\mathrm{m/s})$'
uLUTColorBar.ComponentTitle = ''
uLUTColorBar.TitleFontSize = 48
uLUTColorBar.TitleFontFamily = 'Times'
uLUTColorBar.TitleColor = [0.0, 0.0, 0.0]

uLUTColorBar.LabelFontSize = 48
uLUTColorBar.LabelFontFamily = 'Times'
uLUTColorBar.LabelColor = [0.0, 0.0, 0.0]

# save
SaveScreenshot('fig_streamline_ave.jpg',
               renderView1,
               ImageResolution=[900, 1800],
               OverrideColorPalette='WhiteBackground')

SaveScreenshot('fig_streamline_ave.png',
               renderView1,
               ImageResolution=[900, 1800],
               OverrideColorPalette='WhiteBackground')
