from copy import deepcopy
import itertools
import numpy as np
from math import sin,cos,pi,exp, acos


################################################################
# [1] Jerry G Eldridge (JGE), from graph.py code
#

# Center of 3D points
def Center(pts,flag2d = False):
    PTS = [np.array(pt) for pt in pts]
    X = [pt[0] for pt in PTS]
    Y = [pt[1] for pt in PTS]
    if flag2d:
        C = [np.mean(X),np.mean(Y)]
    else:
        Z = [pt[2] for pt in PTS]
        C = [np.mean(X),np.mean(Y),np.mean(Z)]
    return C

def PathEdges(path):
    path0 = deepcopy(path)
    L = []
    i = 0
    for i in range(len(path)-1):
        e = [path0[i],path0[i+1]]
        L.append(e)
    return L

def GraphUnionPseudo(G1,G2):
    G = {}
    G['V'] = list(zip(G1['V'],[0]*len(G1['V'])))+\
             list(zip(G2['V'],[1]*len(G2['V'])))
    G['E'] = [[(e[0],0),(e[1],0)] for e in G1['E']]+\
             [[(e[0],1),(e[1],1)] for e in G2['E']]
    return G

def PseudoToGraph(G):
    V = list(range(len(G['V'])))
    d = {}
    i = 0
    for i in V:
        v = G['V'][i]
        d[v] = i
    E = []
    for e in G['E']:
        u,v = e
        f = [d[u],d[v]]
        E.append(f)
    G2 = {}
    G2['V'] = V
    G2['E'] = E
    return G2

def GraphUnion(G1,G2):
    H = GraphUnionPseudo(G1,G2)
    G = PseudoToGraph(H)
    return G

def Cn(N=3):
##    """
##    https://en.wikipedia.org/wiki/Cycle_graph
##    """
    if N < 3:
        print("Error: Cycle must have at least 3 vertices")
        return {}
    doc = {"V":list(range(N)),"E":PathEdges(list(range(N)))+[[N-1,0]]}
    return doc

def Pn(N):
##    """
##    https://en.wikipedia.org/wiki/Path_graph
##    """
    doc = {}
    doc["V"] = list(range(N))
    doc["E"] = PathEdges(list(range(N)))
    return doc

def RemoveLoops(G):
    F = []
    for e in G['E']:
        u,v = e
        if not (u == v):
            F.append(e)
    G2 = {}
    G2['V'] = deepcopy(G['V'])
    G2['E'] = F
    return G2

def QuotientGraph0(G, R):
    S = []
    for L in R:
        for x in L:
            S.append(x)

    I = list(set(G['V']) - set(S))
    for x in I:
        R.append([x])
    V = range(len(R))
    E = []
    for e in G['E']:
        u,v = e
        for i in range(len(R)):
            if u in R[i]:
                break
        for j in range(len(R)):
            if v in R[j]:
                break
        f = [i,j]
        if f not in E:
            E.append(f)
    G2 = {}
    G2['V'] = V
    G2['E'] = E
    return G2

def QuotientGraph(G, R):
    G2 = MakeUndirected(G)
    G3 = QuotientGraph0(G2,R)
    G4 = RemoveLoops(G3)
    return G4

def GraphProduct(doc1,doc2):
##    """
##    [Bondy,Murty] Graph Theory with Applications,
##    North-Holland, 1976
##
##    The product of simple graphs G and H is the simple
##    graph G x H with vertex set V(G) x V(H) ('x' cartesian
##    product) in which (u,v) is adjacent to (u',v') if and only
##    if u = u' and [v,v'] in E(H), or v = v' and [u,u']
##    in E(G).
##
##    A simple graph is a graph with no loops [u,u] or
##    two parallel edges [u,v] and [u,v] both in E.
##    """
    Obj = []
    for el in itertools.product(doc1["V"],doc2["V"]):
        Obj.append(el)
    V = list(range(len(Obj)))
    def LookupObj(Obj,v):
        i = 0
        for obj in Obj:
            if v == obj:
                return i
            i += 1
        return -1
    E = []
    for i in V:
        u,v = Obj[i]
        for j in V:
            up,vp = Obj[j]
            if (u == up and ([v,vp]in doc2["E"])) or \
               (v == vp and ([u,up] in doc1["E"])):
                E.append([i,j])
    doc = {}
    doc["V"] = V
    doc["E"] = E
    doc["object"]=Obj
    return doc

