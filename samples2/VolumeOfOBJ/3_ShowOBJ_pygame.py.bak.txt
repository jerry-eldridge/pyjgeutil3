import polygon_area as pa
import QuaternionGroup as QG
import vectors as vec

import numpy as np
from math import pi,acos

from copy import deepcopy

from scipy.spatial import KDTree

BIGDATA = r"C:/_BigData/_3D/my_scenes/"

def MergePoints(pts,epsilon=1e-2):
    kdtree = KDTree(pts)
    L = range(len(pts))
    for pt in map(lambda k: pts[k],L):
        ball = kdtree.query_ball_point(pt,epsilon)
        if len(ball) > 1:
            ball = ball[1:]
            for k in ball:
                try:
                    L.remove(k)
                except:
                    continue
    return [map(lambda k: pts[k], L),L]

def Reduce(G,epsilon=1):
    pts,S = MergePoints(G['pts'],epsilon)
    print len(S)
    v = S[0]
    V = []
    d = {}
    i = 0
    for u in G['V']:
        d[u] = i
        if u in S:
            continue
        else:
            V.append(i)
            i += 1
    E = []
    for e in G['E']:
        u0,v0 = e
        f = [u0,v0]
        g = map(lambda w: d[w],f)
        if len(set(g))==2:
            if g not in E:
                E.append(g)
    F = []
    for f in G['F']:
        g = map(lambda w: d[w],f)
        if len(set(g))>=3:
            if g not in F:
                F.append(g)
    G2 = {}
    G2['V'] = V
    G2['E'] = E
    G2['F'] = F
    G2['pts']=pts
    G2 = AddNormals(G2)
    return G2

def PseudoToGraph(G):
    V = range(len(G['V']))
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

def area(pts):
    C,A = pa.PolygonCentroid(pts)
    return A

def AddNormals(G):
    G['N'] = []
    for face in G['F']:
        polygon = map(lambda v: G['pts'][v],face)
        A,B,C = polygon[:3]
        A = np.array(A)
        B = np.array(B)
        C = np.array(C)
        V1 = A-C
        V2 = A-B
        N = np.cross(V1,V2)
        N = list(N/np.linalg.norm(N))
        G['N'].append(N)
    return G

def Transform_3D_to_2D(polygon1,normal):
    # Create V1 and V2 vectors of polygon1 normal and [0,0,1] z-axis
    V1 = normal
    V2 = [0,0,1] # z-axis
    V1 = np.array(V1)
    V2 = np.array(V2)
    # create a rotation axis to rotate V1 to V2
    # and compute angle in degrees of rotation, obtain quaternion for this
    axis = np.cross(V1,V2)
    angle = acos(np.inner(V1,V2)/(np.linalg.norm(V1)*np.linalg.norm(V2)))
    degrees = angle*180/pi
    q = QG.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
    # compute rotation matrix R for quaternion q
    epsilon = 1e-8
    R = q.rotation_matrix()
    # Now transform polygon1 to polygon2 so it
    # has normal [0,0,1] in z-axis using rotation R
    polygon2 = []
    pt0 = list(np.einsum('ij,j->i',R,polygon1[0]))
    z = pt0[2] # z-component of first point
    for pt in polygon1:
        pt2 = list(np.einsum('ij,j->i',R,pt))
        pt2[2] -= z # translate pt2 by [0,0,-z]
        polygon2.append(pt2)
    C = np.array([0,0,0])
    for pt in polygon2:
        C = C + np.array(pt)
    C = C/(1.0*len(polygon2))
    for i in range(len(polygon2)):
        pt = polygon2[i]
        pt2 = list(np.array(pt)-C)
        polygon2[i] = pt2        
    return polygon2

def area3d(G,i):
    face = G['F'][i]
    polygon1 = map(lambda v: G['pts'][v],face)
    normal1 = G['N'][i]
    polygon2 = Transform_3D_to_2D(polygon1,normal1)
    A = area(polygon2)
    C = np.array([0,0,0])
    N = len(polygon1)
    for pt in polygon1:
        C = C + np.array(pt)
    C = C/(1.0*N)
    C = list(C)
    return C,A

def volume(G):
    V = 0
    # First make sure volume is not signed volume
    M = 1e5 # use big number to translate graph 
    G = Translate(G,[M,M,M])
    for i in range(len(G['F'])):
        C,dS = area3d(G,i)
        n = G['N'][i]
        face = G['F'][i]
        polygon1 = map(lambda v: G['pts'][v],face)
        F = np.array(C)/3.0 
        val = -np.inner(F,n)*abs(dS)
        V += val
    return V

