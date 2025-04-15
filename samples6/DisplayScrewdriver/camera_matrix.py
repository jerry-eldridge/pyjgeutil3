import QuaternionGroup as HH

import scipy as sp
import numpy as np
import cv2
import graphics_cv as racg
from copy import deepcopy

from math import pi,cos,sin,acos,fmod

###############################################
# JGE:
def read_obj_to_points(fn):
    f = open(fn,'r')
    txt = f.read()
    f.close()
    lines = txt.split('\n')
    pts0 = []
    F = []
    def G(v):
        toks = v.split('/')
        if len(toks) > 1:
            return int(toks[0])-1
        else:
            return int(v)-1
    for line in lines:
        if len(line) == 0:
            continue
        else:
            if line[0:2] == 'v ':
                toks = line.split(' ')
                x,y,z = toks[1:]
                x,y,z = list(map(float,[x,y,z]))
                pt = [x,y,z]
                pts0.append(pt)
            elif line[0:3] == 'vn ':
                continue
            elif line[0:3] == 'vt ':
                continue
            elif line[0:2] == 'f ':
                continue
    for line in lines:
        if len(line) == 0:
            continue
        else:
            if line[0:2] == 'f ':
                toks = line.split(' ')
                try:
                    toks.remove('')
                except:
                    ii = 0
                f = toks[1:]
                f = list(map(G,f))
                F.append(f)
            elif line[0:3] == 'vn ':
                continue
            elif line[0:3] == 'vt ':
                continue
            elif line[0:2] == 'n ':
                continue
    return pts0,F

def distance(A,B):
    return float(np.linalg.norm(np.array(B)-np.array(A)))

def lerp(A,B,t):
    C = np.array(A)*(1-t) + np.array(B)*t
    C = list(map(float,list(C)))
    return C
#
###############################################

#####################################################
# [1] Microsoft Copilot, a large language model
# prompted with a query to find z-depth buffering.
#
def z_depth_buffering(pts_2d, z_depths, faces):
    visible_faces = []

    for face in faces:
        # Extract the z-depth values for the vertices
        # of the face
        face_z = [z_depths[idx] for idx in face]
        
        # Compute average z-depth for the face
        avg_z = np.mean(face_z)
        
        # Use a simple painter's algorithm
        # approach: frontmost faces first
        visible_faces.append((avg_z, face))
    
    # Sort faces by average z-depth (back to front)
    visible_faces.sort(key=lambda x: x[0], reverse=True)

    # Extract only the face indices, sorted
    return [face[1] for face in visible_faces]

# Copilot queried about creating a shading model
# like Phong or Gouraud shading

def compute_gouraud_shading(light_positions, \
    light_intensities, polygon_3d_points, \
    polygon_2d_points):
    # Convert 3D points to NumPy array for
    # vector calculations
    polygon_3d = np.array(polygon_3d_points, \
                dtype=np.float32)
    
    # Compute the normal vector of the polygon
    # (assuming planar polygon)
    v1 = polygon_3d[1] - polygon_3d[0]
    v2 = polygon_3d[2] - polygon_3d[0]
    normal = np.cross(v1, v2)
    normal = normal / np.linalg.norm(normal)
        # Normalize the normal vector
    
    # Compute shading for each vertex
    shading = np.zeros(len(polygon_3d))
    for light_position, light_intensity in \
        zip(light_positions, light_intensities):
        for i, point in enumerate(polygon_3d):
            # Vector from vertex to light source
            light_vector = np.array(light_position) - \
                           point
            light_vector = light_vector /\
                    (np.linalg.norm(light_vector)+1e-8)

            # Dot product for intensity calculation
            intensity = light_intensity * \
                    max(0, np.dot(normal, light_vector))
            shading[i] += intensity

    # Interpolate shading across 2D points
    # (Gouraud shading approximation)
    interpolated_shading = np.interp(
        range(len(polygon_2d_points)),
        range(len(polygon_3d_points)),
        shading
    )

    # Colorize polygon with interpolated shading
    colorized_polygon = [[int(s), int(s), int(s)] \
            for s in interpolated_shading]
    return colorized_polygon
#
#######################################################

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
def intrinsic_camera_matrix(alpha_x,alpha_y,skew,cx,cy):
    K = np.zeros((3,4),dtype="float")
    K[0,0] = alpha_x
    K[0,1] = skew
    K[0,2] = cx
    K[1,1] = alpha_y
    K[1,2] = cy
    K[2,2] = 1
    return K

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

def AimAxis(axis1,axis2):
    # Create V1 and V2 vectors of polygon1 normal and [0,0,1] z-axis
    V1 = axis1
    V2 = axis2 # z-axis
    V1 = np.array(V1)
    V2 = np.array(V2)
    # create a rotation axis to rotate V1 to V2
    # and compute angle in degrees of rotation, obtain quaternion for this
    axis = np.cross(V1,V2)
    angle = acos(np.inner(V1,V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))
    degrees = angle*180/pi
    q = HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    R = q.ToEuler()
    return R
#
############################################