def ExtrudeGraph(doc):
##    """
##    Extrude Graph by Multiplying a single edge with the
##    doc: doc2 = edge x doc, with doc2["object"] and vertices
##    ordered so that (0,doc) and (1,doc) are copies of doc
##    and corresponding vertices are edges from (0,doc) and (1,doc).
##    """
    doc1 = {"V":list(range(2)),\
            "E":PathEdges(list(range(2)))}
    doc2 = GraphProduct(doc1,doc)
    return doc2
#
#######################################################################################

#######################################################################################
# Jerry G Eldridge, from QuaternionGroup.py
#

import numpy as np
from math import sqrt,pi,cos,sin,acos,asin,tan,atan

from copy import deepcopy

# multipy two square n x n matrices A and B together
def MatMul(A,B):
    return np.einsum('ij,jk->ik',A,B)

# https://en.wikipedia.org/wiki/Quaternion#Matrix_representations
class Quaternion:
    # use S to mean self instance of Quaternion class.
    def __init__(S,L):
        assert(len(L)==4)
        S.L = deepcopy(L)
        S.I = np.identity(4)
        # note that i**2 = j**2 = k**2 = -I
        # and other quaternion group algebra rules hold
        S.i = np.array([
            [0,-1,0,0],
            [1,0,0,0],
            [0,0,0,-1],
            [0,0,1,0]])
        S.j = np.array([
            [0,0,-1,0],
            [0,0,0,1],
            [1,0,0,0],
            [0,-1,0,0]])
        S.k = np.array([
            [0,0,0,-1],
            [0,0,-1,0],
            [0,1,0,0],
            [1,0,0,0]])
        S.A = L[0]*S.I + L[1]*S.i + L[2]*S.j + L[3]*S.k
        S.q = np.array(L)
        return
    # S + q
    def __add__(S,q):
        A = S.A + q.A
        q2 = Quaternion([A[0,0],A[1,0],A[2,0],A[3,0]])
        return q2
    # -S where S is quaternion
    def __neg__(S):
        A = -S.A
        q2 = Quaternion([A[0,0],A[1,0],A[2,0],A[3,0]])
        return q2
    # S - q
    def __sub__(S,q):
        q2 = S + (-q)
        return q2
    # turn quarternions into vector space using real scalars
    def right_smul(S,x):
        A = x*S.A
        q2 = Quaternion([A[0,0],A[1,0],A[2,0],A[3,0]])
        return q2
    # multiply quaternions S*q
    def __mul__(S,q):
        if type(q) == type(Quaternion([1,0,0,0])): # quaternion
            A = MatMul(S.A,q.A)
            q2 = Quaternion([A[0,0],A[1,0],A[2,0],A[3,0]])
            return q2
        if type(q) in [type(3.1),type(3)]: # real number
            x = q
            return S.right_smul(x)
    def __pow__(S,n):
        q = Quaternion([1,0,0,0]) # one
        for i in range(1,n):
            q = q*S
        return q
    # string representation of quaternion
    def __str__(S):
        s = '[%.4f,%.4f,%.4f,%.4f]' % tuple(S.q)
        return s
    def __repr__(S):
        return str(S)
    # conjugate of a quaternion
    def conjugate(S):
        q2 = Quaternion([S.q[0],-S.q[1],-S.q[2],-S.q[3]])
        return q2
    def inv(S):
        epsilon = 1e-8
        assert(abs(S)**2 > epsilon)
        qi = S.conjugate()*(1.0/abs(S)**2)
        return qi
    # norm of the quaternion field
    def __abs__(S):
        q = S*S.conjugate()
        return sqrt(q.q[0])
    # create a versor or unit quaternion
    def normalize(S):
        x = 1.0/abs(S)
        q = S*x
        return q
    # S[n] for quaternion S
    def __getitem__(S,n):
        return S.q[n]
    # S[b] = c for quaternion S
    def __setitem__(S,b,c):
        S.q[b] = c 
        q2 = Quaternion([S.q[0],S.q[1],S.q[2],S.q[3]])
        return q2
    def rotation_matrix(S):
