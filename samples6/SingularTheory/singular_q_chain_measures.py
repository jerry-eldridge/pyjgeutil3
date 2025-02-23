import AT_singular_theory as atst

import numpy as np

def line_integral(omega_1q,f1):
    s = 0
    for i in range(len(omega_1q.S)):
        sigma = omega_1q.S[i]
        if sigma.q != 1:
            continue
        facet1 = sigma**1
        facet2 = sigma**2
        orientation = omega_1q.V[i].x
        A = facet1.P()[0]
        B = facet2.P()[0]
        ds = orientation*d(A,B)
        s = s + f1(A)*ds
    return s

def vector_area_triangle(P):
    epsilon = 1e-8
    Q = np.array(P)
    v1 = Q[1]-Q[0]
    v2 = Q[2]-Q[0]
    v = np.cross(v1,v2)
    v_mag = np.linalg.norm(v)
    if abs(v_mag) > epsilon:
        normal = v/v_mag
    else:
        normal = v
    dA = 0.5*v_mag*normal
    return dA,normal

def surface_integral(omega_2q,f2):
    s = 0
    for i in range(len(omega_2q.S)):
        sigma = omega_2q.S[i]
        if sigma.q != 2:
            continue
        P = sigma.P()
        orientation = omega_2q.V[i].x
        dA = vector_area_triangle(P)[0]
        pt = P[0]
        s = s + orientation*np.inner(f2(pt),dA)
    return s

mu1 = lambda f1: lambda omega: \
               line_integral(omega,f)

import numpy as np
d = lambda A,B: np.linalg.norm(np.array(B)-np.array(A))

def Indices(sigma):
    L = []
    for i in range(len(sigma.S)):
        f = sigma.S[i]
        v = sigma.V[i]
        P = f.P()
        Q = [pts.index(p)+1 for p in P]
        L.append((Q,v.x))
    return L

def volume_3q(omega_3q):
    s = 0
    for i in range(len(omega_3q.S)):
        # omega_3d contains tetrahedrons so
        # iterate through tetrahedrons sigma
        sigma = omega_3q.S[i]
        if sigma.q != 3:
            continue
        # get boundary to each tetrahedron bdysigma
        bdysigma = atst.bdy(sigma)
        # bdysigma contains faces tau
        for j in range(len(bdysigma.S)):
            tau = bdysigma.S[j]
            if tau.q != 2:
                continue
            P = sigma.P()
            orientation = bdysigma.V[j].x
            dA,n = vector_area_triangle(P)
            C = np.mean(P,axis=0)
            F = C/3.0
            val = -np.inner(F,dA)*orientation
            s = s + abs(val)
    val = np.linalg.norm(s)
    return s

def volume_2q(omega_2q):
    s = 0
    for i in range(len(omega_2q.S)):
        tau = omega_2q.S[i]
        if tau.q != 2:
            continue
        P = tau.P()
        orientation = omega_2q.V[i].x
        dA,n = vector_area_triangle(P)
        C = np.mean(P,axis=0)
        F = C/3.0
        val = -np.inner(F,dA)*orientation
        s = s + val
    val = np.linalg.norm(s)
    return s
