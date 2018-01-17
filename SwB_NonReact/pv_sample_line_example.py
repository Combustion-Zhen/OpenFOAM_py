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
# renderView1.ViewSize = [3248, 1905]

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

# create a new 'Plot Over Line'
plotOverLine1 = PlotOverLine(Input=swBfoam,
    Source='High Resolution Line Source')

# init the 'High Resolution Line Source' selected for 'Source'
plotOverLine1.Source.Point1 = [-0.18000000715255737, -0.18000000715255737, -0.40000003576278687]
plotOverLine1.Source.Point2 = [0.18000000715255737, 0.18000000715255737, 0.36000004410743713]

# Properties modified on plotOverLine1
plotOverLine1.Tolerance = 2.22044604925031e-16

# Properties modified on plotOverLine1.Source
plotOverLine1.Source.Point1 = [-0.18000000715255737, 0.0, -0.35]
plotOverLine1.Source.Point2 = [0.18000000715255737, 0.0, -0.35]

# get layout
viewLayout1 = GetLayout()

# Create a new 'Line Chart View'
lineChartView1 = CreateView('XYChartView')
lineChartView1.ViewSize = [1620, 1905]

# place view in the layout
viewLayout1.AssignView(2, lineChartView1)

# show data in view
plotOverLine1Display = Show(plotOverLine1, lineChartView1)
# trace defaults for the display properties.
plotOverLine1Display.CompositeDataSetIndex = [0]
plotOverLine1Display.UseIndexForXAxis = 0
plotOverLine1Display.XArrayName = 'arc_length'
plotOverLine1Display.SeriesVisibility = ['nuSgs', 'p', 'U_Magnitude', 'U_0_Magnitude', 'UMean_Magnitude', 'UPrime2Mean_Magnitude']
plotOverLine1Display.SeriesLabel = ['arc_length', 'arc_length', 'nuSgs', 'nuSgs', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude', 'U_0_X', 'U_0_X', 'U_0_Y', 'U_0_Y', 'U_0_Z', 'U_0_Z', 'U_0_Magnitude', 'U_0_Magnitude', 'UMean_X', 'UMean_X', 'UMean_Y', 'UMean_Y', 'UMean_Z', 'UMean_Z', 'UMean_Magnitude', 'UMean_Magnitude', 'UPrime2Mean_XX', 'UPrime2Mean_XX', 'UPrime2Mean_YY', 'UPrime2Mean_YY', 'UPrime2Mean_ZZ', 'UPrime2Mean_ZZ', 'UPrime2Mean_XY', 'UPrime2Mean_XY', 'UPrime2Mean_YZ', 'UPrime2Mean_YZ', 'UPrime2Mean_XZ', 'UPrime2Mean_XZ', 'UPrime2Mean_Magnitude', 'UPrime2Mean_Magnitude']
plotOverLine1Display.SeriesColor = ['arc_length', '0', '0', '0', 'nuSgs', '0.89', '0.1', '0.11', 'p', '0.22', '0.49', '0.72', 'U_X', '0.3', '0.69', '0.29', 'U_Y', '0.6', '0.31', '0.64', 'U_Z', '1', '0.5', '0', 'U_Magnitude', '0.65', '0.34', '0.16', 'U_0_X', '0', '0', '0', 'U_0_Y', '0.89', '0.1', '0.11', 'U_0_Z', '0.22', '0.49', '0.72', 'U_0_Magnitude', '0.3', '0.69', '0.29', 'UMean_X', '0.6', '0.31', '0.64', 'UMean_Y', '1', '0.5', '0', 'UMean_Z', '0.65', '0.34', '0.16', 'UMean_Magnitude', '0', '0', '0', 'UPrime2Mean_XX', '0.89', '0.1', '0.11', 'UPrime2Mean_YY', '0.22', '0.49', '0.72', 'UPrime2Mean_ZZ', '0.3', '0.69', '0.29', 'UPrime2Mean_XY', '0.6', '0.31', '0.64', 'UPrime2Mean_YZ', '1', '0.5', '0', 'UPrime2Mean_XZ', '0.65', '0.34', '0.16', 'UPrime2Mean_Magnitude', '0', '0', '0']
plotOverLine1Display.SeriesPlotCorner = ['arc_length', '0', 'nuSgs', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'U_0_X', '0', 'U_0_Y', '0', 'U_0_Z', '0', 'U_0_Magnitude', '0', 'UMean_X', '0', 'UMean_Y', '0', 'UMean_Z', '0', 'UMean_Magnitude', '0', 'UPrime2Mean_XX', '0', 'UPrime2Mean_YY', '0', 'UPrime2Mean_ZZ', '0', 'UPrime2Mean_XY', '0', 'UPrime2Mean_YZ', '0', 'UPrime2Mean_XZ', '0', 'UPrime2Mean_Magnitude', '0']
plotOverLine1Display.SeriesLineStyle = ['arc_length', '1', 'nuSgs', '1', 'p', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'U_Magnitude', '1', 'U_0_X', '1', 'U_0_Y', '1', 'U_0_Z', '1', 'U_0_Magnitude', '1', 'UMean_X', '1', 'UMean_Y', '1', 'UMean_Z', '1', 'UMean_Magnitude', '1', 'UPrime2Mean_XX', '1', 'UPrime2Mean_YY', '1', 'UPrime2Mean_ZZ', '1', 'UPrime2Mean_XY', '1', 'UPrime2Mean_YZ', '1', 'UPrime2Mean_XZ', '1', 'UPrime2Mean_Magnitude', '1']
plotOverLine1Display.SeriesLineThickness = ['arc_length', '2', 'nuSgs', '2', 'p', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'U_Magnitude', '2', 'U_0_X', '2', 'U_0_Y', '2', 'U_0_Z', '2', 'U_0_Magnitude', '2', 'UMean_X', '2', 'UMean_Y', '2', 'UMean_Z', '2', 'UMean_Magnitude', '2', 'UPrime2Mean_XX', '2', 'UPrime2Mean_YY', '2', 'UPrime2Mean_ZZ', '2', 'UPrime2Mean_XY', '2', 'UPrime2Mean_YZ', '2', 'UPrime2Mean_XZ', '2', 'UPrime2Mean_Magnitude', '2']
plotOverLine1Display.SeriesMarkerStyle = ['arc_length', '0', 'nuSgs', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'U_0_X', '0', 'U_0_Y', '0', 'U_0_Z', '0', 'U_0_Magnitude', '0', 'UMean_X', '0', 'UMean_Y', '0', 'UMean_Z', '0', 'UMean_Magnitude', '0', 'UPrime2Mean_XX', '0', 'UPrime2Mean_YY', '0', 'UPrime2Mean_ZZ', '0', 'UPrime2Mean_XY', '0', 'UPrime2Mean_YZ', '0', 'UPrime2Mean_XZ', '0', 'UPrime2Mean_Magnitude', '0']

# Rescale transfer function
pLUT.RescaleTransferFunction(-342.670043945, 1023.70568848)

# Rescale transfer function
pPWF.RescaleTransferFunction(-342.670043945, 1023.70568848)

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = ['nuSgs', 'U_Magnitude', 'U_0_Magnitude', 'UMean_Magnitude', 'UPrime2Mean_Magnitude']
plotOverLine1Display.SeriesColor = ['arc_length', '0', '0', '0', 'nuSgs', '0.889998', '0.100008', '0.110002', 'p', '0.220005', '0.489998', '0.719997', 'U_X', '0.300008', '0.689998', '0.289998', 'U_Y', '0.6', '0.310002', '0.639994', 'U_Z', '1', '0.500008', '0', 'U_Magnitude', '0.650004', '0.340002', '0.160006', 'U_0_X', '0', '0', '0', 'U_0_Y', '0.889998', '0.100008', '0.110002', 'U_0_Z', '0.220005', '0.489998', '0.719997', 'U_0_Magnitude', '0.300008', '0.689998', '0.289998', 'UMean_X', '0.6', '0.310002', '0.639994', 'UMean_Y', '1', '0.500008', '0', 'UMean_Z', '0.650004', '0.340002', '0.160006', 'UMean_Magnitude', '0', '0', '0', 'UPrime2Mean_XX', '0.889998', '0.100008', '0.110002', 'UPrime2Mean_YY', '0.220005', '0.489998', '0.719997', 'UPrime2Mean_ZZ', '0.300008', '0.689998', '0.289998', 'UPrime2Mean_XY', '0.6', '0.310002', '0.639994', 'UPrime2Mean_YZ', '1', '0.500008', '0', 'UPrime2Mean_XZ', '0.650004', '0.340002', '0.160006', 'UPrime2Mean_Magnitude', '0', '0', '0']
plotOverLine1Display.SeriesPlotCorner = ['UMean_Magnitude', '0', 'UMean_X', '0', 'UMean_Y', '0', 'UMean_Z', '0', 'UPrime2Mean_Magnitude', '0', 'UPrime2Mean_XX', '0', 'UPrime2Mean_XY', '0', 'UPrime2Mean_XZ', '0', 'UPrime2Mean_YY', '0', 'UPrime2Mean_YZ', '0', 'UPrime2Mean_ZZ', '0', 'U_0_Magnitude', '0', 'U_0_X', '0', 'U_0_Y', '0', 'U_0_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'nuSgs', '0', 'p', '0']
plotOverLine1Display.SeriesLineStyle = ['UMean_Magnitude', '1', 'UMean_X', '1', 'UMean_Y', '1', 'UMean_Z', '1', 'UPrime2Mean_Magnitude', '1', 'UPrime2Mean_XX', '1', 'UPrime2Mean_XY', '1', 'UPrime2Mean_XZ', '1', 'UPrime2Mean_YY', '1', 'UPrime2Mean_YZ', '1', 'UPrime2Mean_ZZ', '1', 'U_0_Magnitude', '1', 'U_0_X', '1', 'U_0_Y', '1', 'U_0_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'arc_length', '1', 'nuSgs', '1', 'p', '1']
plotOverLine1Display.SeriesLineThickness = ['UMean_Magnitude', '2', 'UMean_X', '2', 'UMean_Y', '2', 'UMean_Z', '2', 'UPrime2Mean_Magnitude', '2', 'UPrime2Mean_XX', '2', 'UPrime2Mean_XY', '2', 'UPrime2Mean_XZ', '2', 'UPrime2Mean_YY', '2', 'UPrime2Mean_YZ', '2', 'UPrime2Mean_ZZ', '2', 'U_0_Magnitude', '2', 'U_0_X', '2', 'U_0_Y', '2', 'U_0_Z', '2', 'U_Magnitude', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'arc_length', '2', 'nuSgs', '2', 'p', '2']
plotOverLine1Display.SeriesMarkerStyle = ['UMean_Magnitude', '0', 'UMean_X', '0', 'UMean_Y', '0', 'UMean_Z', '0', 'UPrime2Mean_Magnitude', '0', 'UPrime2Mean_XX', '0', 'UPrime2Mean_XY', '0', 'UPrime2Mean_XZ', '0', 'UPrime2Mean_YY', '0', 'UPrime2Mean_YZ', '0', 'UPrime2Mean_ZZ', '0', 'U_0_Magnitude', '0', 'U_0_X', '0', 'U_0_Y', '0', 'U_0_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'nuSgs', '0', 'p', '0']

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = ['U_Magnitude', 'U_0_Magnitude', 'UMean_Magnitude', 'UPrime2Mean_Magnitude']

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = ['U_Magnitude', 'UMean_Magnitude', 'UPrime2Mean_Magnitude']

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = ['U_Magnitude', 'UMean_Magnitude']

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = ['UMean_Magnitude']

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = []

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = ['UMean_Z']

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = ['UMean_Y', 'UMean_Z']

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = ['UMean_X', 'UMean_Y', 'UMean_Z']

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = ['UMean_Y', 'UMean_Z']

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = ['UMean_Z']

# Properties modified on plotOverLine1Display
plotOverLine1Display.SeriesVisibility = []

# set active source
SetActiveSource(swBfoam)

# create a new 'Plot Selection Over Time'
plotSelectionOverTime1 = PlotSelectionOverTime(Input=swBfoam,
    Selection=None)

# set active source
SetActiveSource(swBfoam)

# destroy plotSelectionOverTime1
Delete(plotSelectionOverTime1)
del plotSelectionOverTime1

# create a new 'Plot Over Line'
plotOverLine2 = PlotOverLine(Input=swBfoam,
    Source='High Resolution Line Source')

# init the 'High Resolution Line Source' selected for 'Source'
plotOverLine2.Source.Point1 = [-0.18000000715255737, -0.18000000715255737, -0.40000003576278687]
plotOverLine2.Source.Point2 = [0.18000000715255737, 0.18000000715255737, 0.36000004410743713]

# Properties modified on swBfoam
swBfoam.CellArrays = ['U', 'U_0', 'nuSgs', 'p', 'UMean', 'UPrime2Mean']

# Properties modified on plotOverLine2
plotOverLine2.Tolerance = 2.22044604925031e-16

# Properties modified on plotOverLine2.Source
plotOverLine2.Source.Point1 = [-0.18000000715255737, 0.0, -0.1]
plotOverLine2.Source.Point2 = [0.18000000715255737, 0.0, -0.1]

# show data in view
plotOverLine2Display = Show(plotOverLine2, lineChartView1)
# trace defaults for the display properties.
plotOverLine2Display.CompositeDataSetIndex = [0]
plotOverLine2Display.UseIndexForXAxis = 0
plotOverLine2Display.XArrayName = 'arc_length'
plotOverLine2Display.SeriesVisibility = ['nuSgs', 'p', 'U_Magnitude', 'U_0_Magnitude', 'UMean_Magnitude', 'UPrime2Mean_Magnitude']
plotOverLine2Display.SeriesLabel = ['arc_length', 'arc_length', 'nuSgs', 'nuSgs', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude', 'U_0_X', 'U_0_X', 'U_0_Y', 'U_0_Y', 'U_0_Z', 'U_0_Z', 'U_0_Magnitude', 'U_0_Magnitude', 'UMean_X', 'UMean_X', 'UMean_Y', 'UMean_Y', 'UMean_Z', 'UMean_Z', 'UMean_Magnitude', 'UMean_Magnitude', 'UPrime2Mean_XX', 'UPrime2Mean_XX', 'UPrime2Mean_YY', 'UPrime2Mean_YY', 'UPrime2Mean_ZZ', 'UPrime2Mean_ZZ', 'UPrime2Mean_XY', 'UPrime2Mean_XY', 'UPrime2Mean_YZ', 'UPrime2Mean_YZ', 'UPrime2Mean_XZ', 'UPrime2Mean_XZ', 'UPrime2Mean_Magnitude', 'UPrime2Mean_Magnitude']
plotOverLine2Display.SeriesColor = ['arc_length', '0', '0', '0', 'nuSgs', '0.89', '0.1', '0.11', 'p', '0.22', '0.49', '0.72', 'U_X', '0.3', '0.69', '0.29', 'U_Y', '0.6', '0.31', '0.64', 'U_Z', '1', '0.5', '0', 'U_Magnitude', '0.65', '0.34', '0.16', 'U_0_X', '0', '0', '0', 'U_0_Y', '0.89', '0.1', '0.11', 'U_0_Z', '0.22', '0.49', '0.72', 'U_0_Magnitude', '0.3', '0.69', '0.29', 'UMean_X', '0.6', '0.31', '0.64', 'UMean_Y', '1', '0.5', '0', 'UMean_Z', '0.65', '0.34', '0.16', 'UMean_Magnitude', '0', '0', '0', 'UPrime2Mean_XX', '0.89', '0.1', '0.11', 'UPrime2Mean_YY', '0.22', '0.49', '0.72', 'UPrime2Mean_ZZ', '0.3', '0.69', '0.29', 'UPrime2Mean_XY', '0.6', '0.31', '0.64', 'UPrime2Mean_YZ', '1', '0.5', '0', 'UPrime2Mean_XZ', '0.65', '0.34', '0.16', 'UPrime2Mean_Magnitude', '0', '0', '0']
plotOverLine2Display.SeriesPlotCorner = ['arc_length', '0', 'nuSgs', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'U_0_X', '0', 'U_0_Y', '0', 'U_0_Z', '0', 'U_0_Magnitude', '0', 'UMean_X', '0', 'UMean_Y', '0', 'UMean_Z', '0', 'UMean_Magnitude', '0', 'UPrime2Mean_XX', '0', 'UPrime2Mean_YY', '0', 'UPrime2Mean_ZZ', '0', 'UPrime2Mean_XY', '0', 'UPrime2Mean_YZ', '0', 'UPrime2Mean_XZ', '0', 'UPrime2Mean_Magnitude', '0']
plotOverLine2Display.SeriesLineStyle = ['arc_length', '1', 'nuSgs', '1', 'p', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'U_Magnitude', '1', 'U_0_X', '1', 'U_0_Y', '1', 'U_0_Z', '1', 'U_0_Magnitude', '1', 'UMean_X', '1', 'UMean_Y', '1', 'UMean_Z', '1', 'UMean_Magnitude', '1', 'UPrime2Mean_XX', '1', 'UPrime2Mean_YY', '1', 'UPrime2Mean_ZZ', '1', 'UPrime2Mean_XY', '1', 'UPrime2Mean_YZ', '1', 'UPrime2Mean_XZ', '1', 'UPrime2Mean_Magnitude', '1']
plotOverLine2Display.SeriesLineThickness = ['arc_length', '2', 'nuSgs', '2', 'p', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'U_Magnitude', '2', 'U_0_X', '2', 'U_0_Y', '2', 'U_0_Z', '2', 'U_0_Magnitude', '2', 'UMean_X', '2', 'UMean_Y', '2', 'UMean_Z', '2', 'UMean_Magnitude', '2', 'UPrime2Mean_XX', '2', 'UPrime2Mean_YY', '2', 'UPrime2Mean_ZZ', '2', 'UPrime2Mean_XY', '2', 'UPrime2Mean_YZ', '2', 'UPrime2Mean_XZ', '2', 'UPrime2Mean_Magnitude', '2']
plotOverLine2Display.SeriesMarkerStyle = ['arc_length', '0', 'nuSgs', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'U_0_X', '0', 'U_0_Y', '0', 'U_0_Z', '0', 'U_0_Magnitude', '0', 'UMean_X', '0', 'UMean_Y', '0', 'UMean_Z', '0', 'UMean_Magnitude', '0', 'UPrime2Mean_XX', '0', 'UPrime2Mean_YY', '0', 'UPrime2Mean_ZZ', '0', 'UPrime2Mean_XY', '0', 'UPrime2Mean_YZ', '0', 'UPrime2Mean_XZ', '0', 'UPrime2Mean_Magnitude', '0']

# Properties modified on plotOverLine2Display
plotOverLine2Display.SeriesVisibility = []
plotOverLine2Display.SeriesColor = ['arc_length', '0', '0', '0', 'nuSgs', '0.889998', '0.100008', '0.110002', 'p', '0.220005', '0.489998', '0.719997', 'U_X', '0.300008', '0.689998', '0.289998', 'U_Y', '0.6', '0.310002', '0.639994', 'U_Z', '1', '0.500008', '0', 'U_Magnitude', '0.650004', '0.340002', '0.160006', 'U_0_X', '0', '0', '0', 'U_0_Y', '0.889998', '0.100008', '0.110002', 'U_0_Z', '0.220005', '0.489998', '0.719997', 'U_0_Magnitude', '0.300008', '0.689998', '0.289998', 'UMean_X', '0.6', '0.310002', '0.639994', 'UMean_Y', '1', '0.500008', '0', 'UMean_Z', '0.650004', '0.340002', '0.160006', 'UMean_Magnitude', '0', '0', '0', 'UPrime2Mean_XX', '0.889998', '0.100008', '0.110002', 'UPrime2Mean_YY', '0.220005', '0.489998', '0.719997', 'UPrime2Mean_ZZ', '0.300008', '0.689998', '0.289998', 'UPrime2Mean_XY', '0.6', '0.310002', '0.639994', 'UPrime2Mean_YZ', '1', '0.500008', '0', 'UPrime2Mean_XZ', '0.650004', '0.340002', '0.160006', 'UPrime2Mean_Magnitude', '0', '0', '0']
plotOverLine2Display.SeriesPlotCorner = ['UMean_Magnitude', '0', 'UMean_X', '0', 'UMean_Y', '0', 'UMean_Z', '0', 'UPrime2Mean_Magnitude', '0', 'UPrime2Mean_XX', '0', 'UPrime2Mean_XY', '0', 'UPrime2Mean_XZ', '0', 'UPrime2Mean_YY', '0', 'UPrime2Mean_YZ', '0', 'UPrime2Mean_ZZ', '0', 'U_0_Magnitude', '0', 'U_0_X', '0', 'U_0_Y', '0', 'U_0_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'nuSgs', '0', 'p', '0']
plotOverLine2Display.SeriesLineStyle = ['UMean_Magnitude', '1', 'UMean_X', '1', 'UMean_Y', '1', 'UMean_Z', '1', 'UPrime2Mean_Magnitude', '1', 'UPrime2Mean_XX', '1', 'UPrime2Mean_XY', '1', 'UPrime2Mean_XZ', '1', 'UPrime2Mean_YY', '1', 'UPrime2Mean_YZ', '1', 'UPrime2Mean_ZZ', '1', 'U_0_Magnitude', '1', 'U_0_X', '1', 'U_0_Y', '1', 'U_0_Z', '1', 'U_Magnitude', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'arc_length', '1', 'nuSgs', '1', 'p', '1']
plotOverLine2Display.SeriesLineThickness = ['UMean_Magnitude', '2', 'UMean_X', '2', 'UMean_Y', '2', 'UMean_Z', '2', 'UPrime2Mean_Magnitude', '2', 'UPrime2Mean_XX', '2', 'UPrime2Mean_XY', '2', 'UPrime2Mean_XZ', '2', 'UPrime2Mean_YY', '2', 'UPrime2Mean_YZ', '2', 'UPrime2Mean_ZZ', '2', 'U_0_Magnitude', '2', 'U_0_X', '2', 'U_0_Y', '2', 'U_0_Z', '2', 'U_Magnitude', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'arc_length', '2', 'nuSgs', '2', 'p', '2']
plotOverLine2Display.SeriesMarkerStyle = ['UMean_Magnitude', '0', 'UMean_X', '0', 'UMean_Y', '0', 'UMean_Z', '0', 'UPrime2Mean_Magnitude', '0', 'UPrime2Mean_XX', '0', 'UPrime2Mean_XY', '0', 'UPrime2Mean_XZ', '0', 'UPrime2Mean_YY', '0', 'UPrime2Mean_YZ', '0', 'UPrime2Mean_ZZ', '0', 'U_0_Magnitude', '0', 'U_0_X', '0', 'U_0_Y', '0', 'U_0_Z', '0', 'U_Magnitude', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'arc_length', '0', 'nuSgs', '0', 'p', '0']

# save data
SaveData('/home/luz0a/OpenFOAM/luz0a-2.3.x/run/SwB/SwBd_L-400_20M_PISO/vel_test2.csv', proxy=plotOverLine2)

# set active source
SetActiveSource(plotOverLine1)

# save data
SaveData('/home/luz0a/OpenFOAM/luz0a-2.3.x/run/SwB/SwBd_L-400_20M_PISO/vel_test1.csv', proxy=plotOverLine1)

# set active source
SetActiveSource(swBfoam)

# create a new 'Plot Global Variables Over Time'
plotGlobalVariablesOverTime1 = PlotGlobalVariablesOverTime(Input=swBfoam)

# set active source
SetActiveSource(swBfoam)

# destroy plotGlobalVariablesOverTime1
Delete(plotGlobalVariablesOverTime1)
del plotGlobalVariablesOverTime1

# create a new 'Plot Over Line'
plotOverLine3 = PlotOverLine(Input=swBfoam,
    Source='High Resolution Line Source')

# init the 'High Resolution Line Source' selected for 'Source'
plotOverLine3.Source.Point1 = [-0.18000000715255737, -0.18000000715255737, -0.40000003576278687]
plotOverLine3.Source.Point2 = [0.18000000715255737, 0.18000000715255737, 0.36000004410743713]

# Properties modified on plotOverLine3
plotOverLine3.Tolerance = 2.22044604925031e-16

# Properties modified on plotOverLine3.Source
plotOverLine3.Source.Point1 = [-0.02, 0.0, 0.01]
plotOverLine3.Source.Point2 = [0.02, 0.0, 0.01]

# show data in view
plotOverLine3Display = Show(plotOverLine3, lineChartView1)
# trace defaults for the display properties.
plotOverLine3Display.CompositeDataSetIndex = [0]
plotOverLine3Display.UseIndexForXAxis = 0
plotOverLine3Display.XArrayName = 'arc_length'
plotOverLine3Display.SeriesVisibility = ['nuSgs', 'p', 'U_Magnitude', 'U_0_Magnitude', 'UMean_Magnitude', 'UPrime2Mean_Magnitude']
plotOverLine3Display.SeriesLabel = ['arc_length', 'arc_length', 'nuSgs', 'nuSgs', 'p', 'p', 'U_X', 'U_X', 'U_Y', 'U_Y', 'U_Z', 'U_Z', 'U_Magnitude', 'U_Magnitude', 'U_0_X', 'U_0_X', 'U_0_Y', 'U_0_Y', 'U_0_Z', 'U_0_Z', 'U_0_Magnitude', 'U_0_Magnitude', 'UMean_X', 'UMean_X', 'UMean_Y', 'UMean_Y', 'UMean_Z', 'UMean_Z', 'UMean_Magnitude', 'UMean_Magnitude', 'UPrime2Mean_XX', 'UPrime2Mean_XX', 'UPrime2Mean_YY', 'UPrime2Mean_YY', 'UPrime2Mean_ZZ', 'UPrime2Mean_ZZ', 'UPrime2Mean_XY', 'UPrime2Mean_XY', 'UPrime2Mean_YZ', 'UPrime2Mean_YZ', 'UPrime2Mean_XZ', 'UPrime2Mean_XZ', 'UPrime2Mean_Magnitude', 'UPrime2Mean_Magnitude']
plotOverLine3Display.SeriesColor = ['arc_length', '0', '0', '0', 'nuSgs', '0.89', '0.1', '0.11', 'p', '0.22', '0.49', '0.72', 'U_X', '0.3', '0.69', '0.29', 'U_Y', '0.6', '0.31', '0.64', 'U_Z', '1', '0.5', '0', 'U_Magnitude', '0.65', '0.34', '0.16', 'U_0_X', '0', '0', '0', 'U_0_Y', '0.89', '0.1', '0.11', 'U_0_Z', '0.22', '0.49', '0.72', 'U_0_Magnitude', '0.3', '0.69', '0.29', 'UMean_X', '0.6', '0.31', '0.64', 'UMean_Y', '1', '0.5', '0', 'UMean_Z', '0.65', '0.34', '0.16', 'UMean_Magnitude', '0', '0', '0', 'UPrime2Mean_XX', '0.89', '0.1', '0.11', 'UPrime2Mean_YY', '0.22', '0.49', '0.72', 'UPrime2Mean_ZZ', '0.3', '0.69', '0.29', 'UPrime2Mean_XY', '0.6', '0.31', '0.64', 'UPrime2Mean_YZ', '1', '0.5', '0', 'UPrime2Mean_XZ', '0.65', '0.34', '0.16', 'UPrime2Mean_Magnitude', '0', '0', '0']
plotOverLine3Display.SeriesPlotCorner = ['arc_length', '0', 'nuSgs', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'U_0_X', '0', 'U_0_Y', '0', 'U_0_Z', '0', 'U_0_Magnitude', '0', 'UMean_X', '0', 'UMean_Y', '0', 'UMean_Z', '0', 'UMean_Magnitude', '0', 'UPrime2Mean_XX', '0', 'UPrime2Mean_YY', '0', 'UPrime2Mean_ZZ', '0', 'UPrime2Mean_XY', '0', 'UPrime2Mean_YZ', '0', 'UPrime2Mean_XZ', '0', 'UPrime2Mean_Magnitude', '0']
plotOverLine3Display.SeriesLineStyle = ['arc_length', '1', 'nuSgs', '1', 'p', '1', 'U_X', '1', 'U_Y', '1', 'U_Z', '1', 'U_Magnitude', '1', 'U_0_X', '1', 'U_0_Y', '1', 'U_0_Z', '1', 'U_0_Magnitude', '1', 'UMean_X', '1', 'UMean_Y', '1', 'UMean_Z', '1', 'UMean_Magnitude', '1', 'UPrime2Mean_XX', '1', 'UPrime2Mean_YY', '1', 'UPrime2Mean_ZZ', '1', 'UPrime2Mean_XY', '1', 'UPrime2Mean_YZ', '1', 'UPrime2Mean_XZ', '1', 'UPrime2Mean_Magnitude', '1']
plotOverLine3Display.SeriesLineThickness = ['arc_length', '2', 'nuSgs', '2', 'p', '2', 'U_X', '2', 'U_Y', '2', 'U_Z', '2', 'U_Magnitude', '2', 'U_0_X', '2', 'U_0_Y', '2', 'U_0_Z', '2', 'U_0_Magnitude', '2', 'UMean_X', '2', 'UMean_Y', '2', 'UMean_Z', '2', 'UMean_Magnitude', '2', 'UPrime2Mean_XX', '2', 'UPrime2Mean_YY', '2', 'UPrime2Mean_ZZ', '2', 'UPrime2Mean_XY', '2', 'UPrime2Mean_YZ', '2', 'UPrime2Mean_XZ', '2', 'UPrime2Mean_Magnitude', '2']
plotOverLine3Display.SeriesMarkerStyle = ['arc_length', '0', 'nuSgs', '0', 'p', '0', 'U_X', '0', 'U_Y', '0', 'U_Z', '0', 'U_Magnitude', '0', 'U_0_X', '0', 'U_0_Y', '0', 'U_0_Z', '0', 'U_0_Magnitude', '0', 'UMean_X', '0', 'UMean_Y', '0', 'UMean_Z', '0', 'UMean_Magnitude', '0', 'UPrime2Mean_XX', '0', 'UPrime2Mean_YY', '0', 'UPrime2Mean_ZZ', '0', 'UPrime2Mean_XY', '0', 'UPrime2Mean_YZ', '0', 'UPrime2Mean_XZ', '0', 'UPrime2Mean_Magnitude', '0']

# save data
SaveData('/home/luz0a/OpenFOAM/luz0a-2.3.x/run/SwB/SwBd_L-400_20M_PISO/vel_test3.csv', proxy=plotOverLine3)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [0.0, 0.0, 1.7471957052005773]
renderView1.CameraFocalPoint = [0.0, 0.0, -0.019999995827674866]
renderView1.CameraParallelScale = 0.45738390384941197

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).