#        """
#        Euler-Rodrigues parameters S.q computing
#        3D rotation matrix R = S.rotation_matrix()
#        for quaternion S.
#        """
        q2 = S.normalize()
        a,b,c,d = list(q2.q)
        R = np.array([
            [a**2+b**2-c**2-d**2,2*(b*c-a*d),2*(b*d+a*c)],
            [2*(b*c+a*d),a**2-b**2+c**2-d**2,2*(c*d-a*b)],
            [2*(b*d-a*c),2*(c*d+a*b),a**2-b**2-c**2+d**2]])
        return R
    #https://en.wikipedia.org/wiki/Axis%E2%80%93angle_representation
    def set_rotation_matrix(S,R):
        theta = acos((np.trace(R)-1)/2.0)
        omega = np.array([
            R[2,1]-R[1,2],
            R[0,2]-R[2,0],
            R[1,0]-R[0,1]])/(2*sin(theta))
        alpha = theta
        beta = omega
        # https://en.wikipedia.org/wiki/Direction_cosine
        a,b,c = beta/np.linalg.norm(beta)
        q = Quaternion([
             cos(alpha/2.0),
             sin(alpha/2.0)*a,
             sin(alpha/2.0)*b,
             sin(alpha/2.0)*c])
        S = q
        return q
    # https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    def ToEuler(self):
        import math
        w,x,y,z = self.L
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        X = math.degrees(math.atan2(t0, t1))

        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        Y = math.degrees(math.asin(t2))

        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        Z = math.degrees(math.atan2(t3, t4))
        return X,Y,Z

def slerp(q1,q2,t):
#    """
#    q = slerp(q1,q2,t) - spherical lerp two quaternions
#    q1 and q2 blending them for t in interval [0,1].
#    q1 = slerp(q1,q2,0) and q2 = slerp(q1,q2,1)
#    creating a path from q1 to q2 parametrized by t.
#    Thus q.rotation_matrix() is a path from the
#    rotation of q1 to rotation of q2.
#    """
    # use right scalar multiplication
    q = q1*(1-t)+q2*t
    return q

# https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
def rotation_quaternion(degrees,x,y,z):
#    """
#    q = rotation_quaternion(degrees,x,y,z) returns
#    a quaternion representing a rotation matrix
#    of a 3D rotation about axis (x,y,z) by degrees
#    angle.
#    """
    alpha = degrees*pi/180.0
    beta = np.array([x,y,z])
    # https://en.wikipedia.org/wiki/Direction_cosine
    A0 = np.linalg.norm(beta)
    epsilon = 1e-8
    if A0 > epsilon:
        beta = beta/A0
    q = Quaternion([
         cos(alpha/2.0),
         sin(alpha/2.0)*beta[0],
         sin(alpha/2.0)*beta[1],
         sin(alpha/2.0)*beta[2]])
    return q

def FromEuler(X,Y,Z):
    roll,pitch,yaw = X,Y,Z
    RQ = rotation_quaternion
    q = RQ(yaw,0,0,1)*RQ(pitch,0,1,0)*RQ(roll,1,0,0)
    return q

# https://en.wikipedia.org/wiki/Aircraft_principal_axes
# X is pitch axis (right of aircraft)
# Y is yaw axis (down from aircraft)
# Z is roll axis (front of aircraft)
def RollYawPitch(L):
    roll,yaw,pitch = L
    X,Y,Z = roll,pitch,yaw
    q2 = FromEuler(X,Y,Z)
    return q2

