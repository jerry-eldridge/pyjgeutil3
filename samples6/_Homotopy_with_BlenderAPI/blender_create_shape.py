import bpy
import bmesh

#############################################################################
# [1] Microsoft Copilot, a language model provided code
# for create_shape.
#
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
    return O1
#
# end microsoft copilot code
############################################################
