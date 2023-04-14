from PySide6.QtWidgets import QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOXML import vtkXMLStructuredGridReader
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper, vtkRenderer

from src.data import DATA_DIR, to_filename


def build_vtk_widget(parent: QWidget, init_time: int = 1000):
    reader = vtkXMLStructuredGridReader()
    reader.SetFileName(str(DATA_DIR / to_filename(init_time)))

    # Disable the arrays we don't need to save memory.
    reader.SetPointArrayStatus("u", 0)
    reader.SetPointArrayStatus("v", 0)
    reader.SetPointArrayStatus("w", 0)
    reader.SetPointArrayStatus("theta", 0)
    reader.SetPointArrayStatus("O2", 0)
    reader.SetPointArrayStatus("rhowatervapor", 0)
    reader.SetPointArrayStatus("rhof_1", 1)
    reader.SetPointArrayStatus("convht_1", 0)
    reader.SetPointArrayStatus("frhosiesrad_1", 0)

    mapper = vtkDataSetMapper()
    mapper.SetInputConnection(reader.GetOutputPort())

    actor = vtkActor()
    actor.SetMapper(mapper)

    renderer = vtkRenderer()
    renderer.AddActor(actor)
    colors = vtkNamedColors()
    renderer.SetBackground(colors.GetColor3d("SlateGray"))  # type: ignore

    widget = QVTKRenderWindowInteractor(parent)
    widget.GetRenderWindow().AddRenderer(renderer)
    widget.Initialize()

    return widget
