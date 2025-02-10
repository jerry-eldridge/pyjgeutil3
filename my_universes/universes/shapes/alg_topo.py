from . import extrusion as ext
from .common import graph as gra
from .common import affine as aff

import numpy as np

from copy import deepcopy

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))

def copy_graph(G):
    G2 = {}
    K = list(G.keys())
    for key in K:
        G2[key] = deepcopy(G[key])
    return G2

def AT_Cylinder(path, cross_sections,
        bcap=True,ecap=True,closed=False):
    m = len(cross_sections[0])
    G = gra.Cn(m)
    G['pts'] = deepcopy(cross_sections[0])
    m = len(G['V'])
    n = len(path)
    k = n
    assert(n>=3)
    H = ext.ExtrudeGraph(G,k)
    pts = []
    F = []
    N = []
    G0 = deepcopy(G)
    G0['F'] = [G['V'][:3]]
    N0 = ext.FaceNormal(G0,0)
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
        q_k = ext.AimAxis(axis1,axis2)
        s_k = [1,1,1]
        t_k = list(A)
        pts_k = deepcopy(cross_sections[i])
        C_k = aff.Center(pts_k)
        pts_k = aff.Translate(pts_k,-C_k[0],-C_k[1],-C_k[2],align=False)
        pts_k = aff.Rotate(pts_k,q_k,align=False)
        pts_k = aff.Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
        pts_k = aff.Translate(pts_k,t_k[0],t_k[1],t_k[2],align=False)        
        pts = pts + pts_k
    pts_k = deepcopy(cross_sections[-1])
    C_k = aff.Center(pts_k)
    pts_k = aff.Translate(pts_k,-C_k[0],-C_k[1],-C_k[2],align=False)
    pts_k = aff.Rotate(pts_k,q_k,align=False)
    pts_k = aff.Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
    pts_k = aff.Translate(pts_k,t_k[0],t_k[1],t_k[2],align=False)        
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
                   G_f = ext.ExtrudeGraph(G,2)
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
        C0 = aff.Center(pts0)
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
            N_fi = ext.FaceNormal(G_f,0)
            N.append(N_fi)
    if ecap:
        i = n-1
        pts0 = deepcopy(pts[i*m:(i+1)*m])
        C0 = aff.Center(pts0)
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
            N_fi = ext.FaceNormal(G_f,0)
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
    H = ext.ExtrudeGraph(G,k)
    pts = []
    F = []
    N = []
    G0 = deepcopy(G)
    G0['F'] = [G['V'][:3]]
    N0 = ext.FaceNormal(G0,0)
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
        q_k = ext.AimAxis(axis1,axis2)
        s_k = [1,1,1]
        t_k = list(A)
        pts_k = deepcopy(cross_sections[i])
        C_k = aff.Center(pts_k)
        pts_k = aff.Translate(pts_k,-C_k[0],-C_k[1],-C_k[2],align=False)
        pts_k = aff.Rotate(pts_k,q_k,align=False)
        pts_k = aff.Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
        pts_k = aff.Translate(pts_k,t_k[0],t_k[1],t_k[2],align=False)        
        pts = pts + pts_k
    pts_k = deepcopy(cross_sections[-1])
    C_k = aff.Center(pts_k)
    pts_k = aff.Translate(pts_k,-C_k[0],-C_k[1],-C_k[2],align=False)
    pts_k = aff.Rotate(pts_k,q_k,align=False)
    pts_k = aff.Scale(pts_k, s_k[0],s_k[1],s_k[2],align=False)
    pts_k = aff.Translate(pts_k,t_k[0],t_k[1],t_k[2],align=False)        
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
                   G_f = ext.ExtrudeGraph(G,2)
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
            N_fi = ext.FaceNormal(G_f,0)
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
            N_fi = ext.FaceNormal(G_f,0)
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
    
        
