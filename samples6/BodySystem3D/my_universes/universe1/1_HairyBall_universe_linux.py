import sys
sys.path.append("/home/bolligfun/Universes/")
import universes
import universes.scene_object as so
import universes.shapes.primitives as ps

BIGDATA = r"/home/bolligfun/Universes/universe1/my_scenes/"

Sce = so.Scene()

# Sce.add adds the graph G to the scene and it
# also selects the object graph just added, but
# below we explicitly select each object for clarity.
# Select a shape before a transform else last
# selection will be used.

G = ps.create_hairy_ball(nfibers=150)
Sce.add(G,"HairyBall")
Sce.select("HairyBall")
T = [-0.38344, 112.793, 3.02941]
R = [-108.81, 0, 0]
S = [11.552, 9.568, 9.501]
Sce.transform(T,R,S)
T = [-4.6343, 15.642, 2.219]
Pivot = [-1.898, 109.087, -1.972]
R = [0,0,0]
S = [1,1,1]
Sce.transform(T,R,S,Pivot)

# Create and Position floor
G = ps.create_cube()
Sce.add(G,"floor")
Sce.select("floor")
T = [-4.37696, -6.88287, 0.0]
R = [0,0,0]
S = [8.328, 0.212, 14.092]
Sce.transform(T,R,S)

# Create and Position camera1_shape
G = ps.create_cube()
Sce.add(G,"camera1_shape")
Sce.select("camera1_shape")
T = [ -433.88, 192.63, -736.52]
R = [ 0.99142, -147.796, -2.37719]
S = [0.96449, 0.96449, 0.96449]
Sce.transform(T,R,S)

# Create and Position Wall_L
G = ps.create_cube()
Sce.add(G,"Wall_L")
Sce.select("Wall_L")
T = [403.975, 164.510, -11.869]
R = [0,0,0]
S = [0.184, 3.310, 14.497]
Sce.transform(T,R,S)

# Create and Position Wall_R
G = ps.create_cube()
Sce.add(G,"Wall_R")
Sce.select("Wall_R")
T = [-5.966, 168.664, 700.511]
R = [0,0,0]
S = [8.281, 3.303, 0.200]
Sce.transform(T,R,S)

# Create and Position RoomLight
G = ps.create_cube()
Sce.add(G,"RoomLight")
Sce.select("RoomLight")
T = [216.230, 136.029, -328.001]
R = [0,0,0]
S = [.5,.5,.5]
Sce.transform(T,R,S)

# Create and Position Cube_Of_Enlightment
G = ps.create_cube()
Sce.add(G,"Cube_Of_Enlightment")
Sce.select("Cube_Of_Enlightment")
T = [-245.906, 58.589, 154.687]
R = [0,0,0]
S = [1,1,2.223] # [1, 1, 2.223]
Sce.transform(T,R,S)

# Create and Position DomeLight
G = ps.create_cube()
Sce.add(G,"DomeLight")
Sce.select("DomeLight")
T = [0,0,0]
R = [270,0,0]
S = [.5,.5,.5]
Sce.transform(T,R,S)

# Create and Position RoomCeilingLight
G = ps.create_cube()
Sce.add(G,"RoomCeilingLight")
Sce.select("RoomCeilingLight")
T = [-11.765, 303.413, -89.231]
R = [-87.468, 0, 0]
S = [.5,.5,.2]
Sce.transform(T,R,S)

# Create and Position CylinderBody (this
# cylinder model could be improved upon)
G = ps.create_cylinder()
Sce.add(G,"CylinderBody")
Sce.select("CylinderBody")
T = [179.095, 110.551, -183.738]
R = [0,0,0]
S = [0.475, 2.106, 0.372]
Sce.transform(T,R,S)

# Create and Position Ceiling
G = ps.create_cube()
Sce.add(G,"Ceiling")
Sce.select("Ceiling")
T = [0, 323.252, -13.058]
R = [0,0,0]
S = [8.378, 0.216, 14.494]
Sce.transform(T,R,S)

#################################

fn_save = BIGDATA+"HairyBallScene-03.obj"
Sce.save(fn_save)

# Double-Click on OBJ file
import os
#os.system(fn_save)
