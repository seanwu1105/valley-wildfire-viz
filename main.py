import sys

from PySide6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOXML import vtkXMLStructuredGridReader
from vtkmodules.vtkRenderingCore import vtkActor, vtkDataSetMapper, vtkRenderer

from src.data import DATA_DIR, FILE_ID_MIN, to_filename
from src.temporal import build_temporal_gui
from src.vtk_side_effects import import_for_rendering_core, import_for_rendering_volume
from src.window import WINDOW_HEIGHT, WINDOW_WIDTH

import_for_rendering_core()
import_for_rendering_volume()

# I intentionally put everything related to VTK in the global scope as the VTK Python
# wrapper sucks. Sometimes, it throws a segfault if you wrap some of the code in a
# function. It seems to be a problem with the garbage collector. Thus, until the project
# is feature complete, I suggest we keep everything related to VTK in the global scope
# though it's ugly.

app = QApplication()

window = QMainWindow()
window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
central = QWidget()
layout = QGridLayout()
layout.setColumnStretch(1, 1)
temporal_label, temporal_gui = build_temporal_gui()
layout.addWidget(temporal_label, 0, 0)
layout.addWidget(temporal_gui, 0, 1, 1, -1)

######## VTK Widget

reader = vtkXMLStructuredGridReader()
reader.SetFileName(str(DATA_DIR / to_filename(FILE_ID_MIN)))

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

vtk_widget = QVTKRenderWindowInteractor(central)
vtk_widget.GetRenderWindow().AddRenderer(renderer)
vtk_widget.Initialize()

######## VTK Widget End

layout.addWidget(vtk_widget, 1, 0, 1, -1)

central.setLayout(layout)
window.setCentralWidget(central)

window.show()
sys.exit(app.exec())
