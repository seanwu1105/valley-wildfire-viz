import sys

from PySide6.QtWidgets import QApplication, QGridLayout, QLabel, QMainWindow, QWidget

from src.vtk_side_effects import import_for_rendering_core
from src.window import WINDOW_HEIGHT, WINDOW_WIDTH


# For simplicity, use GUI widgets to store the state of the application.
def build_gui():
    window = QMainWindow()
    window.resize(WINDOW_WIDTH, WINDOW_HEIGHT)
    central = QWidget()
    layout = QGridLayout()

    vtk_widget = build_vtk_widget(central)
    layout.addWidget(vtk_widget, 0, 0, 1, -1)

    central.setLayout(layout)
    window.setCentralWidget(central)
    return window


def build_vtk_widget(parent: QWidget):
    widget = QLabel("this is a placeholder for vtk widget", parent)
    return widget


if __name__ == "__main__":
    import_for_rendering_core()
    app = QApplication()
    gui = build_gui()
    gui.show()
    sys.exit(app.exec())
