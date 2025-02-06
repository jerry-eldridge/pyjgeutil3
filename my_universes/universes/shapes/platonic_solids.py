from . import extrusion as ext
from .common import graph as gra
from .common import affine as aff

import numpy as np
import scipy.spatial as ss

from copy import deepcopy
from math import sqrt

# tetrahedron
def create_tetrahedron0(pts):
    assert(len(pts) == 4)
    V = list(range(4))
    E = [[0,1],[1,2],[2,0],[3,1],[3,2],[3,0]]
    F = [[0,1,3], [1,2,3], [0,3,2], [0,2,1]]
    G = {}
    G['V'] = V
    G['E'] = E
    G['F'] = F
    G['pts'] = pts
    N = []
    for i in range(len(G['F'])):
        N_i = ext.FaceNormal(G,i)
        N.append(N_i)
    G['N'] = N    
    return G

def create_tetrahedron():
    a = 1
    b = sqrt(3)/2*a
    c = sqrt(a**2-b**2/4)
    mid = np.mean([[0,0,0],[a,0,0],[a/2,b,0]],axis=0)
    mid = list(map(float,list(mid)))
    pts = [[0,0,0],[a,0,0],[a/2,b,0],[mid[0],mid[1],b]]
    G = create_tetrahedron0(pts)
    return G

# cube
def create_cube0(pts):
    assert(len(pts) == 8)
    V = list(range(8))
    E = [[0,1],[5,1],[5,4],[4,0],[2,6],[6,7],
         [7,3],[3,2],[1,2],[5,6],[4,7],[0,3]]
    F = [[0, 1, 5], [0, 5, 4], [1, 2, 6], [1, 6, 5],
         [7, 6, 2], [7, 2, 3], [4, 7, 3], [4, 3, 0],
         [7, 4, 5], [7, 5, 6], [0, 3, 2], [0, 2, 1]]
    G = {}
    G['V'] = V
    G['E'] = E
    G['F'] = F
    G['pts'] = pts
    N = []
    for i in range(len(G['F'])):
        N_i = ext.FaceNormal(G,i)
        N.append(N_i)
    G['N'] = N    
    return G

def create_cube():
    w = 1
    h = 1
    d = 1
    pts = [[-w/2,-h/2,-d/2],[w/2,-h/2,-d/2],
           [w/2,h/2,-d/2],[-w/2,h/2,-d/2],
           [-w/2,-h/2,d/2],[w/2,-h/2,d/2],
           [w/2,h/2,d/2],[-w/2,h/2,d/2]]
    G = create_cube0(pts)
    return G

# octahedron
def create_octahedron():
    # create top
    a = 1
    b = sqrt(3)/2*a
    c = sqrt(a**2-b**2/4)
    mid = np.mean([[0,0,0],[a,0,0],[a/2,b,0]],axis=0)
    mid = list(map(float,list(mid)))
    F = [[0,1,3], [1,2,3], [0,3,2], [0,2,1]]
    pts1 = [[0,0,0],[a,0,0],[a/2,b,0],[mid[0],mid[1],b]]
    V = list(range(4))
    E = [[0,1],[1,2],[2,0],[3,1],[3,2],[3,0]]
    F = [[0,1,3], [1,2,3], [0,3,2]]
    G1 = {}
    G1['V'] = V
    G1['E'] = E
    G1['F'] = F
    G1['pts'] = pts1
    N = []
    for i in range(len(G1['F'])):
        N_i = ext.FaceNormal(G1,i)
        N.append(N_i)
    G1['N'] = N
    

    # create bottom
    a = 1
    b = sqrt(3)/2*a
    c = sqrt(a**2-b**2/4)
    mid = np.mean([[0,0,0],[a,0,0],[a/2,b,0]],axis=0)
    mid = list(map(float,list(mid)))
    #F = [[0,1,3], [1,2,3], [0,3,2], [0,2,1]]
    pts2 = [[0,0,0],[a,0,0],[a/2,b,0],[mid[0],mid[1],-b]]
    V = list(range(4))
    E = [[0,1],[1,2],[2,0],[3,1],[3,2],[3,0]]
    F = [[0,1,3], [1,2,3], [0,3,2]]
    F = list(map(lambda f: list(reversed(f)),F))
    G2 = {}
    G2['V'] = V
    G2['E'] = E
    G2['F'] = F
    G2['pts'] = pts2
    N = []
    for i in range(len(G2['F'])):
        N_i = ext.FaceNormal(G2,i)
        N.append(N_i)
    G2['N'] = N
    
    G = ext.GraphUnionS(G1,G2)
    return G

##############################################
# copilot:

