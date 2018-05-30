#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
swBfoam = OpenFOAMReader(FileName='SwB.foam')
swBfoam.MeshRegions = ['internalMesh']
swBfoam.CellArrays = ['CH4Mean', 'CH4Prime2Mean', 'CO2Mean', 'CO2Prime2Mean', 'COMean', 'COPrime2Mean', 'H2Mean', 'H2OMean', 'H2OPrime2Mean', 'H2Prime2Mean', 'N2Mean', 'N2Prime2Mean', 'NOMean', 'NOPrime2Mean', 'O2Mean', 'O2Prime2Mean', 'OHMean', 'OHPrime2Mean', 'T', 'TMean', 'TPrime2Mean', 'U', 'UMean', 'UPrime2Mean', 'Z', 'ZMean', 'ZPrime2Mean', 'alphaSgs', 'chi', 'chiMean', 'chiPrime2Mean', 'muSgs', 'p', 'rho', 'thermo:alpha', 'thermo:mu', 'thermo:psi', 'varZ', 'varZMean', 'varZPrime2Mean']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
renderView1.ViewSize = [2199, 1890]

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')
pLUT.RGBPoints = [92308.953125, 0.231373, 0.298039, 0.752941, 103047.96875, 0.865003, 0.865003, 0.865003, 113786.984375, 0.705882, 0.0156863, 0.14902]
pLUT.ScalarRangeInitialized = 1.0

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')
pPWF.Points = [92308.953125, 0.0, 0.5, 0.0, 113786.984375, 1.0, 0.5, 0.0]
pPWF.ScalarRangeInitialized = 1

# show data in view
swBfoamDisplay = Show(swBfoam, renderView1)
# trace defaults for the display properties.
swBfoamDisplay.Representation = 'Surface'
swBfoamDisplay.ColorArrayName = ['POINTS', 'p']
swBfoamDisplay.LookupTable = pLUT
swBfoamDisplay.OSPRayScaleArray = 'p'
swBfoamDisplay.OSPRayScaleFunction = 'PiecewiseFunction'
swBfoamDisplay.SelectOrientationVectors = 'U'
swBfoamDisplay.ScaleFactor = 0.0760000079870224
swBfoamDisplay.SelectScaleArray = 'p'
swBfoamDisplay.GlyphType = 'Arrow'
swBfoamDisplay.GlyphTableIndexArray = 'p'
swBfoamDisplay.DataAxesGrid = 'GridAxesRepresentation'
swBfoamDisplay.PolarAxes = 'PolarAxesRepresentation'
swBfoamDisplay.ScalarOpacityFunction = pPWF
swBfoamDisplay.ScalarOpacityUnitDistance = 0.005582608543122148
swBfoamDisplay.GaussianRadius = 0.0380000039935112
swBfoamDisplay.SetScaleArray = ['POINTS', 'p']
swBfoamDisplay.ScaleTransferFunction = 'PiecewiseFunction'
swBfoamDisplay.OpacityArray = ['POINTS', 'p']
swBfoamDisplay.OpacityTransferFunction = 'PiecewiseFunction'

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
swBfoamDisplay.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Clip'
clip1 = Clip(Input=swBfoam)
clip1.ClipType = 'Plane'
clip1.Scalars = ['POINTS', 'p']
clip1.Value = 103047.96875

# init the 'Plane' selected for 'ClipType'
clip1.ClipType.Origin = [0.0, 0.0, -0.019999995827674866]

# Properties modified on clip1.ClipType
clip1.ClipType.Origin = [0.0, 0.0, -0.06]
clip1.ClipType.Normal = [0.0, 0.0, 1.0]

# Properties modified on clip1.ClipType
clip1.ClipType.Origin = [0.0, 0.0, -0.06]
clip1.ClipType.Normal = [0.0, 0.0, 1.0]

