#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
swBdfoam = OpenFOAMReader(FileName='./SwBd.foam')
swBdfoam.MeshRegions = ['internalMesh']
#swBdfoam.CellArrays = ['T', 'U', 'Z', 'alphaSgs', 'chi', 'muSgs', 'p', 'rho', 'thermo:alpha', 'thermo:mu', 'thermo:psi', 'varZ']
swBdfoam.CellArrays = ['T', 'U', 'Z', 'p']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

animationScene1.GoToLast()

# Properties modified on swBdfoam
swBdfoam.SkipZeroTime = 0

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
renderView1.ViewSize = [1200, 1800]

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')
pLUT.RGBPoints = [99228.6640625, 0.231373, 0.298039, 0.752941, 102824.83203125, 0.865003, 0.865003, 0.865003, 106421.0, 0.705882, 0.0156863, 0.14902]
pLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')
pPWF.Points = [99228.6640625, 0.0, 0.5, 0.0, 106421.0, 1.0, 0.5, 0.0]
pPWF.ScalarRangeInitialized = 1

# show data in view
swBdfoamDisplay = Show(swBdfoam, renderView1)
# trace defaults for the display properties.
swBdfoamDisplay.Representation = 'Surface'
swBdfoamDisplay.ColorArrayName = ['POINTS', 'p']
swBdfoamDisplay.LookupTable = pLUT
swBdfoamDisplay.OSPRayScaleArray = 'p'
swBdfoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
swBdfoamDisplay.SelectOrientationVectors = 'U'
swBdfoamDisplay.ScaleFactor = 0.0760000079870224
swBdfoamDisplay.SelectScaleArray = 'p'
swBdfoamDisplay.GlyphType = 'Arrow'
swBdfoamDisplay.GlyphTableIndexArray = 'p'
swBdfoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
swBdfoamDisplay.PolarAxes = 'PolarAxesRepresentation'
swBdfoamDisplay.ScalarOpacityFunction = pPWF
swBdfoamDisplay.ScalarOpacityUnitDistance = 0.007207100759349316
swBdfoamDisplay.GaussianRadius = 0.0380000039935112
swBdfoamDisplay.SetScaleArray = ['POINTS', 'p']
swBdfoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
swBdfoamDisplay.OpacityArray = ['POINTS', 'p']
swBdfoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
swBdfoamDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Slice'
slice1 = Slice(Input=swBdfoam)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.0, 0.0, -0.019999995827674866]

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1.SliceType)

# show data in view
slice1Display = Show(slice1, renderView1)
# trace defaults for the display properties.
slice1Display.Representation = 'Surface'
slice1Display.ColorArrayName = ['POINTS', 'p']
slice1Display.LookupTable = pLUT
slice1Display.OSPRayScaleArray = 'p'
slice1Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice1Display.SelectOrientationVectors = 'U'
slice1Display.ScaleFactor = 0.07600000202655793
slice1Display.SelectScaleArray = 'p'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'p'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'
slice1Display.GaussianRadius = 0.03800000101327897
slice1Display.SetScaleArray = ['POINTS', 'p']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'p']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(swBdfoam, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# get color legend/bar for pLUT in view renderView1
pLUTColorBar = GetScalarBar(pLUT, renderView1)

# change scalar bar placement
pLUTColorBar.Orientation = 'Vertical'
pLUTColorBar.WindowLocation = 'AnyLocation'
pLUTColorBar.Position = [0.7, 0.1]
pLUTColorBar.ScalarBarLength = 0.3

# current camera placement for renderView1
renderView1.CameraPosition = [-1.7671957010282522, 0.0, -0.019999995827674866]
renderView1.CameraFocalPoint = [0.0, 0.0, -0.019999995827674866]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.1

# save screenshot
SaveScreenshot('./snapshot_p.png', renderView1, ImageResolution=[1200, 1800])
#WriteImage('./snapshot_p.png')

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'T'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'T'
tLUT = GetColorTransferFunction('T')
tLUT.RGBPoints = [298.0, 0.231373, 0.298039, 0.752941, 1236.251953125, 0.865003, 0.865003, 0.865003, 2174.50390625, 0.705882, 0.0156863, 0.14902]
tLUT.ScalarRangeInitialized = 1.0

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# get color legend/bar for pLUT in view renderView1
tLUTColorBar = GetScalarBar(tLUT, renderView1)

# change scalar bar placement
tLUTColorBar.Orientation = 'Vertical'
tLUTColorBar.WindowLocation = 'AnyLocation'
tLUTColorBar.Position = [0.7, 0.1]
tLUTColorBar.ScalarBarLength = 0.3

# current camera placement for renderView1
renderView1.CameraPosition = [-1.7671957010282522, 0.0, -0.019999995827674866]
renderView1.CameraFocalPoint = [0.0, 0.0, -0.019999995827674866]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.1

# save screenshot
SaveScreenshot('./snapshot_T.png', renderView1, ImageResolution=[1200, 1800])

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'U', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(tLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'U'
uLUT = GetColorTransferFunction('U')
uLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 31.43146394925068, 0.865003, 0.865003, 0.865003, 62.86292789850136, 0.705882, 0.0156863, 0.14902]
uLUT.ScalarRangeInitialized = 1.0

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, True)

# Update a scalar bar component title.
UpdateScalarBarsComponentTitle(uLUT, slice1Display)

# current camera placement for renderView1
renderView1.CameraPosition = [-1.7671957010282522, 0.0, -0.019999995827674866]
renderView1.CameraFocalPoint = [0.0, 0.0, -0.019999995827674866]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.45738390384941197

# save screenshot
SaveScreenshot('./snapshot_U.png', renderView1, ImageResolution=[1200, 1800])

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'U', 'Z'))

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, False)

# Update a scalar bar component title.
UpdateScalarBarsComponentTitle(uLUT, slice1Display)

# current camera placement for renderView1
renderView1.CameraPosition = [-1.7671957010282522, 0.0, -0.019999995827674866]
renderView1.CameraFocalPoint = [0.0, 0.0, -0.019999995827674866]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.45738390384941197

# save screenshot
SaveScreenshot('./snapshot_UZ.png', renderView1, ImageResolution=[1200, 1800])

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'Z'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(uLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'Z'
zLUT = GetColorTransferFunction('Z')
zLUT.RGBPoints = [-1.1714355614006466e-12, 0.231373, 0.298039, 0.752941, 0.4999999999994143, 0.865003, 0.865003, 0.865003, 1.0, 0.705882, 0.0156863, 0.14902]
zLUT.ScalarRangeInitialized = 1.0

# current camera placement for renderView1
renderView1.CameraPosition = [-1.7671957010282522, 0.0, -0.019999995827674866]
renderView1.CameraFocalPoint = [0.0, 0.0, -0.019999995827674866]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.45738390384941197

# save screenshot
SaveScreenshot('./snapshot_Z.png', renderView1, ImageResolution=[1200, 1800])
