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
from src.flame import get_flame_actors  # , get_flame_volume
from src.vegetation import get_vegetation_actor
from src.vtk_side_effects import import_for_rendering_core, import_for_rendering_volume

# from src.wind import get_wind_stream_actor
from src.window import WINDOW_HEIGHT, WINDOW_WIDTH

import_for_rendering_core()
import_for_rendering_volume()


def print_camera_settings(renderer: vtkRenderer):
    camera = renderer.GetActiveCamera()
    print("Camera settings:")
    print("  * position:        %s" % (camera.GetPosition(),))
    print("  * focal point:     %s" % (camera.GetFocalPoint(),))
    print("  * up vector:       %s" % (camera.GetViewUp(),))
    print("  * clipping range:  %s" % (camera.GetClippingRange(),))


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
    event: str,
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
    # wind_actor, wind_scalar_bar = get_wind_stream_actor(vts_reader.GetOutputPort())
    # renderer.AddActor(wind_actor)
    # renderer.AddActor(wind_scalar_bar)

    flame_actors, _ = get_flame_actors(vts_reader.GetOutputPort())
    # (
    # flame_volume,
    # _,
    # update_auto_adjust_sample_distances,
    # ) = get_flame_volume(vti_reader.GetOutputPort())

    # renderer.AddActor(flame_scalar_bar)

    for actor in flame_actors:
        renderer.AddActor(actor)

    colors = vtkNamedColors()
    renderer.SetBackground(colors.GetColor3d("SlateGray"))  # type: ignore

    renderer.SetUseDepthPeeling(True)
    renderer.SetMaximumNumberOfPeels(100)
    renderer.SetOcclusionRatio(0.0)

    # renderer.GetActiveCamera().SetPosition(-423.45965077898506, 747.431780358385, -479.8084945259253)
    # renderer.GetActiveCamera().SetFocalPoint(239.0, 360.1801300048828, 59.0)
    # renderer.GetActiveCamera().SetViewUp(0.6080162809740067, -0.06123356946813224, -0.7915596326498271)
    # renderer.GetActiveCamera().SetClippingRange(393.18430301265687, 1625.2139188614644)

    window = vtkRenderWindow()
    window.AddRenderer(renderer)
    window.SetSize(WINDOW_WIDTH, WINDOW_HEIGHT)

    interactor = vtkRenderWindowInteractor()
    interactor.SetRenderWindow(window)
    interactor.AddObserver(
        "KeyPressEvent",
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