# this code function "_calculate_sign" provided
# by Microsoft's copilot
def _calculate_sign(A, B, C, center):
    # Convert points to numpy arrays if they are
    # not already
    A, B, C, center = list(map(np.array,
                               [A, B, C, center]))
    
    # Compute the normal vector using cross product
    AB = B - A
    AC = C - A
    normal = np.cross(AB, AC)
    
    # Compute the vector from center to A
    CA = A - center
    
    # Calculate the dot product
    dot_product = np.dot(normal, CA)
    
    # Determine the sign based on the dot product
    sgn = np.sign(dot_product)
    
    return sgn

# :copilot
################################################


def create_icosahedron():
    ##################################
    # JGE:
    
    # JGE created graph but had no points to it
##    G = {'V': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
##         'E': [[0, 1], [1,0], [0, 2], [2, 0], [0, 3],
##               [3, 0], [0, 7], [7, 0], [0, 8], [8,0],
##               [1, 2], [2, 1], [1, 3], [3, 1], [1, 4],
##               [4, 1], [1, 5], [5,1], [2, 5], [5, 2],
##               [2, 6], [6, 2], [2, 7], [7, 2], [3, 4],
##               [4,3], [3, 8], [8, 3], [3, 9], [9, 3],
##               [4, 5], [5, 4], [4, 9], [9,4], [4, 10],
##               [10, 4], [5, 6], [6, 5], [5, 10],
##               [10, 5], [6, 7],[7, 6], [6, 10],
##               [10, 6], [6, 11], [11, 6], [7, 8],
##               [8, 7], [7,11], [11, 7], [8, 9], [9, 8],
##               [8, 11], [11, 8], [9, 10], [10, 9],
##               [9, 11], [11, 9], [10, 11], [11, 10]], 
##        'F': [[0, 2, 1], [0, 1, 3], [1, 2, 5],
##              [0, 7, 2], [0, 8, 7], [0, 3, 8],
##              [1, 4, 3], [1,5, 4], [2, 7, 6],
##              [2, 6, 5], [7, 8, 11], [8, 9, 11],
##              [8, 3, 9],[3, 4, 9], [4, 10, 9],
##              [10, 11, 9], [4, 5, 10], [6, 10, 5],
##              [6,11, 10], [6, 7, 11]]}

    # :JGE
    ##############################################

    ##############################################
    # Copilot begin.
    
    # [1] Microsoft Copilot, a large language model

    phi = (1 + sqrt(5)) / 2
    pts0 = [
    (0, 1, phi), (0, -1, phi), (0, 1, -phi),
    (0, -1, -phi), (1, phi, 0), (1, -phi, 0),
    (-1, phi, 0), (-1, -phi, 0), (phi, 0, 1),
    (-phi, 0, 1), (phi, 0, -1), (-phi, 0, -1)]
    pts0 = list(map(list, pts0))

    O = aff.Center(pts0)
    O = list(map(float, O))
    
    pts = np.array(pts0)
    hull = ss.ConvexHull(pts)
    hull_F = hull.simplices

    # Copilot end.
    #################################
    
    ########################################
    # JGE:
    E = []
    F = []
    N = []
    for f in hull_F:
        u,v,w = list(map(int,list(f)))
        A = pts[u]
        B = pts[v]
        C = pts[w]
        N_f = ext.FaceNormalABC(A,B,C)

        # ss.ConvexHull does not orient surface's
        # simplices as desired so reverse listing
        # of f = [u,v,w] to f = [u,w,v] when this
        # occurs
        sgn = _calculate_sign(A, B, C, O)
        if sgn < 0:
            # swap counter-clockwise and clockwise
            u,v,w = u,w,v
            
        e1 = [u,v]
        e2 = [v,w]
        e3 = [w,u]
        if e1 not in E:
            E.append(e1)
        if e2 not in E:
            E.append(e2)
        if e3 not in E:
            E.append(e3)
        F.append([u,v,w])
            
        N_f = list(map(float,list(N_f)))
        N.append(N_f)
    G = {}
    G['V'] = range(len(pts0))
    G['E'] = E
    G['F'] = F
    G['pts'] = pts0

    # :JGE
    #########################################
    return G

def create_dodecahedron():
    ##################################
    # JGE:
    
    # JGE created graph but had no points to it
