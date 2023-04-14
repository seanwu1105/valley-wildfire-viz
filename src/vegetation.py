from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkRenderingCore import (
    vtkColorTransferFunction,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkSmartVolumeMapper


def build_vegetation_volume(port: vtkAlgorithmOutput):
    mapper = vtkSmartVolumeMapper()
    mapper.SetInputConnection(port)

    ctf = vtkColorTransferFunction()
    ctf.AddRGBPoint(0.0, 97 / 255, 255 / 255, 136 / 255)
    ctf.AddRGBPoint(1.0, 0 / 255, 102 / 255, 0 / 255)

    volume_property = vtkVolumeProperty()
    volume_property.ShadeOn()
    volume_property.SetInterpolationTypeToLinear()
    volume_property.SetColor(ctf)

    volume = vtkVolume()
    volume.SetMapper(mapper)
    # volume.SetProperty(volume_property)

    return volume
