import bpy
import bmesh

###########################################################
# [1] Microsoft Copilot, a language model provided code
# for create_shape.
def create_shape(mesh_name,object_name, V, E, F, T, R, S, RGBA):
    # Create a new mesh and object
    M1 = bpy.data.meshes.new(mesh_name)
    O1 = bpy.data.objects.new(object_name, M1)

    # Link the object to the scene collection
    bpy.context.collection.objects.link(O1)
    
    V2 = list(map(tuple, V))
    E2 = list(map(tuple, E))
    F2 = list(map(tuple, F))

    # Create the mesh from the data
    M1.from_pydata(V2, E2, F2)
    O1.scale = tuple(S)
    O1.location = tuple(T)
    O1.rotation_euler = tuple(R)

    # Update the mesh with new data
    M1.update()

    # Make the object active and select it
    bpy.context.view_layer.objects.active = O1
    O1.select_set(True)

    # Enter edit mode to see the mesh
    bpy.ops.object.mode_set(mode='EDIT')
    bpy.ops.object.mode_set(mode='OBJECT')
    
    ##################
    # Create a new material
    mat_name = f"{object_name}_mat"
    material = bpy.data.materials.new(name=mat_name)

    # Enable 'Use nodes'
    material.use_nodes = True

    # Get the material node tree
    node_tree = material.node_tree
    nodes = node_tree.nodes

    # Clear all nodes
    for node in nodes:
        nodes.remove(node)

    # Create an output node
    output_node = nodes.new(type='ShaderNodeOutputMaterial')
    output_node.location = (300, 0)

    # Create a diffuse shader node
    diffuse_node = nodes.new(type='ShaderNodeBsdfDiffuse')
    diffuse_node.location = (0, 0)

    # Set the RGB color
    diffuse_node.inputs['Color'].default_value = tuple(RGBA)  
        # RGB (R, G, B, Alpha)

    # Link the diffuse shader to the output node
    node_tree.links.new(diffuse_node.outputs['BSDF'], 
        output_node.inputs['Surface'])

    # Assign the material to the object
    if O1.data.materials:
        O1.data.materials[0] = material
    else:
        O1.data.materials.append(material)

    ##################

    # Optional: Smooth shading
    bmesh_data = bmesh.new()
    bmesh_data.from_mesh(M1)
    bmesh.ops.recalc_face_normals(bmesh_data, faces=bmesh_data.faces)
    bmesh_data.to_mesh(M1)
    bmesh_data.free()
    return
#
############################################################

###########################################################
# JGE code
import sys
sys.path.append(\
    r"C:/Users/jerry/Desktop/_Art/my_universes")
import universes
from copy import deepcopy
import universes.shapes.common.QuaternionGroup as cog
import universes.shapes.extrusion as ext
import universes.shapes.common.affine as aff
import universes.shapes.alg_topo as topo
import numpy as np

from math import sin,cos,pi,exp

import random

seed0 = 12345
random.seed(seed0)

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))


def create_bean(ns=30,nt=30,r_add = 0.25,freq=10,path=None):
    def f(s,t):
        w = 2*s - 1
        w = 2*w
        r = exp(-w**2/2)
        r2 = r*(1+r_add*(sin(2*pi*freq*s)+1)/2.0)
        x,z = [r2*cos(2*pi*t),r2*sin(2*pi*t)]
        pt = [x,0,z]
        return pt
    S = np.linspace(0,1,ns)
    T = np.linspace(0,1,nt)

    if path is None:
        path2 = []
    cross_sections = []
    a = 3
    b = 20
    omega = 2*pi
    def x1(t):
        x = a*cos(omega*t)
        return x
    def x2(t):
        y = a*sin(omega*t)
        return y
    def x3(t):
        z = b*t
        return z
    for i in range(len(S)):
        s = S[i]
        cross_section = list(map(lambda t: f(s,t), T))
        C = aff.Center(cross_section)
        x = x1(s)
        y = x2(s)
        z = x3(s)
        pt_axis = [x,y,z] # [Edwards and Penney]
        if path is None:
            path2.append(pt_axis)
        cross_sections.append(cross_section)
    G = topo.AT_Cylinder(path2, cross_sections,
        bcap=True,ecap=True,closed=False)
    return G

def Random_color():
    R = random.uniform(0,1)
    G = random.uniform(0,1)
    B = random.uniform(0,1)
    A = 1
    return [R,G,B,A]

def Random_rotation():
    rx = random.uniform(-180,180)
    ry = random.uniform(-180,180)
    rz = random.uniform(-180,180)
    R = [rx,ry,rz]
    return R

G = create_bean(ns=30,nt=30,r_add = 0.25,freq=10,path=None)

# Define vertices, edges, and faces
V = [(1, 1, 0), (1, -1, 0), (-1, -1, 0), (-1, 1, 0)]
E = [(0,1),(1,2),(2,0)]
F = [(0,1,2)]
V = deepcopy(G['pts'])
E = deepcopy(G['E'])
F = deepcopy(G['F'])
for i in range(4):
    x = 6*(i/4 - 0.5)
    for j in range(4):
        y = 6*(j/4 - 0.5)
        T = [x,y,1]
        #R = [45,20,0]
        R = Random_rotation()
        S = [.125,.125,.125]
        RGBA = Random_color()
        name = f"bean_{i}_{j}"
        create_shape(f"M_{name}",f"O_{name}", V, E, F, T, R, S, RGBA)