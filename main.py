import sys

from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QMainWindow,
    QPushButton,
    QSpinBox,
    QStyle,
    QVBoxLayout,
    QWidget,
)
from vtkmodules.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOXML import vtkXMLImageDataReader, vtkXMLStructuredGridReader
from vtkmodules.vtkRenderingCore import vtkRenderer

from src.data import (
    EXTRACTED_DIR,
    FILE_ID_MAX,
    FILE_ID_MIN,
    FILE_ID_STEP,
    IMAGE_DATA_DIR,
    to_filename,
)
from src.flame import get_flame_actors, get_flame_volume
from src.images import export_image, remove_images
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
layout = QVBoxLayout()

time_spin_box = QSpinBox()
time_spin_box.setRange(FILE_ID_MIN // FILE_ID_STEP, FILE_ID_MAX // FILE_ID_STEP)
time_spin_box.setSuffix("000")


def start_playback():
    # This is a blocking playback as we do not want to use multi-processing or asyncio
    # to complicate things.
    remove_images()

    while time_spin_box.value() < time_spin_box.maximum():
        time_spin_box.setValue(time_spin_box.value() + 1)
        time_spin_box.repaint()
        export_image(vtk_widget.GetRenderWindow(), f"{time_spin_box.value()}")  # type: ignore


play_button = QPushButton()
play_button.setIcon(app.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
play_button.clicked.connect(start_playback)

time_group_box_layout = QHBoxLayout()
time_group_box_layout.addWidget(time_spin_box, stretch=1)
time_group_box_layout.addWidget(play_button)

time_group_box = QGroupBox("Time")
time_group_box.setLayout(time_group_box_layout)

######## VTK Widget

vts_reader = vtkXMLStructuredGridReader()
vts_reader.SetFileName(str(EXTRACTED_DIR / to_filename(FILE_ID_MIN, extension="vts")))

vti_reader = vtkXMLImageDataReader()
vti_reader.SetFileName(str(IMAGE_DATA_DIR / to_filename(FILE_ID_MIN, extension="vti")))


def on_time_changed(value: str):
    vts_reader.SetFileName(
        str(EXTRACTED_DIR / to_filename(int(value), extension="vts"))
    )

    vti_reader.SetFileName(
        str(IMAGE_DATA_DIR / to_filename(int(value), extension="vti"))
    )

    vtk_widget.GetRenderWindow().Render()


time_spin_box.textChanged.connect(on_time_changed)

renderer = vtkRenderer()
vegetation_actor = get_vegetation_actor(vts_reader.GetOutputPort())
renderer.AddViewProp(vegetation_actor)
wind_actor, wind_scalar_bar, set_wind_color_by = get_wind_stream_actor(
    vts_reader.GetOutputPort()
)
renderer.AddViewProp(wind_actor)
renderer.AddViewProp(wind_scalar_bar)

flame_actors, flame_scalar_bar = get_flame_actors(vts_reader.GetOutputPort())
(
    flame_volume,
    flame_volume_scalar_bar,
    update_auto_adjust_sample_distances,
) = get_flame_volume(vti_reader.GetOutputPort())

renderer.AddViewProp(flame_scalar_bar)
for actor in flame_actors:
    renderer.AddViewProp(actor)

colors = vtkNamedColors()
renderer.SetBackground(colors.GetColor3d("SlateGray"))  # type: ignore

vtk_widget = QVTKRenderWindowInteractor(central)

# Depth Peeling
vtk_widget.GetRenderWindow().SetAlphaBitPlanes(True)
vtk_widget.GetRenderWindow().SetMultiSamples(0)
renderer.SetUseDepthPeeling(True)
renderer.SetMaximumNumberOfPeels(100)
renderer.SetOcclusionRatio(0.0)

vtk_widget.GetRenderWindow().AddRenderer(renderer)
vtk_widget.Initialize()


######## Layer Control


def on_vegetation_layer_changed(state: bool):
    if state:
        renderer.AddViewProp(vegetation_actor)
    else:
        renderer.RemoveViewProp(vegetation_actor)
    vtk_widget.GetRenderWindow().Render()


def on_wind_layer_changed(state: bool):
    if state:
        renderer.AddViewProp(wind_actor)
        renderer.AddViewProp(wind_scalar_bar)
    else:
        renderer.RemoveViewProp(wind_actor)
        renderer.RemoveViewProp(wind_scalar_bar)
    vtk_widget.GetRenderWindow().Render()


def on_flame_contour_layer_changed(state: bool):
    if state:
        renderer.AddViewProp(flame_scalar_bar)
        for a in flame_actors:
            renderer.AddViewProp(a)
    else:
        renderer.RemoveViewProp(flame_scalar_bar)
        for a in flame_actors:
            renderer.RemoveViewProp(a)
    vtk_widget.GetRenderWindow().Render()


def on_flame_volume_layer_changed(state: bool):
    if state:
        renderer.AddViewProp(flame_volume)
        renderer.AddViewProp(flame_volume_scalar_bar)
    else:
        renderer.RemoveViewProp(flame_volume)
        renderer.RemoveViewProp(flame_volume_scalar_bar)
    vtk_widget.GetRenderWindow().Render()


layers_config = (
    ("Vegetation", True, on_vegetation_layer_changed),
    ("Wind", True, on_wind_layer_changed),
    ("Flame (Contour)", True, on_flame_contour_layer_changed),
    ("Flame (Volume)", False, on_flame_volume_layer_changed),
)

layer_group_box = QGroupBox("Layers")
layer_group_box_layout = QHBoxLayout()
layer_group_box.setLayout(layer_group_box_layout)

for layer_name, is_checked, on_state_changed in layers_config:
    layer_checkbox = QCheckBox(layer_name)
    layer_checkbox.setChecked(is_checked)
    layer_checkbox.stateChanged.connect(on_state_changed)
    layer_group_box_layout.addWidget(layer_checkbox)


######## Switch Auto Adjust Volume Sample Distances


def on_auto_adjust_volume_sample_distances_changed(state: bool):
    update_auto_adjust_sample_distances(state)
    vtk_widget.GetRenderWindow().Render()


auto_adjust_volume_sample_distances_check_box = QCheckBox(
    "Auto Adjust Volume Sample Distances"
)
auto_adjust_volume_sample_distances_check_box.setChecked(True)
auto_adjust_volume_sample_distances_check_box.stateChanged.connect(
    on_auto_adjust_volume_sample_distances_changed
)

######## Wind Color Map


def on_wind_color_map_by_o2_changed(state: bool):
    if state:
        set_wind_color_by("O2")
    else:
        set_wind_color_by("wind")
    vtk_widget.GetRenderWindow().Render()


wind_color_map_by_o2_check_box = QCheckBox("Wind Color Map by O2")
wind_color_map_by_o2_check_box.setChecked(True)
wind_color_map_by_o2_check_box.stateChanged.connect(on_wind_color_map_by_o2_changed)


settings_group_box = QGroupBox("Settings")
settings_layout = QHBoxLayout()
settings_group_box.setLayout(settings_layout)
settings_layout.addWidget(auto_adjust_volume_sample_distances_check_box)
settings_layout.addWidget(wind_color_map_by_o2_check_box)

layout.addWidget(time_group_box)
layout.addWidget(layer_group_box)
layout.addWidget(settings_group_box)
layout.addWidget(vtk_widget)

central.setLayout(layout)
window.setCentralWidget(central)

window.show()
sys.exit(app.exec())
