from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkCommonTransforms import vtkTransform
from vtkmodules.vtkFiltersFlowPaths import vtkStreamTracer
from vtkmodules.vtkFiltersGeneral import vtkTransformPolyDataFilter
from vtkmodules.vtkFiltersSources import vtkPointSource
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper


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

    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(streamline.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)

    return actor