Q = Quaternion
# you can right scalar multiply by reals these basis quaternions
e = Q([1,0,0,0])
i = Q([0,1,0,0])
j = Q([0,0,1,0])
k = Q([0,0,0,1])
# q = e*3 + i*4 + j*3.1 + k*5 is Q([3,4,3.1,5])

#
######################################################################################

########################################################################################
# Jerry G Eldridge, from extrusion.py 

def FacePts(G,i):
     f = G['F'][i]
     pts = [G['pts'][v] for v in f]
     return pts
 
def FaceNormalABC(A,B,C):
     A = np.array(A)
     B = np.array(B)
     C = np.array(C)
     N = np.cross(A-B,C-B)
     aa = np.linalg.norm(N)
     epsilon = 1e-8
     if aa > epsilon:
          N = N/aa
     try:
          N = list(map(float,list(N)))
     except:
          N = [0,0,1]
     return N
 
def FaceNormal(G,i):
     pts = FacePts(G,i)
     A,B,C = pts[:3]
     N = FaceNormalABC(A,B,C)
     return N

def ext_ExtrudeGraph(doc,k):
#     """
#     Extrude Graph by Multiplying a single edge with the
#     doc: doc2 = edge x doc, with doc2["object"] and vertices
#     ordered so that (0,doc) and (1,doc) are copies of doc
#     and corresponding vertices are edges from (0,doc) and (1,doc).
#     """
     doc1 = {"V":list(range(k)),"E":PathEdges(list(range(k)))}
     doc2 = GraphProduct(doc1,doc)
     return doc2

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
    q = rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    return q

#
########################################################################################

#########################################################################################
# Jerry G Eldridge, from vectors.py
def rotation_matrix(degrees,x,y,z):
#    """
#    4x4 rotation matrix for axis [x,y,z] rotated by angle, degrees
#    called R, then an extended coordinate X = [x0,x1,x2,1] is
#    XP = R*X and rotated point is [XP[0],XP[1],XP[2]].
#    """
    v = np.array([[x,y,z]]).T
    u = v/norm(v)
    S = np.array([
        [0,-u[2,0],u[1,0]],
        [u[2,0],0,-u[0,0]],
        [-u[1,0],u[0,0],0]])
    I = np.array([
        [1,0,0],
        [0,1,0],
        [0,0,1]])
    uu = u.dot(u.T)
    M = uu+cos(degrees*pi/180)*(I-uu)+sin(degrees*pi/180)*S
    R = np.zeros((4,4),dtype="float32")
    R[:3,:3]=M
    R[3,3] = 1
    return R
def translation_matrix(x,y,z):
#    """
#    4x4 translation matrix that maps a point pt from
#    pt[0] += x
#    pt[1] += y
#    pt[2] += z
#    pt[3] = pt[3] # w = 1
#    """
    T = np.eye(4,4,dtype="float32")
    T[0,3] = x
    T[1,3] = y
    T[2,3] = z
    T[3,3] = 1
    return T
def frustrum_matrix(left,right,bottom,top,near,far):
#    """
#    4x4 frustrum matrix that maps a point pt
#    to perspective transform from 3D to 2D
#    x = x/z
#    y = y/z
#    z = 1
#    w = 1
#    though uses a frustrum square (left,top) to (right,bottom)
#    of depth far to near.
#    
#    T = eye(4,4,dtype="float32")
#    rl = (right-left)*1.0
#    tb = (top-bottom)*1.0
#    fn = (far-near)*1.0
#    T[0,0] = 2*near/rl
#    T[0,2] = (right+left)/rl
#    T[1,1] = 2*near/tb
#    T[1,2] = (top+bottom)/tb
#    T[2,2] = -(far+near)/fn
#    T[2,3] = -2*far*near/fn
#    T[3,2] = -1
#    T[3,3] = 0
#    """
    T = np.eye(4,4,dtype="float32")
    rl = (right-left)*1.0
    tb = (top-bottom)*1.0
    fn = (far-near)*1.0
    T[0,0] = 2*near/rl
    T[0,2] = (right+left)/rl
    T[1,1] = 2*near/tb
    T[1,2] = (top+bottom)/tb
    T[2,2] = -(far+near)/fn
    T[2,3] = -2*far*near/fn
    T[3,2] = -1
    T[3,3] = 0
    return T
