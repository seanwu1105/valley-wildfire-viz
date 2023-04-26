import pathlib

from vtkmodules.vtkIOImage import vtkPNGWriter
from vtkmodules.vtkRenderingCore import vtkRenderWindow, vtkWindowToImageFilter

IMAGES_DIR = pathlib.Path(__file__).parent.parent.resolve() / "images"


def export_image(render_window: vtkRenderWindow, filename: str):
    w2if = vtkWindowToImageFilter()
    w2if.SetInput(render_window)
    w2if.Update()

    writer = vtkPNGWriter()
    writer.SetFileName(str(IMAGES_DIR / f"{filename}.png"))
    writer.SetInputConnection(w2if.GetOutputPort())
    writer.Write()


def remove_images():
    for image in IMAGES_DIR.glob("*.png"):
        image.unlink()
