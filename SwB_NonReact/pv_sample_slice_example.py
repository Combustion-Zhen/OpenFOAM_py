#### import the simple module from the paraview
from paraview.simple import *
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'OpenFOAMReader'
swBfoam = OpenFOAMReader(FileName='/home/luz0a/OpenFOAM/luz0a-2.3.x/run/SwB/SwBd_L-400_20M_PISO/SwB.foam')
swBfoam.MeshRegions = ['internalMesh']
swBfoam.CellArrays = ['U', 'U_0', 'nuSgs', 'p']

# get animation scene
animationScene1 = GetAnimationScene()

# update animation scene based on data timesteps
animationScene1.UpdateAnimationUsingDataTimeSteps()

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1621, 1905]

# get color transfer function/color map for 'p'
pLUT = GetColorTransferFunction('p')

# show data in view
swBfoamDisplay = Show(swBfoam, renderView1)
# trace defaults for the display properties.
swBfoamDisplay.ColorArrayName = ['POINTS', 'p']
swBfoamDisplay.LookupTable = pLUT
swBfoamDisplay.ScalarOpacityUnitDistance = 0.007276560683000747

# reset view to fit data
renderView1.ResetCamera()

# show color bar/color legend
swBfoamDisplay.SetScalarBarVisibility(renderView1, True)

# get opacity transfer function/opacity map for 'p'
pPWF = GetOpacityTransferFunction('p')

# create a new 'Slice'
slice1 = Slice(Input=swBfoam)
slice1.SliceType = 'Plane'
slice1.SliceOffsetValues = [0.0]

# init the 'Plane' selected for 'SliceType'
slice1.SliceType.Origin = [0.0, 0.0, -0.019999995827674866]

# toggle 3D widget visibility (only when running from the GUI)
Hide3DWidgets(proxy=slice1)

# show data in view
slice1Display = Show(slice1, renderView1)
# trace defaults for the display properties.
slice1Display.ColorArrayName = ['POINTS', 'p']
slice1Display.LookupTable = pLUT

# hide data in view
Hide(swBfoam, renderView1)

# show color bar/color legend
slice1Display.SetScalarBarVisibility(renderView1, True)

# save data
SaveData('/home/luz0a/OpenFOAM/luz0a-2.3.x/run/SwB/SwBd_L-400_20M_PISO/vel_test_plane.csv', proxy=slice1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [1.3185222739648121, 0.6234873869718071, 1.4312662978622355]
renderView1.CameraFocalPoint = [0.0, 0.0, -0.019999995827674866]
renderView1.CameraViewUp = [-0.1557150105024011, 0.9510062234552389, -0.2670954856481883]
renderView1.CameraParallelScale = 0.5375177895330844

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).