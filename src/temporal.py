from PySide6.QtWidgets import QLabel, QSpinBox

from src.data import FILE_ID_MAX, FILE_ID_MIN, FILE_ID_STEP


def build_temporal_gui():
    spin_box = QSpinBox()
    spin_box.setRange(FILE_ID_MIN // FILE_ID_STEP, FILE_ID_MAX // FILE_ID_STEP)
    spin_box.setSuffix("000")

    return QLabel("Time"), spin_box
