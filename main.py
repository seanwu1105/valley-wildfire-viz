import sys

from PySide6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkCommonDataModel import (
    vtkDataObject,
    vtkPiecewiseFunction,
    vtkPlanes,
    vtkPointData,
    vtkStructuredGrid,
)
from vtkmodules.vtkCommonExecutionModel import vtkAlgorithmOutput
from vtkmodules.vtkFiltersCore import vtkClipPolyData, vtkContourFilter
from vtkmodules.vtkIOXML import vtkXMLStructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkActor,
    vtkColorTransferFunction,
    vtkDataSetMapper,
    vtkRenderer,
    vtkVolume,
    vtkVolumeProperty,
)
from vtkmodules.vtkRenderingVolume import (
    vtkFixedPointVolumeRayCastMapper,
    vtkGPUVolumeRayCastMapper,
)
from vtkmodules.vtkRenderingVolumeOpenGL2 import vtkSmartVolumeMapper

from src.data import DATA_DIR, to_filename
from src.temporal import build_temporal_gui
from src.vtk_side_effects import import_for_rendering_core, import_for_rendering_volume
from src.window import WINDOW_HEIGHT, WINDOW_WIDTH

# For simplicity, use GUI widgets to store the state of the application.
# def build_gui():
#     window = QMainWindow()
#     window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
#     central = QWidget()
#     layout = QGridLayout()
#     layout.setColumnStretch(1, 1)

#     temporal_label, temporal_gui = build_temporal_gui()
#     layout.addWidget(temporal_label, 0, 0)
#     layout.addWidget(temporal_gui, 0, 1, 1, -1)

#     vtk_widget = build_vtk_widget(central)
#     layout.addWidget(vtk_widget, 1, 0, 1, -1)

#     central.setLayout(layout)
#     window.setCentralWidget(central)
#     return window


import_for_rendering_core()
import_for_rendering_volume()
app = QApplication()

window = QMainWindow()
window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
central = QWidget()
layout = QGridLayout()
layout.setColumnStretch(1, 1)
temporal_label, temporal_gui = build_temporal_gui()
layout.addWidget(temporal_label, 0, 0)
layout.addWidget(temporal_gui, 0, 1, 1, -1)

reader = vtkXMLStructuredGridReader()
reader.SetFileName(str(DATA_DIR / to_filename(1000)))

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

reader.Update()
output: vtkStructuredGrid = reader.GetOutput()  # type: ignore
point_data: vtkPointData = output.GetPointData()  # type: ignore
point_data.SetActiveScalars("rhof_1")

reader.Update()
print(reader.GetOutput())  # type: ignore


# mapper = vtkSmartVolumeMapper()
# mapper.SetInputConnection(reader.GetOutputPort())
# mapper.SetInputArrayToProcess(0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "rhof_1")

# mapper.Update()


# ctf = vtkColorTransferFunction()
# ctf.AddRGBPoint(0.0, 97 / 255, 255 / 255, 136 / 255)
# ctf.AddRGBPoint(1.0, 0 / 255, 102 / 255, 0 / 255)

# volume_property = vtkVolumeProperty()
# volume_property.ShadeOn()
# volume_property.SetInterpolationTypeToLinear()
# volume_property.SetColor(ctf)

# volume = vtkVolume()
# volume.SetMapper(mapper)
# volume.SetProperty(volume_property)

contour = vtkContourFilter()
contour.SetInputConnection(reader.GetOutputPort())
contour.Update()
print(contour.GetInput())  # type: ignore
# contour.SetInputArrayToProcess(
#     0, 0, 0, vtkDataObject.FIELD_ASSOCIATION_POINTS, "rhof_1"
# )
contour.SetValue(0, 0.5)

mapper = vtkDataSetMapper()
mapper.SetInputConnection(contour.GetOutputPort())

actor = vtkActor()
actor.SetMapper(mapper)

renderer = vtkRenderer()
renderer.AddActor(actor)
# renderer.AddVolume(volume)
colors = vtkNamedColors()
renderer.SetBackground(colors.GetColor3d("SlateGray"))  # type: ignore

vtk_widget = QVTKRenderWindowInteractor(central)
vtk_widget.GetRenderWindow().AddRenderer(renderer)
vtk_widget.Initialize()

layout.addWidget(vtk_widget, 1, 0, 1, -1)
central.setLayout(layout)
window.setCentralWidget(central)
gui = window

gui.show()
sys.exit(app.exec())
