from vtkmodules.vtkCommonDataModel import (
    vtkStructuredGrid,
    vtkImageData,
    vtkPiecewiseFunction,
    vtkDataObject,
)
from vtkmodules.vtkIOXML import vtkXMLStructuredGridReader
from vtkmodules.vtkFiltersCore import vtkProbeFilter
from vtkmodules.vtkRenderingCore import (
    vtkVolumeProperty,
    vtkColorTransferFunction,
    vtkVolume,
)
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper


# pylint: disable=too-many-arguments
def create_image_data(data: vtkStructuredGrid):
    bounds = [round(x) for x in data.GetBounds()]
    spacing = (1.0, 1.0, 1.0)

    image_data = vtkImageData()
    image_data.SetExtent(bounds)
    image_data.SetSpacing(spacing)

    return image_data


def add_fire_volume(reader: vtkXMLStructuredGridReader):
    reader.Update()
    image_data = create_image_data(reader.GetOutput())

    probe_filter = vtkProbeFilter()
    probe_filter.SetInputData(image_data)
    probe_filter.SetSourceConnection(reader.GetOutputPort())
    probe_filter.Update()

    volumeProperty = vtkVolumeProperty()
    colorTransferFunction = vtkColorTransferFunction()
    opacityTransferFunction = vtkPiecewiseFunction()

    # flame
    colorTransferFunction.AddRGBPoint(400 - 1, 0, 0, 0)
    colorTransferFunction.AddRGBPoint(400, 0.45, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(500, 0.90, 0.0, 0.0)
    colorTransferFunction.AddRGBPoint(600, 1.00, 0.8, 0.0)
    colorTransferFunction.AddRGBPoint(700, 1.00, 1.0, 0.6)
    colorTransferFunction.AddRGBPoint(800, 1.00, 1.0, 1.0)
    colorTransferFunction.AddRGBPoint(800 + 1, 0, 0, 0)

    opacityTransferFunction.AddPoint(400 - 1, 0)
    opacityTransferFunction.AddPoint(400, 0.5)
    opacityTransferFunction.AddPoint(500, 0.6)
    opacityTransferFunction.AddPoint(600, 0.7)
    opacityTransferFunction.AddPoint(700, 0.8)
    opacityTransferFunction.AddPoint(800, 0.9)
    opacityTransferFunction.AddPoint(800 + 1, 0)

    # smoke
    colorTransferFunction.AddRGBPoint(310 - 1, 0, 0, 0)
    colorTransferFunction.AddRGBPoint(310, 0.96, 0.96, 0.96)
    colorTransferFunction.AddRGBPoint(310 + 1, 0, 0, 0)

    opacityTransferFunction.AddPoint(310 - 1, 0)
    opacityTransferFunction.AddPoint(310, 0.3)
    opacityTransferFunction.AddPoint(310 + 1, 0)

    volumeProperty.SetColor(colorTransferFunction)
    volumeProperty.SetScalarOpacity(opacityTransferFunction)
    volumeProperty.ShadeOn()
    volumeProperty.SetInterpolationTypeToLinear()

    volumeMapper = vtkGPUVolumeRayCastMapper()
    volumeMapper.SetInputConnection(probe_filter.GetOutputPort())
    volumeMapper.SetInputArrayToProcess(
        0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "theta"
    )
    volumeMapper.AutoAdjustSampleDistancesOff()
    volumeMapper.SetSampleDistance(0.1)

    volume = vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)

    return volume