def Translate(G,t):
    for i in range(len(G['pts'])):
        pt = G['pts'][i]
        pt[0] += t[0]
        pt[1] += t[1]
        pt[2] += t[2]
        G['pts'][i] = pt
    return G

def OBJ2Graph(OBJ):
    lines = OBJ.split("\n")
    G = {}
    G['pts'] = []
    for line in lines:
        line = line.strip()
        tokens = line.split(' ')
        if tokens[0] == 'v':
            c,x,y,z = tokens
            x = float(x)
            y = float(y)
            z = float(z)
            G['pts'].append([x,y,z])
    G['V'] = range(len(G['pts']))
    G['F'] = []
    G['E'] = []
    for line in lines:
        tokens = line.split(' ')
        if tokens[0] == 'f':
            L = tokens[1:]
            face = []
            for tok in L:
               v = tok.split('/')[0]
               v = int(v)-1 # indices start at 0 not 1
               face.append(v)
            G['F'].append(face)
            N = len(face)
            for i in range(N):
                u = face[i]
                v = face[(i+1)%N]
                e = [u,v]
                if e not in G['E']:
                    G['E'].append(e)
    G = AddNormals(G)
    return G


fn = BIGDATA+"g_bread_man.obj"
f = open(fn,'r') # open for reading 'r'
OBJS = f.read()
f.close() # close

G = OBJ2Graph(OBJS)
##print "len(G['V'])=",len(G['V'])
##print "len(G['E'])=",len(G['E'])
##print "len(G['F'])=",len(G['F'])
##print "volume(G)=",volume(G)
#G = Reduce(G,epsilon=10)
print "len(G['V'])=",len(G['V'])
print "len(G['E'])=",len(G['E'])
print "len(G['F'])=",len(G['F'])
print "volume(G)=",volume(G)

########################################
import pygame
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

def Center(pts):
    C = np.array([0,0,0])
    for pt in pts:
        A = np.array(pt)
        C = C + A
    C = C/(1.0*len(pts))
    return list(C)

def Scale(pts,sx,sy,sz):
    PTS = []
    for pt in pts:
        x,y,z = pt
        x *= sx
        y *= sy
        z *= sz
        pt = [x,y,z]
        PTS.append(pt)
    return PTS

def Translate(pts,tx,ty,tz):
    PTS = []
    for pt in pts:
        x,y,z = pt
        x += tx
        y += ty
        z += tz
        pt = [x,y,z]
        PTS.append(pt)
    return PTS

PTS = deepcopy(G['pts'])
s = 0.02 # to make unit size
s *= 1.0/70 # double
PTS = Scale(PTS,s,s,s)
C = Center(PTS)
PTS = Translate(PTS,-C[0],-C[1],-C[2])
verticies = tuple(map(tuple,PTS))
edges = tuple(map(tuple,G['E']))

def Object():
    glBegin(GL_LINES)
    for edge in edges:
        for vertex in edge:
            glVertex3fv(verticies[vertex])
    glEnd()
    return

def Map(pt):
    pts0 = [pt]
    pts0 = Translate(pts0,-C[0],-C[1],-C[2])
    pts0 = Scale(pts0,s,s,s)
    return pts0[0]

def Object2(color):
    glBegin(GL_TRIANGLES)
    for f in G['F']:
        v1,v2,v3 = f
        pt = G['N'][v1]
        glNormal3f(pt[0],pt[1],pt[2])
        pt = G['pts'][v1]
        pt = Map(pt)
        glVertex3f(pt[0],pt[1],pt[2])
        pt = G['N'][v2]
        glNormal3f(pt[0],pt[1],pt[2])
        pt = G['pts'][v2]
        pt = Map(pt)
        glVertex3f(pt[0],pt[1],pt[2])
        pt = G['N'][v3]
        glNormal3f(pt[0],pt[1],pt[2])
        pt = G['pts'][v3]
        pt = Map(pt)
        glVertex3f(pt[0],pt[1],pt[2])
    glEnd()
    return


def main():
    pygame.init()
    display = (800,600)
    pygame.display.set_mode(display, DOUBLEBUF|OPENGL)
    glClearColor(0.0,0.0,0.0,0)

    glEnable(GL_DEPTH_TEST)

    # do wireframe
    glPolygonMode(GL_FRONT_AND_BACK,GL_LINE)
    
    gluPerspective(45, (display[0]/display[1]), 0.1, 50.0)

    glTranslatef(0.0,0.0, -5)

    red = [1,0,0]
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        glRotatef(1, 3, 1, 1)
        glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        Object2(red)
        pygame.display.flip()
        pygame.time.wait(10)

main()
