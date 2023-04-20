from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper


def add_fire_volume(port: vtkAlgorithmOutput):
    volume_property = vtkVolumeProperty()
    color_transfer_function = vtkColorTransferFunction()
    opacity_transfer_function = vtkPiecewiseFunction()

    # flame
    color_transfer_function.AddRGBPoint(400 - 1, 0, 0, 0)
    color_transfer_function.AddRGBPoint(400, 0.45, 0.0, 0.0)
    color_transfer_function.AddRGBPoint(500, 0.90, 0.0, 0.0)
    color_transfer_function.AddRGBPoint(600, 1.00, 0.8, 0.0)
    color_transfer_function.AddRGBPoint(700, 1.00, 1.0, 0.6)
    color_transfer_function.AddRGBPoint(800, 1.00, 1.0, 1.0)
    color_transfer_function.AddRGBPoint(800 + 1, 0, 0, 0)

    opacity_transfer_function.AddPoint(400 - 1, 0)
    opacity_transfer_function.AddPoint(400, 0.5)
    opacity_transfer_function.AddPoint(500, 0.6)
    opacity_transfer_function.AddPoint(600, 0.7)
    opacity_transfer_function.AddPoint(700, 0.8)
    opacity_transfer_function.AddPoint(800, 0.9)
    opacity_transfer_function.AddPoint(800 + 1, 0)

    # smoke
    color_transfer_function.AddRGBPoint(310 - 1, 0, 0, 0)
    color_transfer_function.AddRGBPoint(310, 0.96, 0.96, 0.96)
    color_transfer_function.AddRGBPoint(310 + 1, 0, 0, 0)

    opacity_transfer_function.AddPoint(310 - 1, 0)
    opacity_transfer_function.AddPoint(310, 0.3)
    opacity_transfer_function.AddPoint(310 + 1, 0)

    volume_property.SetColor(color_transfer_function)
    volume_property.SetScalarOpacity(opacity_transfer_function)
    volume_property.ShadeOn()
    volume_property.SetInterpolationTypeToLinear()

    volume_mapper = vtkGPUVolumeRayCastMapper()
    volume_mapper.SetInputConnection(port)
    volume_mapper.AutoAdjustSampleDistancesOff()
    volume_mapper.SetSampleDistance(0.1)

    volume = vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)

    return volume
