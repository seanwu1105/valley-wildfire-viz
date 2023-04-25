from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonDataModel import vtkPiecewiseFunction
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkDataSetMapper,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import vtkGPUVolumeRayCastMapper

from src.window import WINDOW_WIDTH


def get_flame_volume(port: vtkAlgorithmOutput):
    volume_property = vtkVolumeProperty()
    color_transfer_function = vtkColorTransferFunction()
    opacity_transfer_function = vtkPiecewiseFunction()

    # flame
    color_transfer_function.AddRGBPoint(400, 0.45, 0.0, 0.0)
    color_transfer_function.AddRGBPoint(500, 0.90, 0.0, 0.0)
    color_transfer_function.AddRGBPoint(600, 1.00, 0.8, 0.0)
    color_transfer_function.AddRGBPoint(700, 1.00, 1.0, 0.6)
    color_transfer_function.AddRGBPoint(800, 1.00, 1.0, 1.0)

    opacity_transfer_function.AddPoint(400 - 1, 0)
    opacity_transfer_function.AddPoint(400, 0.5)
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

    def update_auto_adjust_sample_distances(value: bool):
        if value:
            volume_mapper.AutoAdjustSampleDistancesOn()
        else:
            volume_mapper.AutoAdjustSampleDistancesOff()
            volume_mapper.SetSampleDistance(0.1)

    volume = vtkVolume()
    volume.SetMapper(volume_mapper)
    volume.SetProperty(volume_property)

    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetLookupTable(color_transfer_function)
    scalar_bar.SetTitle("Temperature (K)")
    scalar_bar.SetMaximumWidthInPixels(WINDOW_WIDTH // 10)
    scalar_bar.SetPosition(0.2, 0.1)

    return volume, scalar_bar, update_auto_adjust_sample_distances


def get_flame_actors(port: vtkAlgorithmOutput):
    isosurfaces = [
        # flame
        [400, 0.45, 0.0, 0.0, 0.5],
        [500, 0.90, 0.0, 0.0, 0.6],
        [600, 1.00, 0.8, 0.0, 0.7],
        [700, 1.00, 1.0, 0.6, 0.8],
        [800, 1.00, 1.0, 1.0, 0.9],
        # smoke
        [310, 0.96, 0.96, 0.96, 0.3],
    ]

    color_transfer_function = vtkColorTransferFunction()
    for isovalue, r, g, b, _ in isosurfaces:
        color_transfer_function.AddRGBPoint(isovalue, r, g, b)
    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetLookupTable(color_transfer_function)
    scalar_bar.SetTitle("Temperature (K)")
    scalar_bar.SetMaximumWidthInPixels(WINDOW_WIDTH // 10)
    scalar_bar.SetPosition(0.05, 0.1)

    return (
        tuple(build_contours_actor(port, *param) for param in isosurfaces),
        scalar_bar,
    )


# pylint: disable=too-many-arguments
def build_contours_actor(
    port: vtkAlgorithmOutput,
    isovalue: float,
    r: float,
    g: float,
    b: float,
    alpha: float,
):
    contours = vtkContourFilter()
    contours.SetInputConnection(port)
    contours.SetValue(0, isovalue)

    lut = vtkLookupTable()
    lut.SetNumberOfTableValues(1)
    lut.SetTableValue(0, r, g, b, alpha)
    lut.Build()

    mapper = vtkDataSetMapper()
    mapper.SetLookupTable(lut)
    mapper.SetInputConnection(contours.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(alpha)

    return actor