def scale_matrix(sx,sy,sz):
#    """
#    4x4 scale matrix that scales a point pt
#    x = sx*x
#    y = sy*y
#    z = sz*z
#    w = 1
#    """
    T = np.eye(4,4,dtype="float32")
    T[0,0] = sx
    T[1,1] = sy
    T[2,2] = sz
    T[3,3] = 1
    return T
#
#######################################################################################

#######################################################################################
# Jerry G Eldridge, from affine.py
# rotate points shape with quaternion q

def Transform3(shape, T):
    shape = np.array(shape,dtype=np.float64)
    shape = np.hstack([shape,np.ones((len(shape),1))])
    shape = (T @ shape.T).T
    for i in range(len(shape)):
        shape[i,:] = shape[i,:]/shape[i,3]
    shape = shape[:,0:3]
    shape = list(map(lambda pt: list(map(float,pt)),
                     shape))
    return shape

# transform points with 4x4 transformation matrix T
def Transform(shape,T):
    return Transform3(shape,T)

# convert quaternion to 4x4 rotation matrix
def q2R(q):
    q = Quaternion(q)
    R3 = q.rotation_matrix()
    R = np.identity(4)
    R[:3,:3] = R3
    return R

# round-off numbers in list of points shape
def Round(shape):
    shape = [[int(round(x)) for x in pt] for pt in shape]
    return shape

def Rotate(shape,q,align=True):
    R = q2R(q.q)
    SHAPE = Transform(shape,R)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE

# Translate points shape by [tx,ty,tz]
def Translate(shape,tx,ty,tz,align=True):
    T = translation_matrix(tx, ty, tz)
    SHAPE = Transform(shape,T)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE

# Scale points shape by [sx,sy,sz]
def Scale(shape,sx,sy,sz,align=True):
    T = scale_matrix(sx, sy, sz)
    SHAPE = Transform(shape,T)
    if align:
        SHAPE = Round(SHAPE)
    return SHAPE
#
#######################################################################################