##    G = {'V': [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10,
##               11, 12, 13, 14, 15, 16, 17, 18, 19],
##         'E': [[0, 1], [1, 0], [0, 2], [2, 0],
##               [0, 3], [3,0], [0, 4], [4, 0], [0, 5],
##               [5, 0], [0, 6], [6, 0], [0, 10], [10, 0],
##               [1, 2], [2, 1], [1, 6], [6, 1], [1, 7],
##               [7, 1], [1, 11], [11, 1], [2, 3], [3, 2],
##               [2, 7], [7, 2], [2, 8], [8, 2], [2, 12],
##               [12, 2], [3, 4], [4, 3], [3, 8], [8, 3],
##               [4, 5], [5, 4], [4, 8], [8, 4], [4, 9], 
##                [9, 4], [4, 13], [13, 4], [4, 14], [14, 4],
##               [5, 10], [10, 5], [5, 14], [14, 5], [5, 15],
##               [15, 5], [5, 19], [19, 5], [6, 10], [10, 6],
##               [6, 11], [11, 6], [6, 15], [15, 6], [6,16],
##               [16, 6], [7, 11], [11, 7], [7, 12], [12, 7],
##               [7, 16], [16,7], [7, 17], [17, 7], [8, 12],
##               [12, 8], [8, 13], [13, 8], [8, 17], [17, 8],
##               [8, 18], [18, 8], [9, 13], [13, 9], [9, 14], 
##               [14, 9], [9, 18], [18, 9], [9, 19], [19, 9],
##               [10, 15], [15, 10], [11, 16], [16, 11],
##               [12, 17], [17, 12], [13, 18], [18, 13],
##               [14, 19],[19, 14], [15, 16], [16, 15],
##               [15, 19], [19, 15], [16, 17], [17, 16],
##               [16, 19], [19, 16], [17, 18], [18, 17],
##               [17, 19], [19, 17], [18, 19], [19, 18]], 
##        'F': [[0, 4, 3], [0, 3, 2], [0, 2, 1], [0, 1, 6],
##              [0, 6, 10], [0, 10, 5], [1, 2, 7], [1, 7, 11],
##              [1, 11,6], [2, 3, 8], [2, 8, 12], [2, 12, 7], 
##              [4, 9, 13], [4, 13, 8], [4, 8, 3], [4, 0, 5],
##              [4, 5, 14], [4, 14, 9], [5, 10, 15],
##              [5, 15, 19], [5, 19, 14], [6, 11, 16], [6, 16, 15], 
##              [6, 15, 10], [7, 12, 17], [7, 17, 16],
##              [7, 16, 11], [8, 13, 18], [8, 18, 17], [8,17, 12],
##              [9, 14, 19], [9, 19, 18], [9, 18, 13], 
##             [19, 15, 16], [19, 16, 17], [19, 17, 18]]}

    # :JGE
    ##############################################

    # See icosahedron Copilot method for creating
    # convex hull from points.
    

    # [1] https://en.wikipedia.org/wiki/Dodecahedron
    # where [1] mentions the points like for icosahedron
    pts0 = []
    # eight vertices of a cube
    for x in [1,-1]:
        for y in [1,-1]:
            for z in [1,-1]:
                pt = [x,y,z]
                pts0.append(pt)
        
    phi = (1 + sqrt(5)) / 2
    h = 1/phi # for regular dodecahedron (0.618...)

    for x in [0]:
        for y in [-(1+h),(1+h)]:
            for z in [-(1-h**2),(1-h**2)]:
                  pt = [x,y,z]
                  pts0.append(pt)
    for x in [-(1+h),1+h]:
        for y in [-(1-h**2),(1-h**2)]:
            for z in [0]:
                  pt = [x,y,z]
                  pts0.append(pt) 
    for x in [-(1-h**2),1-h**2]:
        for y in [0]:
            for z in [-(1+h),1+h]:
                  pt = [x,y,z]
                  pts0.append(pt)

    O = aff.Center(pts0)
    O = list(map(float, O))
    
    pts = np.array(pts0)
    hull = ss.ConvexHull(pts)
    hull_F = hull.simplices

    
    ########################################
    # JGE:
    E = []
    F = []
    N = []
    for f in hull_F:
        u,v,w = list(map(int,list(f)))
        A = pts[u]
        B = pts[v]
        C = pts[w]
        N_f = ext.FaceNormalABC(A,B,C)

        # ss.ConvexHull does not orient surface's
        # simplices as desired so reverse listing
        # of f = [u,v,w] to f = [u,w,v] when this
        # occurs
        sgn = _calculate_sign(A, B, C, O)
        if sgn < 0:
            # swap counter-clockwise and clockwise
            u,v,w = u,w,v
            
        e1 = [u,v]
        e2 = [v,w]
        e3 = [w,u]
        if e1 not in E:
            E.append(e1)
        if e2 not in E:
            E.append(e2)
        if e3 not in E:
            E.append(e3)
        F.append([u,v,w])
            
        N_f = list(map(float,list(N_f)))
        N.append(N_f)
    G = {}
    G['V'] = range(len(pts0))
    G['E'] = E
    G['F'] = F
    G['pts'] = pts0

    # :JGE
    #########################################
    return G
