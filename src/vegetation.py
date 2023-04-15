from vtkmodules.vtkCommonDataModel import vtkDataObject
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkFiltersCore import vtkContourFilter
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkDataSetMapper,
)


def get_vegetation_actor(port: vtkAlgorithmOutput):
    contour = vtkContourFilter()
    contour.SetInputArrayToProcess(
        0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "rhof_1"
    )
    contour.SetInputConnection(port)
    contour.GenerateValues(3, 0.0, 1.0)

    ctf = vtkColorTransferFunction()
    ctf.AddHSVPoint(0.2, 38 / 360, 0.91, 0.49)
    ctf.AddHSVPoint(0.3, 120 / 360, 0.38, 0.69)
    ctf.AddHSVPoint(1.0, 120 / 360, 1, 0.41)

    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(contour.GetOutputPort())
    mapper.SetLookupTable(ctf)

    actor = vtkActor()
    actor.GetProperty().SetOpacity(0.75)
    actor.SetMapper(mapper)

    return actor