########################################################################################
# Jerry G Eldridge, from alg_topo.py code
#
def AT_Cylinder(path, cross_sections,
        bcap=True,ecap=True,closed=False):
    m = len(cross_sections[0])
    G = Cn(m)
    G['pts'] = deepcopy(cross_sections[0])
    m = len(G['V'])
    n = len(path)
    k = n
    assert(n>=3)
    H = ext_ExtrudeGraph(G,k)
    pts = []
    F = []
    N = []
    G0 = deepcopy(G)
    G0['F'] = [G['V'][:3]]
    N0 = FaceNormal(G0,0)
    nn = n-1
    if closed:
         nn = n

    # create shape along axis with given
    # cross sections, cross_sections[i]
    for i in range(n-1):
        A = np.array(path[i])
        B = np.array(path[(i+1)%n])
        vB = B - A
        axis1 = N0
        axis2 = list(vB)
        q_k = AimAxis(axis1,axis2)
        s_k = [1,1,1]
        t_k = list(A)
        pts_k = deepcopy(cross_sections[i])
        C_k = Center(pts_k)
        pts_k = Translate(pts_k,-C_k[0],-C_k[1],-C_k[2],align=False)
        pts_k = Rotate(pts_k,q_k,align=False)
        pts_k = Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
        pts_k = Translate(pts_k,t_k[0],t_k[1],t_k[2],align=False)        
        pts = pts + pts_k
    pts_k = deepcopy(cross_sections[-1])
    C_k = Center(pts_k)
    pts_k = Translate(pts_k,-C_k[0],-C_k[1],-C_k[2],align=False)
    pts_k = Rotate(pts_k,q_k,align=False)
    pts_k = Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
    pts_k = Translate(pts_k,t_k[0],t_k[1],t_k[2],align=False)        
    pts = pts + pts_k
    for i in range(n-1):
         for e in G['E']:
              u1,v1 = [u + m*i for u in e]
              u2,v2 = [u + m*(i+1) for u in e]
              f = [u1,u2,v2,v1]
              f1 = [u1,u2,v1]
              f2 = [v1,u2,v2]
              for fi in [f1,f2]:
                   G_f = {}
                   G_f = ext_ExtrudeGraph(G,2)
                   G_f['pts'] = deepcopy(pts[i*m:(i+2)*m])
                   f2i = [u - m*i for u in fi]
                   G_f['F'] = [deepcopy(f2i)]
                   F.append(fi)
                   N_fi = FaceNormal(G_f,0)
                   N.append(N_fi)

    # create begin cap
    if bcap:
        i = 0
        pts0 = deepcopy(pts[i*m:(i+1)*m])
        C0 = Center(pts0)
        w = len(H['V'])
        H['V'].append(w)
        pts.append(C0)
        for j in range(m):
            u1,v1 = [u + m*i for u in [j,(j+1)%m]]
            fj = [u1,v1,w]#[u1,w,v1]
            for k in range(len(fj)):
                e = [fj[k],fj[(k+1)%2]]
                H['E'].append(e)
            F.append(fj)
            G_f = {}
            G_f['V'] = [0,1,2]
            G_f['E'] = [[ii,(ii+1)%3] for ii in range(3)]
            f2j = [0,1,2]
            G_f['pts'] = [pts[v] for v in fj]
            G_f['F'] = [deepcopy(f2j)]
            N_fi = FaceNormal(G_f,0)
            N.append(N_fi)
    if ecap:
        i = n-1
        pts0 = deepcopy(pts[i*m:(i+1)*m])
        C0 = Center(pts0)
        w = len(H['V'])
        H['V'].append(w)
        pts.append(C0)
        for j in range(m):
            u1,v1 = [u + m*i for u in [j,(j+1)%m]]
            fj = [u1,w,v1]
            for k in range(len(fj)):
                e = [fj[k],fj[(k+1)%2]]
                H['E'].append(e)
            F.append(fj)
            G_f = {}
            G_f['V'] = [0,1,2]
            G_f['E'] = [[ii,(ii+1)%3] for ii in range(3)]
            f2j = [0,1,2]
            G_f['pts'] = [pts[v] for v in fj]
            G_f['F'] = [deepcopy(f2j)]
            N_fi = FaceNormal(G_f,0)
            N.append(N_fi)        
        
    H['pts'] = pts
    H['F'] = F
    H['N'] = N
    return H

