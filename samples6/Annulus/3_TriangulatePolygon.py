import scipy.spatial as ss
import matplotlib.pyplot as plt
from copy import deepcopy
from math import cos,sin,pi
import numpy as np

import sys
sys.path.append(\
    r"C:/Users/jerry/Desktop/_Art/my_universes")
import universes.shapes.common.affine as aff
import universes.shapes.common.triangulate_polygon as tpo

lerp = lambda A,B,t: \
       list(map(float,list(\
           np.array(A)*(1-t) + np.array(B)*t)))

######################################################
# [1] excerpt code provided by Microsoft Copilot,
# a large language model.

def plot_2d_triangles(pts, F):
    #print(f"|F| = {len(F)}")
    fig, ax = plt.subplots()
    
    # Plot points for better visualization
    pts = np.array(pts)
    ax.scatter(pts[:, 0], pts[:, 1], color='b')
    
    # Plot triangles
    for face in F:
        triangle = pts[face]
        triangle = np.append(triangle, [triangle[0]],
                    axis=0)  # Close the triangle
        ax.plot(triangle[:, 0], triangle[:, 1], 'r-')
        ax.fill(triangle[:, 0], triangle[:, 1],
                alpha=0.2, color='cyan', edgecolor='r')

    #L_O_i = np.array(L_O_i)
    #ax.scatter(L_O_i[:,0],L_O_i[:,1],color='g')
    
    plt.show()
    return

# end [1].
####################################################

m = 20
m1 = m
m2 = m
a1 = 300
b1 = 300
pts1 = []
for i in range(m1):
    t = i/(m1-1)
    x = a1*cos(2*pi*t)
    y = b1*sin(2*pi*t)
    pt = [x,y]
    pts1.append(pt)
O = np.mean(pts1,axis=0)
O = list(map(float,list(O)))
Q = [(pts1,1)]
k = 3
for j in range(k):
    m2 = 10
    pts_k = []
    t2 = 2*pi*j/(k+1)
    cx = 150*cos(t2) + O[0]
    cy = 150*sin(t2) + O[1]
    for i in range(m2):
        t = i/(m2-1)
        x = 30*cos(2*pi*t)+cx
        y = 30*sin(2*pi*t)+cy
        pt = [x,y]
        pts_k.append(pt)
    Q = Q + [(pts_k,-1)]

ttt = .001
F,pts = tpo.triangulate_polygons(Q,ttt)
plot_2d_triangles(pts, F)
