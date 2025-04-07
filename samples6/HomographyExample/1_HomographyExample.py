import cv2
import numpy as np

from math import pi,cos,sin

##################################################
# JGE: vectors.py
#
# [1] "OpenGL Programming Guide", 7ed, Shreiner
# (rotation matrix, frustrum matrix)
#
def rotation_matrix(degrees,x,y,z):
##    """
##    4x4 rotation matrix for axis [x,y,z] rotated by angle, degrees
##    called R, then an extended coordinate X = [x0,x1,x2,1] is
##    XP = R*X and rotated point is [XP[0],XP[1],XP[2]].
##    """
    v = np.array([[x,y,z]]).T
    u = v/np.linalg.norm(v)
    S = np.array([
        [0,-u[2,0],u[1,0]],
        [u[2,0],0,-u[0,0]],
        [-u[1,0],u[0,0],0]])
    I = np.array([
        [1,0,0],
        [0,1,0],
        [0,0,1]])
    uu = u @ u.T
    M = uu+cos(degrees*pi/180)*(I-uu)+\
        sin(degrees*pi/180)*S
    R = np.zeros((4,4),dtype="float")
    R[:3,:3]=M
    R[3,3] = 1
    return R

def translation_matrix(x,y,z):
##    """
##    4x4 translation matrix that maps a point pt from
##    pt[0] += x
##    pt[1] += y
##    pt[2] += z
##    pt[3] = pt[3] # w = 1
##    """
    T = np.eye(4,4,dtype="float")
    T[0,3] = x
    T[1,3] = y
    T[2,3] = z
    T[3,3] = 1
    return T

def scale_matrix(sx,sy,sz):
##    """
##    4x4 scale matrix that scales a point pt
##    x = sx*x
##    y = sy*y
##    z = sz*z
##    w = 1
##    """
    T = np.eye(4,4,dtype="float")
    T[0,0] = sx
    T[1,1] = sy
    T[2,2] = sz
    T[3,3] = 1
    return T

# perspective
def camera_matrix(f,cx,cy):
    T = np.zeros((3,4),dtype="float")
    T[0,0] = f
    T[1,1] = f
    T[2,2] = 1
    T[0,3] = cx
    T[1,3] = cy
    return T

def transform1(tri):
    tri_a = [pt+[1] for pt in tri]
    tri1 = np.array(tri_a).T
    C = np.mean(tri1,axis=0)
    X1 = translation_matrix(x=-C[0],y=-C[1],z=-C[2])
    R1 = rotation_matrix(degrees=40,x=0,y=1,z=0)
    X2 = translation_matrix(x=C[0],y=C[1],z=C[2])
    T1 = X2 @ R1 @ X1
    tri2 = T1 @ tri1
    tri3 = tri2.T
    tri_b = [pt[:3]/pt[-1] for pt in tri3]
    tri_b = list(map(lambda pt: list(map(float,list(pt))),
                     tri_b))
    return tri_b

def snapshot(tri,cam):
    tri_a = [pt+[1] for pt in tri] # 3D to 4D
    tri1 = np.array(tri_a).T
    tri2 = cam @ tri1 # 4D
    tri3  = tri2.T
    tri4 = [tri3[i]/tri3[i][-1] for i in range(len(tri3))]
    tri5 = list(map(lambda pt: list(map(float,list(pt[:2]))),tri4))
    return tri5

# tri = [...[x,y,z]...]
tri1 = [[-1,0,5],[1,0,5],[0,1,5],[3,4,5]]
print(f"tri1 = {tri1}")

f = 2 # focal length of camera
cx,cy = 2,3 # positioning of camera in 2D
t = [1,2,4] # center of camera
T1 = translation_matrix(-t[0],-t[1],-t[2])
degrees = 30
axis = 1,1,1
T2 = rotation_matrix(degrees,*axis)
s = [1,1,1] # zoom in / zoom out
T3 = scale_matrix(*s)
T4 = translation_matrix(*t)
T = T4 @ T3 @ T2 @ T1
cam1 = camera_matrix(f,cx,cy) @ T
f = 3 # focal length of camera
cx,cy = 4,1 # positioning of camera in 2D
tx,ty,tz = 5,8,1
t = [4,1,0] # center of camera
T1 = translation_matrix(-t[0],-t[1],-t[2])
degrees = 50
axis = 0,1,0
T2 = rotation_matrix(degrees,*axis)
s = [2,2,2] # zoom in / zoom out
T3 = scale_matrix(*s)
T4 = translation_matrix(*t)
T = T4 @ T3 @ T2 @ T1
cam2 = camera_matrix(f,cx,cy) @ T

pts1 = snapshot(tri1,cam1)
pts2 = snapshot(tri1,cam2)
print(f"pts1 = {pts1}")
print(f"pts2 = {pts2}")

##################################################
# [1] Microsoft Copilot, a large language model
# suggested findHomography and triangulatePoints but
# JGE needed to find out how to use these.
###################################################

def image_space_to_3D(cam1,pts1,cam2,pts2):
    P1 = np.array(pts1)
    P2 = np.array(pts2)
    H,status = cv2.findHomography(P1,P2,cv2.RANSAC)
    print(f"status = {status.flatten()}")
    P_4D = cv2.triangulatePoints(cam1,cam2,
                    P1.T, P2.T)
    P_3d = P_4D/P_4D[3]                               
    print(f"Homography Matrix: H = \n{H}")
    pts = []
    for i in range(P_3d.shape[0]):
        pt = P_3d[:,i]
        pt = pt.flatten()
        pt = pt[:3]/pt[3]
        pt = list(map(float,list(pt)))
        pts.append(pt)
        print(f"pt[{i}] = {pt}")
    return pts

pts = image_space_to_3D(cam1,pts1,cam2,pts2)