# show data in view
clip1Display = Show(clip1, renderView1)
# trace defaults for the display properties.
clip1Display.Representation = 'Surface'
clip1Display.ColorArrayName = ['POINTS', 'p']
clip1Display.LookupTable = pLUT
clip1Display.OSPRayScaleArray = 'p'
clip1Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip1Display.SelectOrientationVectors = 'U'
clip1Display.ScaleFactor = 0.042000004276633265
clip1Display.SelectScaleArray = 'p'
clip1Display.GlyphType = 'Arrow'
clip1Display.GlyphTableIndexArray = 'p'
clip1Display.DataAxesGrid = 'GridAxesRepresentation'
clip1Display.PolarAxes = 'PolarAxesRepresentation'
clip1Display.ScalarOpacityFunction = pPWF
clip1Display.ScalarOpacityUnitDistance = 0.004296650276400489
clip1Display.GaussianRadius = 0.021000002138316633
clip1Display.SetScaleArray = ['POINTS', 'p']
clip1Display.ScaleTransferFunction = 'PiecewiseFunction'
clip1Display.OpacityArray = ['POINTS', 'p']
clip1Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(swBfoam, renderView1)

# show color bar/color legend
clip1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# reset view to fit data
renderView1.ResetCamera()

# create a new 'Clip'
clip2 = Clip(Input=clip1)
clip2.ClipType = 'Plane'
clip2.Scalars = ['POINTS', 'p']
clip2.Value = 101426.88671875

# init the 'Plane' selected for 'ClipType'
clip2.ClipType.Origin = [0.0, 0.0, 0.15000002272427082]

# Properties modified on clip2.ClipType
clip2.ClipType.Origin = [0.0, 0.0, 0.12]
clip2.ClipType.Normal = [0.0, 0.0, -1.0]

# Properties modified on clip2.ClipType
clip2.ClipType.Origin = [0.0, 0.0, 0.12]
clip2.ClipType.Normal = [0.0, 0.0, -1.0]

# show data in view
clip2Display = Show(clip2, renderView1)
# trace defaults for the display properties.
clip2Display.Representation = 'Surface'
clip2Display.ColorArrayName = ['POINTS', 'p']
clip2Display.LookupTable = pLUT
clip2Display.OSPRayScaleArray = 'p'
clip2Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip2Display.SelectOrientationVectors = 'U'
clip2Display.ScaleFactor = 0.02100000083446503
clip2Display.SelectScaleArray = 'p'
clip2Display.GlyphType = 'Arrow'
clip2Display.GlyphTableIndexArray = 'p'
clip2Display.DataAxesGrid = 'GridAxesRepresentation'
clip2Display.PolarAxes = 'PolarAxesRepresentation'
clip2Display.ScalarOpacityFunction = pPWF
clip2Display.ScalarOpacityUnitDistance = 0.002676453856209217
clip2Display.GaussianRadius = 0.010500000417232515
clip2Display.SetScaleArray = ['POINTS', 'p']
clip2Display.ScaleTransferFunction = 'PiecewiseFunction'
clip2Display.OpacityArray = ['POINTS', 'p']
clip2Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(clip1, renderView1)

# show color bar/color legend
clip2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Clip'
clip3 = Clip(Input=clip2)
clip3.ClipType = 'Plane'
clip3.Scalars = ['POINTS', 'p']
clip3.Value = 101426.88671875

# init the 'Plane' selected for 'ClipType'
clip3.ClipType.Origin = [0.0, 0.0, 0.029999999329447746]

# Properties modified on clip3.ClipType
clip3.ClipType.Origin = [0.0, -0.05, 0.029999999329447746]
clip3.ClipType.Normal = [0.0, 1.0, 0.0]

# Properties modified on clip3.ClipType
clip3.ClipType.Origin = [0.0, -0.05, 0.029999999329447746]
clip3.ClipType.Normal = [0.0, 1.0, 0.0]

