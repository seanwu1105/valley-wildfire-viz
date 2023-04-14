import sys

from PySide6.QtWidgets import QApplication, QGridLayout, QMainWindow, QWidget

from src.temporal import build_temporal_gui
from src.vtk_side_effects import import_for_rendering_core, import_for_rendering_volume
from src.vtk_widget import build_vtk_widget
from src.window import WINDOW_HEIGHT, WINDOW_WIDTH


# For simplicity, use GUI widgets to store the state of the application.
def build_gui():
    window = QMainWindow()
    window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    central = QWidget()
    layout = QGridLayout()
    layout.setColumnStretch(1, 1)

    temporal_label, temporal_gui = build_temporal_gui()
    layout.addWidget(temporal_label, 0, 0)
    layout.addWidget(temporal_gui, 0, 1, 1, -1)

    vtk_widget = build_vtk_widget(central)
    layout.addWidget(vtk_widget, 1, 0, 1, -1)

    central.setLayout(layout)
    window.setCentralWidget(central)
    return window


if __name__ == "__main__":
    import_for_rendering_core()
    import_for_rendering_volume()
    app = QApplication()
    gui = build_gui()
    gui.show()
    sys.exit(app.exec())