##################################################
# [1] Microsoft Copilot, a large language model
# suggested findHomography and triangulatePoints but
# JGE needed to find out how to use these.
###################################################

def image_space_to_3D(cam1,pts1,cam2,pts2):
    P1 = np.array(pts1)
    P2 = np.array(pts2)
    H,status = cv2.findHomography(P1,P2,cv2.RANSAC)
    #print(f"status = {status.flatten()}")
    P_4D = cv2.triangulatePoints(cam1,cam2,
                    P1.T, P2.T)
    #print(f"P_4D = {P_4D}")
    P_3d = P_4D/P_4D[3]
    #print(f"P_3d = {P_3d}")
    #print(f"Homography Matrix: H = \n{H}")
    pts = []
    for i in range(P_3d.shape[1]):
        pt = P_3d[:,i]
        pt = pt.flatten()
        pt = pt[:3]
        pt = list(map(float,list(pt)))
        pts.append(pt)
        #print(f"pt[{i}] = {pt}")
    return pts,H
#
####################################################

################################################
# JGE:
f_v = lambda P,e: float(np.linalg.det(np.hstack(\
    (P[:,e[0]].reshape(3,1),P[:,e[1]]\
     .reshape(3,1),P[:,e[2]].reshape(3,1)))))
f_pt = lambda P: [f_v(P,[1,2,3]),-f_v(P,[0,2,3]),\
                f_v(P,[0,1,3]),-f_v(P,[0,1,2])]

def plot_graph(gr, cam, pts_3d, faces):
    faces2 = deepcopy(faces)
    pts_2d = cam.snapshot(pts_3d)
    O = cam.get_position()
    z_depths = [distance(O,pts_3d[i]) for i in \
            range(len(pts_3d))]
    faces3 = z_depth_buffering(pts_2d, z_depths, faces2)
    faces2 = deepcopy(faces3)
    light_positions = [[0,0,10],
                       [0,10,0],
                       [10,0,0]]
    light_intensities = [100.0,100.0,200.0] # W
    
    for i in range(len(faces2)):
        fi = faces2[i]
        ni = len(fi)
        pts_3d_fi = np.array(\
            [pts_3d[fi[i]] for i in range(ni)],
            dtype=np.float32)
        pts_2d_fi = np.array(\
            [pts_2d[fi[i]] for i in range(ni)],
            dtype=np.int32)
        shading = compute_gouraud_shading(\
            light_positions, \
            light_intensities, pts_3d_fi, \
            pts_2d_fi)
        color = np.mean([s for s in shading],axis=0)
        color = list(map(int,list(color)))
        racg.cv2.fillPoly(gr.canvas,[pts_2d_fi],color)
    return

def clamp(x,lo,hi):
    return max(lo,min(hi,x))

class Camera:
    def __init__(self, q,scale,alpha_x,alpha_y,skew,\
           cx,cy,Ct, mx, my):
        self._q = q
        self._scale = scale
        self._alpha_x = alpha_x
        self._alpha_y = alpha_y
        self._skew = skew
        self._cx = cx
        self._cy = cy
        self._position = Ct
        self._width = mx
        self._height = my
    def get_principal_point(self):
        return [self._cx, self._cy]
    def get_focal_lengths(self):
        _fx = self._alpha_x/self._width
        _fy = self._alpha_y/self._height
        return [_fx, _fy]
    def get_intrinsic(self):
        alpha_x = self.get_alpha_x()
        alpha_y = self.get_alpha_y()
        skew = self.get_skew()
        cx,cy = self.get_principal_point()
        self._K = intrinsic_camera_matrix(\
            alpha_x,alpha_y,skew,cx,cy)
        return self._K
    def get_rotation(self):
        return self._q.ToEuler()
    def get_scale(self):
        return self._scale
    def get_alpha_x(self):
        return self._alpha_x
    def get_alpha_y(self):
        return self._alpha_y
    def get_skew(self):
        return self._skew
    def get_position(self):
        return self._position
    def get_size(self):
        return [self._width, self._height]
    def set_principal_point(self, cx, cy):
##        print(f"Principal Point: (cx,cy)")
##        print(f"cx = {cx}")
##        print(f"cy = {cy}")
        self._cx, self._cy = [cx,cy]
        return
    def set_focal_lengths(self, fx, fy):
        self._alpha_x = fx * self._width
        self._alpha_y = fy * self._height
        return
    def set_rotation(self, R):
        self._q = HH.FromEuler(*R)
        Rmat = np.identity(4)
        Ra = self._q.rotation_matrix() # R * scale
        Rmat[:3,:3] = Ra[:3,:3]
##        print(f"Camera: quaternion q = {self._q}")
##        print(f"Camera: External Euler: \nr = {R}")
##        print(f"Camera: External Rotation "+\
##              f"Matrix: R = \n{Rmat}")
        return
    def set_scale(self, s):
##        print(f"Image: scale = {s}")
        self._scale = s
        return
    def set_alpha_x(self, alpha_x):
##        print(f"alpha_x = fx * mx = {alpha_x}")
        self._alpha_x = alpha_x
        return
    def set_alpha_y(self, alpha_y):