# show data in view
clip3Display = Show(clip3, renderView1)
# trace defaults for the display properties.
clip3Display.Representation = 'Surface'
clip3Display.ColorArrayName = ['POINTS', 'p']
clip3Display.LookupTable = pLUT
clip3Display.OSPRayScaleArray = 'p'
clip3Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip3Display.SelectOrientationVectors = 'U'
clip3Display.ScaleFactor = 0.02100000083446503
clip3Display.SelectScaleArray = 'p'
clip3Display.GlyphType = 'Arrow'
clip3Display.GlyphTableIndexArray = 'p'
clip3Display.DataAxesGrid = 'GridAxesRepresentation'
clip3Display.PolarAxes = 'PolarAxesRepresentation'
clip3Display.ScalarOpacityFunction = pPWF
clip3Display.ScalarOpacityUnitDistance = 0.002455609039883639
clip3Display.GaussianRadius = 0.010500000417232515
clip3Display.SetScaleArray = ['POINTS', 'p']
clip3Display.ScaleTransferFunction = 'PiecewiseFunction'
clip3Display.OpacityArray = ['POINTS', 'p']
clip3Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(clip2, renderView1)

# show color bar/color legend
clip3Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Clip'
clip4 = Clip(Input=clip3)
clip4.ClipType = 'Plane'
clip4.Scalars = ['POINTS', 'p']
clip4.Value = 101426.88671875

# init the 'Plane' selected for 'ClipType'
clip4.ClipType.Origin = [0.0, 0.027500001713633537, 0.029999999329447746]

# Properties modified on clip4.ClipType
clip4.ClipType.Origin = [0.0, 0.05, 0.029999999329447746]
clip4.ClipType.Normal = [0.0, -1.0, 0.0]

# Properties modified on clip4.ClipType
clip4.ClipType.Origin = [0.0, 0.05, 0.029999999329447746]
clip4.ClipType.Normal = [0.0, -1.0, 0.0]

# show data in view
clip4Display = Show(clip4, renderView1)
# trace defaults for the display properties.
clip4Display.Representation = 'Surface'
clip4Display.ColorArrayName = ['POINTS', 'p']
clip4Display.LookupTable = pLUT
clip4Display.OSPRayScaleArray = 'p'
clip4Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip4Display.SelectOrientationVectors = 'U'
clip4Display.ScaleFactor = 0.02100000083446503
clip4Display.SelectScaleArray = 'p'
clip4Display.GlyphType = 'Arrow'
clip4Display.GlyphTableIndexArray = 'p'
clip4Display.DataAxesGrid = 'GridAxesRepresentation'
clip4Display.PolarAxes = 'PolarAxesRepresentation'
clip4Display.ScalarOpacityFunction = pPWF
clip4Display.ScalarOpacityUnitDistance = 0.0022892767869242786
clip4Display.GaussianRadius = 0.010500000417232515
clip4Display.SetScaleArray = ['POINTS', 'p']
clip4Display.ScaleTransferFunction = 'PiecewiseFunction'
clip4Display.OpacityArray = ['POINTS', 'p']
clip4Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(clip3, renderView1)

# show color bar/color legend
clip4Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Clip'
clip5 = Clip(Input=clip4)
clip5.ClipType = 'Plane'
clip5.Scalars = ['POINTS', 'p']
clip5.Value = 101426.88671875

# init the 'Plane' selected for 'ClipType'
clip5.ClipType.Origin = [0.0, 0.0, 0.029999999329447746]

# Properties modified on clip5.ClipType
clip5.ClipType.Normal = [0.0, 1.0, 0.0]

# Properties modified on clip5.ClipType
clip5.ClipType.Normal = [0.0, 1.0, 0.0]

