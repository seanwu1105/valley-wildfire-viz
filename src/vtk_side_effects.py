# pylint: disable=unused-import import-outside-toplevel
# pyright: reportUnusedImport=false


def import_for_rendering_core():
    import vtkmodules.vtkInteractionStyle
    import vtkmodules.vtkRenderingFreeType
    import vtkmodules.vtkRenderingOpenGL2


def import_for_rendering_volume():
    import vtkmodules.vtkRenderingVolumeOpenGL2
