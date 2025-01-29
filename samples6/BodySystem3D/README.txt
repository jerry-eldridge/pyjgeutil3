README

This script creates bodysystem_3d.obj  in this directory 
using the 2_BodySystem3D_graphics.py python3 script.

The .mtl are material files. The .obj is an Alias Wavefront
.obj 3D model file containing a simplicial complex
made of 0-simplices (points or vertices 'v') and 2-simplices
(triangles or faces 'f') and there are also vertex normals
or the sort of "up direction" to "ground" where a triangle
face defines the local ground plane (normals 'vn').
There are optionally texture coordinates in an .obj file
(texture uvs 'vt') where a mapping from image space
im : [0,1] x [0,1] -> color where im(u,v) = color so
'vt <u> <v>' specifies such a map for the i-th vt to
the j-th v in the face 'f 1/2/3 ...' where 1 is v vertex index,
2 is vt texture coordinate index (u,v) and 3 denotes vn
normal index. The indices start at 1.

In the material .mtl file, there is a material name. That
name is used in the .obj file with "mtllib <filename>.mtl"
and later before faces 'f's with "usemtl <material_name>"
with <material_name> defined in <filename>.mtl. Several
materials can be used. Also there are also possible group 'g'
and object 'o' specification followed by a name 'g <name>'
or 'o <name>'.


