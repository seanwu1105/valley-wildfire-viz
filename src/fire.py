import vtk


# pylint: disable=too-many-arguments
def get_flame_volume(port: vtk.vtkAlgorithmOutput):
    # Extract the geometry from the structured grid dataset
    geometryFilter = vtk.vtkStructuredGridGeometryFilter()
    geometryFilter.SetInputConnection(port)
    geometryFilter.Update()

    # Create an unstructured grid dataset from the extracted geometry
    unstructuredGrid = vtk.vtkUnstructuredGrid()
    unstructuredGrid.ShallowCopy(geometryFilter.GetOutput())

    # print(unstructuredGrid.GetPointData().GetScalars().GetRange())
    # Create a vtkUnstructuredGridVolumeRayCastMapper
    mapper = vtk.vtkUnstructuredGridVolumeRayCastMapper()
    mapper.SetInputData(unstructuredGrid)

    # Create vtkVolumeProperty
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.ShadeOff()  # Disable shading

    # Set the color transfer function
    colorTransferFunction = vtk.vtkColorTransferFunction()
    colorTransferFunction.AddRGBPoint(400 - 1, 0, 0, 0)
    colorTransferFunction.AddRGBPoint(400, 0.5, 0, 0)
    colorTransferFunction.AddRGBPoint(800, 1, 0, 0)
    colorTransferFunction.AddRGBPoint(800 + 1, 0, 0, 0)
    volumeProperty.SetColor(colorTransferFunction)

    # Set the opacity transfer function
    opacityTransferFunction = vtk.vtkPiecewiseFunction()
    opacityTransferFunction.AddPoint(400 - 1, 0)
    opacityTransferFunction.AddPoint(400, 0.5)
    opacityTransferFunction.AddPoint(800, 0.7)
    opacityTransferFunction.AddPoint(800 + 1, 0)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)

    # Create vtkVolume
    volume = vtk.vtkVolume()
    volume.SetMapper(mapper)
    volume.SetProperty(volumeProperty)

    return volume
