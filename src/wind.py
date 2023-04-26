import typing

from vtkmodules.vtkCommonDataModel import vtkDataSetAttributes
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersCore import vtkAssignAttribute
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingAnnotation import vtkScalarBarActor
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkDataSetMapper,
)

from src.color_scales import BLACK_BLUE_WHITE
from src.window import WINDOW_WIDTH


def get_wind_stream_actor(port: vtkAlgorithmOutput):
    seeds = vtkPointSource()
    seeds.SetNumberOfPoints(100)

    transform = vtkTransform()
    transform.Translate(-90, 0, 140)
    transform.Scale(250, 250, 250)

    transformer = vtkTransformPolyDataFilter()
    transformer.SetInputConnection(seeds.GetOutputPort())
    transformer.SetTransform(transform)

    streamline = vtkStreamTracer()
    streamline.SetInputConnection(port)
    streamline.SetSourceConnection(transformer.GetOutputPort())
    streamline.SetMaximumPropagation(500)
    streamline.SetIntegrationDirectionToBoth()

    aa = vtkAssignAttribute()
    aa.SetInputConnection(streamline.GetOutputPort())

    lut_o2 = get_lut((0.227, 0.23))
    lut_magnitude = get_lut((0.0, 16))

    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(aa.GetOutputPort())
    mapper.UseLookupTableScalarRangeOn()

    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetMaximumWidthInPixels(WINDOW_WIDTH // 10)

    def set_color_by(color_by: typing.Literal["O2", "wind"]):
        aa.Assign(color_by, vtkDataSetAttributes.SCALARS, vtkAssignAttribute.POINT_DATA)
        if color_by == "O2":
            mapper.SetLookupTable(lut_o2)
            scalar_bar.SetTitle("O2 Concentration")
        elif color_by == "wind":
            mapper.SetLookupTable(lut_magnitude)
            scalar_bar.SetTitle("Wind Magnitude")
        scalar_bar.SetLookupTable(mapper.GetLookupTable())  # type: ignore

    set_color_by("O2")

    actor = vtkActor()
    actor.GetProperty().SetOpacity(0.5)
    actor.SetMapper(mapper)

    return actor, scalar_bar, set_color_by


def get_lut(lut_range: tuple[float, float]):
    num_steps = len(BLACK_BLUE_WHITE)
    step_size = (lut_range[1] - lut_range[0]) / (num_steps - 1)

    lut = vtkColorTransferFunction()
    for i, color in enumerate(BLACK_BLUE_WHITE):
        lut.AddRGBPoint(lut_range[0] + i * step_size, *color)

    return lut