def AT_Graph_Cylinder(path, G, cross_sections,
        bcap=True,ecap=True,closed=False):
    G['pts'] = deepcopy(cross_sections[0])
    m = len(G['V'])
    n = len(path)
    k = n
    assert(n>=3)
    H = ext_ExtrudeGraph(G,k)
    pts = []
    F = []
    N = []
    G0 = deepcopy(G)
    G0['F'] = [G['V'][:3]]
    N0 = FaceNormal(G0,0)
    nn = n-1
    if closed:
         nn = n

    # create shape along axis with given
    # cross sections, cross_sections[i]
    for i in range(n-1):
        A = np.array(path[i])
        B = np.array(path[(i+1)%n])
        vB = B - A
        axis1 = N0
        axis2 = list(vB)
        q_k = AimAxis(axis1,axis2)
        s_k = [1,1,1]
        t_k = list(A)
        pts_k = deepcopy(cross_sections[i])
        C_k = Center(pts_k)
        pts_k = Translate(pts_k,-C_k[0],-C_k[1],-C_k[2],align=False)
        pts_k = Rotate(pts_k,q_k,align=False)
        pts_k = Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
        pts_k = Translate(pts_k,t_k[0],t_k[1],t_k[2],align=False)        
        pts = pts + pts_k
    pts_k = deepcopy(cross_sections[-1])
    C_k = Center(pts_k)
    pts_k = Translate(pts_k,-C_k[0],-C_k[1],-C_k[2],align=False)
    pts_k = Rotate(pts_k,q_k,align=False)
    pts_k = Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
    pts_k = Translate(pts_k,t_k[0],t_k[1],t_k[2],align=False)        
    pts = pts + pts_k
    for i in range(n-1):
         for j in range(len(G['E'])):
              e = G['E'][j]
              sgn = G['OR'][j]
              u1,v1 = [u + m*i for u in e]
              u2,v2 = [u + m*(i+1) for u in e]
              f = [u1,u2,v2,v1]
              if sgn == 1:
                  f1 = [u1,u2,v1]
                  f2 = [v1,u2,v2]
              else:
                  f1 = [u1,v1,u2]
                  f2 = [v1,v2,u2]
              for fi in [f1,f2]:
                   G_f = {}
                   G_f = ext_ExtrudeGraph(G,2)
                   G_f['pts'] = deepcopy(pts[i*m:(i+2)*m])
                   f2i = [u - m*i for u in fi]
                   G_f['F'] = [deepcopy(f2i)]
                   F.append(fi)
                   N_fi = ext.FaceNormal(G_f,0)
                   N.append(N_fi)

    # create begin cap
    if bcap:
        i = 0
        pts0 = deepcopy(pts[i*m:(i+1)*m])
        for f in G['F']:
            u,v,w = f
            u1 = u + m*i
            v1 = v + m*i
            w1 = w + m*i
            fj = [u1,v1,w1]
            for k in range(len(fj)):
                e = [fj[k],fj[(k+1)%2]]
                H['E'].append(e)
            F.append(fj)
            G_f = {}
            G_f['V'] = [0,1,2]
            G_f['E'] = [[ii,(ii+1)%3] for ii in range(3)]
            f2j = [0,1,2]
            G_f['pts'] = [pts[v] for v in fj]
            G_f['F'] = [deepcopy(f2j)]
            N_fi = FaceNormal(G_f,0)
            N.append(N_fi)
    if ecap:
        i = n-1
        pts0 = deepcopy(pts[i*m:(i+1)*m])
        for f in G['F']:
            u,v,w = f
            u1 = u + m*i
            v1 = v + m*i
            w1 = w + m*i
            fj = [u1,w1,v1]
            for k in range(len(fj)):
                e = [fj[k],fj[(k+1)%2]]
                H['E'].append(e)
            F.append(fj)
            G_f = {}
            G_f['V'] = [0,1,2]
            G_f['E'] = [[ii,(ii+1)%3] for ii in range(3)]
            f2j = [0,1,2]
            G_f['pts'] = [pts[v] for v in fj]
            G_f['F'] = [deepcopy(f2j)]
            N_fi = FaceNormal(G_f,0)
            N.append(N_fi)        
  
    H['pts'] = pts
    H['F'] = F
    H['N'] = N
    return H

class String_Particle:
    def __init__(self,G, x_func, section_func, ds):
        self.s = 0
        self.ds = ds
        self.xf = x_func
        self.G = copy_graph(G)
        self.sectionf = section_func
    def get_world_sheet(self,bcap=True,ecap=True):
        path = []
        cross_sections = []
        smin = 0
        smax = self.s + 2*self.ds
        s = smin
        while s < smax + self.ds:
            x = self.xf(s)
            section = self.sectionf(s)
            path.append(x)
            cross_sections.append(section)
            s = s + self.ds
        G2 = AT_Graph_Cylinder(path, self.G,
                    cross_sections,
                    bcap=bcap,ecap=ecap,
                    closed=False)
        return G2
    def propagate(self):
        self.s = min(1,self.s + self.ds)
    def reset(self):
        self.s = 0
#
########################################################################################