# show data in view
clip5Display = Show(clip5, renderView1)
# trace defaults for the display properties.
clip5Display.Representation = 'Surface'
clip5Display.ColorArrayName = ['POINTS', 'p']
clip5Display.LookupTable = pLUT
clip5Display.OSPRayScaleArray = 'p'
clip5Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip5Display.SelectOrientationVectors = 'U'
clip5Display.ScaleFactor = 0.02100000083446503
clip5Display.SelectScaleArray = 'p'
clip5Display.GlyphType = 'Arrow'
clip5Display.GlyphTableIndexArray = 'p'
clip5Display.DataAxesGrid = 'GridAxesRepresentation'
clip5Display.PolarAxes = 'PolarAxesRepresentation'
clip5Display.ScalarOpacityFunction = pPWF
clip5Display.ScalarOpacityUnitDistance = 0.0027158731921682337
clip5Display.GaussianRadius = 0.010500000417232515
clip5Display.SetScaleArray = ['POINTS', 'p']
clip5Display.ScaleTransferFunction = 'PiecewiseFunction'
clip5Display.OpacityArray = ['POINTS', 'p']
clip5Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(clip4, renderView1)

# show color bar/color legend
clip5Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Slice'
slice1 = Slice(Input=clip5)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.0, 0.02500000037252903, 0.029999999329447746]

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
slice1Display.ScaleFactor = 0.01799999959766865
slice1Display.SelectScaleArray = 'p'
slice1Display.GlyphType = 'Arrow'
slice1Display.GlyphTableIndexArray = 'p'
slice1Display.DataAxesGrid = 'GridAxesRepresentation'
slice1Display.PolarAxes = 'PolarAxesRepresentation'
slice1Display.GaussianRadius = 0.008999999798834325
slice1Display.SetScaleArray = ['POINTS', 'p']
slice1Display.ScaleTransferFunction = 'PiecewiseFunction'
slice1Display.OpacityArray = ['POINTS', 'p']
slice1Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(clip5, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# set active source
SetActiveSource(clip4)

# create a new 'Clip'
clip6 = Clip(Input=clip4)
clip6.ClipType = 'Plane'
clip6.Scalars = ['POINTS', 'p']
clip6.Value = 101426.88671875

# init the 'Plane' selected for 'ClipType'
clip6.ClipType.Origin = [0.0, 0.0, 0.029999999329447746]

# set active source
SetActiveSource(clip6)

# show data in view
clip6Display = Show(clip6, renderView1)
# trace defaults for the display properties.
clip6Display.Representation = 'Surface'
clip6Display.ColorArrayName = ['POINTS', 'p']
clip6Display.LookupTable = pLUT
clip6Display.OSPRayScaleArray = 'p'
clip6Display.OSPRayScaleFunction = 'PiecewiseFunction'
clip6Display.SelectOrientationVectors = 'U'
clip6Display.ScaleFactor = 0.01799999959766865
clip6Display.SelectScaleArray = 'p'
clip6Display.GlyphType = 'Arrow'
clip6Display.GlyphTableIndexArray = 'p'
clip6Display.DataAxesGrid = 'GridAxesRepresentation'
clip6Display.PolarAxes = 'PolarAxesRepresentation'
clip6Display.ScalarOpacityFunction = pPWF
clip6Display.ScalarOpacityUnitDistance = 0.0022417471510480427
clip6Display.GaussianRadius = 0.008999999798834325
clip6Display.SetScaleArray = ['POINTS', 'p']
clip6Display.ScaleTransferFunction = 'PiecewiseFunction'
clip6Display.OpacityArray = ['POINTS', 'p']
clip6Display.OpacityTransferFunction = 'PiecewiseFunction'

# show color bar/color legend
clip6Display.SetScalarBarVisibility(renderView1, True)

# Properties modified on clip6.ClipType
clip6.ClipType.Normal = [0.0, -1.0, 0.0]

# Properties modified on clip6.ClipType
clip6.ClipType.Normal = [0.0, -1.0, 0.0]

# show data in view
clip6Display = Show(clip6, renderView1)

# hide data in view
Hide(clip4, renderView1)

# show color bar/color legend
clip6Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# create a new 'Slice'
slice2 = Slice(Input=clip6)
slice2.SliceType = 'Plane'
slice2.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice2.SliceType.Origin = [0.0, -0.02500000037252903, 0.029999999329447746]

# show data in view
slice2Display = Show(slice2, renderView1)
# trace defaults for the display properties.
slice2Display.Representation = 'Surface'
slice2Display.ColorArrayName = ['POINTS', 'p']
slice2Display.LookupTable = pLUT
slice2Display.OSPRayScaleArray = 'p'
slice2Display.OSPRayScaleFunction = 'PiecewiseFunction'
slice2Display.SelectOrientationVectors = 'U'
slice2Display.ScaleFactor = 0.01799999959766865
slice2Display.SelectScaleArray = 'p'
slice2Display.GlyphType = 'Arrow'
slice2Display.GlyphTableIndexArray = 'p'
slice2Display.DataAxesGrid = 'GridAxesRepresentation'
slice2Display.PolarAxes = 'PolarAxesRepresentation'
slice2Display.GaussianRadius = 0.008999999798834325
slice2Display.SetScaleArray = ['POINTS', 'p']
slice2Display.ScaleTransferFunction = 'PiecewiseFunction'
slice2Display.OpacityArray = ['POINTS', 'p']
slice2Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(clip6, renderView1)

# show color bar/color legend
slice2Display.SetScalarBarVisibility(renderView1, True)

# update the view to ensure updated data information
renderView1.Update()

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice2.SliceType)

