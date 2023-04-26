from vtkmodules.vtkCommonColor import vtkNamedColors
from vtkmodules.vtkIOXML import vtkXMLImageDataReader, vtkXMLStructuredGridReader
from vtkmodules.vtkRenderingCore import (
    vtkRenderer,
    vtkRenderWindow,
    vtkRenderWindowInteractor,
)

from src.data import (
    EXTRACTED_DIR,
    FILE_ID_MAX,
    FILE_ID_MIN,
    FILE_ID_STEP,
    IMAGE_DATA_DIR,
    to_filename,
)
from src.flame import get_flame_actors
from src.vegetation import get_vegetation_actor
from src.vtk_side_effects import import_for_rendering_core, import_for_rendering_volume
from src.window import WINDOW_HEIGHT, WINDOW_WIDTH

import_for_rendering_core()
import_for_rendering_volume()


def print_camera_settings(renderer: vtkRenderer):
    camera = renderer.GetActiveCamera()
    print("Camera settings:")
    print(f"  * position:        {camera.GetPosition()}")
    print(f"  * focal point:     {camera.GetFocalPoint()}")
    print(f"  * up vector:       {camera.GetViewUp()}")
    print(f"  * clipping range:  {camera.GetClippingRange()}")


def play(
    window: vtkRenderWindow,
    vts_reader: vtkXMLStructuredGridReader,
    vti_reader: vtkXMLImageDataReader,
):
    for value in range(FILE_ID_MIN, FILE_ID_MAX + 1, FILE_ID_STEP):
        vts_reader.SetFileName(
            str(EXTRACTED_DIR / to_filename(int(value), extension="vts"))
        )

        vti_reader.SetFileName(
            str(IMAGE_DATA_DIR / to_filename(int(value), extension="vti"))
        )
        window.Render()


def key_pressed_callback(
    obj: vtkRenderWindowInteractor,
    _: str,
    renderer: vtkRenderer,
    window: vtkRenderWindow,
    vts_reader: vtkXMLStructuredGridReader,
    vti_reader: vtkXMLImageDataReader,
):
    key = obj.GetKeySym()
    if key == "c":
        print_camera_settings(renderer)
    elif key == "s":
        play(window, vts_reader, vti_reader)


def main():
    vts_reader = vtkXMLStructuredGridReader()
    vts_reader.SetFileName(
        str(EXTRACTED_DIR / to_filename(FILE_ID_MIN, extension="vts"))
    )

    vti_reader = vtkXMLImageDataReader()
    vti_reader.SetFileName(
        str(IMAGE_DATA_DIR / to_filename(FILE_ID_MIN, extension="vti"))
    )

    renderer = vtkRenderer()
    vegetation_actor = get_vegetation_actor(vts_reader.GetOutputPort())
    renderer.AddActor(vegetation_actor)

    flame_actors, _ = get_flame_actors(vts_reader.GetOutputPort())

    for actor in flame_actors:
        renderer.AddActor(actor)

    colors = vtkNamedColors()
    renderer.SetBackground(colors.GetColor3d("SlateGray"))  # type: ignore

    renderer.SetUseDepthPeeling(True)
    renderer.SetMaximumNumberOfPeels(100)
    renderer.SetOcclusionRatio(0.0)

    window = vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.AddObserver(
        "KeyPressEvent",  # type: ignore
        lambda obj, event: key_pressed_callback(
            obj, event, renderer, window, vts_reader, vti_reader
        ),
    )
    interactor.Initialize()

    interactor.Initialize()
    window.Render()
    interactor.Start()


if __name__ == "__main__":
    main()