##        print(f"alpha_y = fy * my = {alpha_y}")
        self._alpha_y = alpha_y
        return
    def set_skew(self, skew):
##        print(f"Image: skew = {skew}")
        self._skew = skew
        return
    def set_position(self, T):
##        print(f"Camera Position:\nt = [tx,ty,tz] = {T}")
        self._position = T
        return 
    def set_size(self, width, height):
        self._width, self._height = width,height
        return
    def get_camera_matrix(self):
        K = self.get_intrinsic()
##        print("""K = self.get_intrinsic() = 
##[ mx*fx, skew, cx ],
##[    0, my*fy, cy ],
##[    0,     0,  1 ] =
##"""
##          f"\n{K}")
        
        tx,ty,tz = self.get_position()
        scale = self.get_scale()
        R = self.get_rotation()
        T = translation_matrix(tx,ty,tz)
##        print(f"""T = 
##[ 1, 0, 0, tx ],
##[ 0, 1, 0, ty ],
##[ 0, 0, 1, tz ],
##[ 0, 0, 0,  1 ] =
##{T}
##""")
        q = HH.FromEuler(*R)
        Rmat = q.rotation_matrix()
        Rmat4x4 = np.identity(4)
        Rmat4x4[:3,:3] = Rmat[:,:]
        P =  K @ (Rmat4x4 * scale) @ T
        return P
    def set_camera_matrix(self, P, width,height):
##        print(f"="*30)
##        print(f"Arbitrary 3 x 4 matrix to camera:")
##        print(f"P = \n{P}")

        # QR-decomposition, RQ-decomposition into
        # [1] https://en.wikipedia.org/wiki/Orthogonal_matrix
        # [2] https://en.wikipedia.org/wiki/QR_decomposition
        # (see relation to RQ decomposition)
        # K is upper triangular matrix 'R' and R is
        # orthogonal matrix 'Q'. The set of orthogonal
        # matrices 3 x 3 is called O(3) with the property
        # R is orthogonal if its transpose is equal to
        # its invers: np.allclose(R.T,np.linalg.inv(R)) is
        # True. A subgroup of O(3) is SO(3).
        # [3] https://en.wikipedia.org/wiki/Orthogonal_group
        # [4] https://en.wikipedia.org/wiki/3D_rotation_group
        # such that np.linalg.det(R) is 1.
        K,R = sp.linalg.rq(P[:,:3])
        epsilon = 1e-8
        scale1 = K[2,2]
        val = np.linalg.det(R)
        scale2 = val
        assert(abs(scale1) > epsilon)
        assert(abs(scale2) > epsilon)
        K = K/scale1
        R = R/scale2
        R4x4 = np.identity(4)
        R4x4[:3,:3] = R[:,:]
        scale = scale1 * scale2
        alpha_x = K[0,0]
        alpha_y = K[1,1]
        skew = K[0,1]
        cx = K[0,2]
        cy = K[1,2]
##        print(f"scale_x: alpha_x = {alpha_x}")
##        print(f"scale_y: alpha_y = {alpha_y}")
##        print(f"s = skew = {skew}")
##        print(f"cx = {cx}")
##        print(f"cy = {cy}")
        q = HH.Quaternion([0,0,0,0]\
                    ).set_rotation_matrix(R)
        r = q.ToEuler()
##        print(f"Camera: Intrinsic K = \n{K}")
        PP = np.array(f_pt(P))
        Ct = PP/PP[-1]
        Ct = Ct[:3].reshape(3,1)
##        print(f"scale = {scale}")
##        print(f"Camera Center: \n"+\
##              f"C~ = {Ct.flatten()}")
##        print(f"Camera: quaternion q = {q}")
##        print(f"Camera: External Euler: \nr = {r}")
##        print(f"Camera: External Rotation Matrix: R = \n{R}")
##        print("KRS:",K.shape,R.shape,scale)
        P2 = np.hstack((K@(R*scale),-K@(R*scale)@Ct))
##        print(f"P2 = [K@(R*scale)|-K@(R*scale)*C~] = \n{P2}")
##        print(f"="*30)


        self.set_principal_point(cx,cy)
        self.set_rotation(r)
        self.set_scale(scale)
        self.set_alpha_x(alpha_x)
        self.set_alpha_y(alpha_y)
        self.set_skew(skew)
        self.set_position(Ct)
        self.set_size(width,height)
##        print(f"P3 = {self.get_camera_matrix()}")
        return
    def snapshot(self, pts_3d):
        cam = self.get_camera_matrix()
        image_2d = snapshot(pts_3d,cam)
        return image_2d
    def aim(self, y_axis, pt_aim):
        O = np.array(self.get_position())
        A = np.array(pt_aim)
        C = list(map(float,list(A-O)))
        R = AimAxis(y_axis, C)
        self.set_rotation(R)
        return R
    def snapshot_of_pts(self, pts_3d, F, color):
        gr = racg.Graphics(w=self._width,
                           h=self._height)
        gr.Clear()
        plot_graph(gr,self, pts_3d, F)
        image = gr.canvas.copy()
        return image


