from numpy import array,ones,zeros
from numpy.linalg import det
def PointInSimplexTest(simplex,pt):
    """
    simplex is a numpy array of points and pt is to test if in
    that simplex. All points have dimension d. The point pt
    is a numpy array of coordinate values (floats).

    See http://steve.hollasch.net/cgindex/geometry/ptintet.html
    The tetrahedron pattern here can be applied to simplices of
    any dimension.

    For any simplex was implemented from the method described.

    Comment:
    The determinant of arrays looks similar to a previous
    script that I did that tested for vectors to be
    independent using a determinant with the
    determinant of one of these combinations had to be zero.

    """
    d = len(pt) # dimension of point pt which is a list
    
    A = zeros( (d+2,d+1,d+1), dtype='float')
    D = zeros((d+2), dtype='float')
    for n in range(d+2):
        L = []
        for i in range(d+1):
            if i == n:
                row = list(pt) + [1]
            else:
                row = list(simplex[i]) + [1]
            L.append(row)
        A[n,:,:] = array(L,dtype='float')
    for n in range(d+2):
        D[n] = det(A[n,:,:])

    def sign(x):
        if x < 0:
            return -1
        elif x > 0:
            return 1
        else:
            return 0

    #alpha,beta,gamma,delta barycentric coordinates
    barycentric = []
    for n in range(0,d+1):
        barycentric.append(1.0*D[n]/D[d+1])
    doc = {}
    doc['barycentric'] = barycentric
    doc['degenerate'] = (D[d+1] == 0)
    doc['on_boundary'] = []
    i = 0
    for Di in D[0:d+1]:
        if Di == 0:
            doc['on_boundary'].append(i)
        i += 1
    doc['outside_boundary'] = []
    doc['inside_boundary'] = []
    i = 0
    for Di in D[0:d+1]:
        if not (sign(Di) == sign(D[d+1])):
            doc['outside_boundary'].append(i)
        else:
            doc['inside_boundary'].append(i)
        i += 1
    if len(doc['inside_boundary']) == d+1:
        doc['test'] = True
    else:
        doc['test'] = False
    return doc

def PointInSimplicesTest(points,simplices,pt):
    """
import numpy as np
from scipy.spatial import Delaunay
points = np.array([
    [0,0,0,1],
    [1,0,0,2],
    [0,1,0,4],
    [0,0,1,5],
    [3,1,0,-1],
    [3,0,2,1]])
tri = Delaunay(points)
simplices = tri.simplices

d = len(list(points[0]))
barycentric = [0.1,0.2,0.3,0.2,0]
barycentric[-1] = 1 - sum(barycentric[:-1])
pt = zeros((d),dtype='float')
i = 0
for v in simplices[0]:
    pt = pt + points[v]*barycentric[i]
    i += 1
print pt
test,docs = PointInSimplicesTest(points,simplices,pt)
print docs
print test
    """
    test = False
    docs = []
    i = 0
    for simplex in simplices:
        simplex = map(lambda i: points[i],simplex)
        doc = PointInSimplexTest(simplex,pt)
        doc['_id'] = i
        docs.append(doc)
        test = test or doc['test']
        i += 1
    return test,docs


