import vtk

def create_layer(port, isovalue, r, g, b, alpha):
    contours = vtk.vtkContourFilter()
    contours.SetInputConnection(port);
    contours.SetValue(0, isovalue)

    lut = vtk.vtkLookupTable()
    lut.SetNumberOfTableValues(1)
    lut.SetTableValue(0, r, g, b, alpha)
    lut.Build()
    
    mapper = vtk.vtkDataSetMapper()
    mapper.SetLookupTable(lut)
    mapper.SetInputConnection(contours.GetOutputPort())
    
    actor = vtk.vtkActor()
    actor.SetMapper(mapper)
    actor.GetProperty().SetOpacity(alpha)
    
    return actor

def add_flame_actor(port, renderer):
    isosurfaces = [
                   [400,0.2,0,0,0.7],
                   [500,0.4,0,0,0.7],
                   [600,0.6,0,0,0.7],
                   [700,0.8,0,0,0.7],
                   [800,1.0,0,0,0.7],
                   ]
                   
    for param in isosurfaces:
        actor = create_layer(port, *param)
        renderer.AddActor(actor)
        
def add_smoke_actor(port, renderer):
    isosurfaces = [
                   [350,1,1,1,0.5],
                   ]
                   
    for param in isosurfaces:
        actor = create_layer(port, *param)
        renderer.AddActor(actor)