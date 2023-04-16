import sys

from PySide6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOXML import vtkXMLStructuredGridReader
from vtkmodules.vtkRenderingCore import vtkRenderer

from src.data import EXTRACTED_DIR, FILE_ID_MIN, to_filename
from src.fire import add_flame_actor, add_smoke_actor
from src.temporal import build_temporal_gui
from src.vegetation import get_vegetation_actor
from src.vtk_side_effects import import_for_rendering_core, import_for_rendering_volume
from src.wind import get_wind_stream_actor
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
temporal_label, temporal_spinbox = build_temporal_gui()
layout.addWidget(temporal_label, 0, 0)
layout.addWidget(temporal_spinbox, 0, 1, 1, -1)

######## VTK Widget

reader = vtkXMLStructuredGridReader()
reader.SetFileName(str(EXTRACTED_DIR / to_filename(FILE_ID_MIN)))


def on_time_changed(value: str):
    reader.SetFileName(str(EXTRACTED_DIR / to_filename(int(value))))
    vtk_widget.GetRenderWindow().Render()


temporal_spinbox.textChanged.connect(on_time_changed)

renderer = vtkRenderer()
renderer.AddActor(get_vegetation_actor(reader.GetOutputPort()))
wind_actor, wind_scalar_bar = get_wind_stream_actor(reader.GetOutputPort())
renderer.AddActor(wind_actor)
renderer.AddActor2D(wind_scalar_bar)
add_flame_actor(reader.GetOutputPort(), renderer)
add_smoke_actor(reader.GetOutputPort(), renderer)

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
