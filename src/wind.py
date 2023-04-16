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
    aa.Assign("O2", vtkDataSetAttributes.SCALARS, vtkAssignAttribute.POINT_DATA)

    lut = vtkColorTransferFunction()
    lut_range = (0.227, 0.23)
    num_steps = len(BLACK_BLUE_WHITE)
    step_size = (lut_range[1] - lut_range[0]) / (num_steps - 1)
    for i, color in enumerate(BLACK_BLUE_WHITE):
        lut.AddRGBPoint(lut_range[0] + i * step_size, *color)

    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(aa.GetOutputPort())
    mapper.UseLookupTableScalarRangeOn()
    mapper.SetLookupTable(lut)

    scalar_bar = vtkScalarBarActor()
    scalar_bar.SetLookupTable(mapper.GetLookupTable())  # type: ignore

    actor = vtkActor()
    actor.GetProperty().SetOpacity(0.5)
    actor.SetMapper(mapper)

    return actor, scalar_bar
