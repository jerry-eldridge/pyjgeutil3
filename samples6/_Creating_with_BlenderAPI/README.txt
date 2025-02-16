README.txt

See the folder ../Beans/ which we use for this.
This is an experimental folder where we use 
my_universes library to create a graph G = (V,E,pts,F,N)
where V are vertex indices, E are edges, pts are
geometry points, F are faces, and N are normals.
An edge e in E is e = [u,v] for u,v in V. And
pts[v] is the point for vertex index v. The faces
f in F are triangulated in my_universes and I needed
to modify extrusion.py so that tripy.py was not used
as that is not imported as a library in Blender API python.
N are normals N[v]. The faces are a list of three
vertices mostly to simplify the explanation a little.

For Blender API, it calls pts the name V so
we use a Microsoft Copilot generated code (a large
language model is Copilot) for converting G into
a scene object.

The script create_beans.py is run within Blender, a free 3D 
modeling animation and rendering software, available
online. One navigates to Blender > Scripting and runs
create_beans.py with it pointing to the location of
my_universes library which is at jgeutil github and making
sure to add lights and there be a camera to the scene
and the camera is pointing to the beans.

 