# set active source
SetActiveSource(slice1)

# reset view to fit data
renderView1.ResetCamera()

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
tLUT.RGBPoints = [298.0, 0.231373, 0.298039, 0.752941, 1256.1572265625, 0.865003, 0.865003, 0.865003, 2214.314453125, 0.705882, 0.0156863, 0.14902]
tLUT.ScalarRangeInitialized = 1.0

# set active source
SetActiveSource(slice2)

# set scalar coloring
ColorBy(slice2Display, ('POINTS', 'TMean'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(pLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice2Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice2Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'TMean'
tMeanLUT = GetColorTransferFunction('TMean')
tMeanLUT.RGBPoints = [298.0, 0.231373, 0.298039, 0.752941, 1194.8056640625, 0.865003, 0.865003, 0.865003, 2091.611328125, 0.705882, 0.0156863, 0.14902]
tMeanLUT.ScalarRangeInitialized = 1.0

# create a new 'Temporal Statistics'
temporalStatistics1 = TemporalStatistics(Input=slice2)

# Properties modified on temporalStatistics1
temporalStatistics1.ComputeMinimum = 0
temporalStatistics1.ComputeMaximum = 0
temporalStatistics1.ComputeStandardDeviation = 0

# show data in view
temporalStatistics1Display = Show(temporalStatistics1, renderView1)
# trace defaults for the display properties.
temporalStatistics1Display.Representation = 'Surface'
temporalStatistics1Display.ColorArrayName = [None, '']
temporalStatistics1Display.OSPRayScaleArray = 'CH4Mean_average'
temporalStatistics1Display.OSPRayScaleFunction = 'PiecewiseFunction'
temporalStatistics1Display.SelectOrientationVectors = 'CH4Mean_average'
temporalStatistics1Display.ScaleFactor = 0.01799999959766865
temporalStatistics1Display.SelectScaleArray = 'CH4Mean_average'
temporalStatistics1Display.GlyphType = 'Arrow'
temporalStatistics1Display.GlyphTableIndexArray = 'CH4Mean_average'
temporalStatistics1Display.DataAxesGrid = 'GridAxesRepresentation'
temporalStatistics1Display.PolarAxes = 'PolarAxesRepresentation'
temporalStatistics1Display.GaussianRadius = 0.008999999798834325
temporalStatistics1Display.SetScaleArray = ['POINTS', 'CH4Mean_average']
temporalStatistics1Display.ScaleTransferFunction = 'PiecewiseFunction'
temporalStatistics1Display.OpacityArray = ['POINTS', 'CH4Mean_average']
temporalStatistics1Display.OpacityTransferFunction = 'PiecewiseFunction'

# hide data in view
Hide(slice2, renderView1)

# update the view to ensure updated data information
renderView1.Update()

# set scalar coloring
ColorBy(temporalStatistics1Display, ('POINTS', 'TMean_average'))

# rescale color and/or opacity maps used to include current data range
temporalStatistics1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
temporalStatistics1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'TMean_average'
tMean_averageLUT = GetColorTransferFunction('TMean_average')
tMean_averageLUT.RGBPoints = [298.0, 0.231373, 0.298039, 0.752941, 1189.994873046875, 0.865003, 0.865003, 0.865003, 2081.98974609375, 0.705882, 0.0156863, 0.14902]
tMean_averageLUT.ScalarRangeInitialized = 1.0

# set scalar coloring
ColorBy(temporalStatistics1Display, ('POINTS', 'UMean_average', 'Magnitude'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(tMean_averageLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
temporalStatistics1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
temporalStatistics1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'UMean_average'
uMean_averageLUT = GetColorTransferFunction('UMean_average')
uMean_averageLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 19.858241780686676, 0.865003, 0.865003, 0.865003, 39.71648356137335, 0.705882, 0.0156863, 0.14902]
uMean_averageLUT.ScalarRangeInitialized = 1.0

# set scalar coloring
ColorBy(temporalStatistics1Display, ('POINTS', 'UMean_average', 'Z'))

# rescale color and/or opacity maps used to exactly fit the current data range
temporalStatistics1Display.RescaleTransferFunctionToDataRange(False, False)

# Update a scalar bar component title.
UpdateScalarBarsComponentTitle(uMean_averageLUT, temporalStatistics1Display)

# set active source
SetActiveSource(slice1)

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
uLUT.RGBPoints = [0.0, 0.231373, 0.298039, 0.752941, 19.061934160671782, 0.865003, 0.865003, 0.865003, 38.123868321343565, 0.705882, 0.0156863, 0.14902]
uLUT.ScalarRangeInitialized = 1.0

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'U', 'Z'))

# rescale color and/or opacity maps used to exactly fit the current data range
slice1Display.RescaleTransferFunctionToDataRange(False, False)

# Update a scalar bar component title.
UpdateScalarBarsComponentTitle(uLUT, slice1Display)

# current camera placement for renderView1
renderView1.CameraPosition = [-0.39779259664765326, 0.0, 0.029999999329447746]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.029999999329447746]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.1029563000131978

# save screenshot
SaveScreenshot('snapshot_U_UMean_Z.png', renderView1, ImageResolution=[2199, 1890])

# set scalar coloring
ColorBy(slice1Display, ('POINTS', 'T'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(uLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
slice1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(temporalStatistics1)

# set scalar coloring
ColorBy(temporalStatistics1Display, ('POINTS', 'TMean_average'))

# Hide the scalar bar for this color map if no visible data is colored by it.
HideScalarBarIfNotNeeded(uMean_averageLUT, renderView1)

# rescale color and/or opacity maps used to include current data range
temporalStatistics1Display.RescaleTransferFunctionToDataRange(True, False)

# show color bar/color legend
temporalStatistics1Display.SetScalarBarVisibility(renderView1, True)

# set active source
SetActiveSource(slice1)

animationScene1.GoToLast()

# current camera placement for renderView1
renderView1.CameraPosition = [-0.39779259664765326, 0.0, 0.029999999329447746]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.029999999329447746]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.1029563000131978

# save screenshot
SaveScreenshot('snapshot_T_TMean.png', renderView1, ImageResolution=[2199, 1890])

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [-0.39779259664765326, 0.0, 0.029999999329447746]
renderView1.CameraFocalPoint = [0.0, 0.0, 0.029999999329447746]
renderView1.CameraViewUp = [0.0, 0.0, 1.0]
renderView1.CameraParallelScale = 0.1029563000131978

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
