from vtkmodules.vtkCommonCore import vtkLookupTable
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper, vtkRenderer


# pylint: disable=too-many-arguments
def create_layer(
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


def add_flame_actor(port: vtkAlgorithmOutput, renderer: vtkRenderer):
    isosurfaces = [
        [400, 0.45, 0.0, 0.0, 0.5],
        [500, 0.90, 0.0, 0.0, 0.6],
        [600, 1.00, 0.8, 0.0, 0.7],
        [700, 1.00, 1.0, 0.6, 0.8],
        [800, 1.00, 1.0, 1.0, 0.9],
    ]

    for param in isosurfaces:
        actor = create_layer(port, *param)
        renderer.AddActor(actor)


def add_smoke_actor(port: vtkAlgorithmOutput, renderer: vtkRenderer):
    isosurfaces = [
        [310, 0.96, 0.96, 0.96, 0.3],
    ]

    for param in isosurfaces:
        actor = create_layer(port, *param)
        renderer.AddActor(actor)
