from numpy import array,ones,zeros
from numpy.linalg import det
def PointInTetrahedronTest(simplex,x,y,z):
    """
    See http://steve.hollasch.net/cgindex/geometry/ptintet.html

    The pattern here can be applied to simplices of
    any dimension.

    Comment:
    The determinant of arrays looks similar to a previous
    script that I did that tested for vectors to be
    independent using a determinant with the
    determinant of one of these combinations had to be zero.

    """
    x1,y1,z1 = simplex[0]
    x2,y2,z2 = simplex[1]
    x3,y3,z3 = simplex[2]
    x4,y4,z4 = simplex[3]

    # for Ai, the ith row of 1 to 4 is replaced by the
    # homogeneous coordinate of point
    A0 = array([
        [x1,y1,z1,1],
        [x2,y2,z2,1],
        [x3,y3,z3,1],
        [x4,y4,z4,1]],dtype='float')
    A1 = array([
        [ x, y, z,1],
        [x2,y2,z2,1],
        [x3,y3,z3,1],
        [x4,y4,z4,1]],dtype='float')
    A2 = array([
        [x1,y1,z1,1],
        [ x, y, z,1],
        [x3,y3,z3,1],
        [x4,y4,z4,1]],dtype='float')
    A3 = array([
        [x1,y1,z1,1],
        [x2,y2,z2,1],
        [ x, y, z,1],
        [x4,y4,z4,1]],dtype='float')
    A4 = array([
        [x1,y1,z1,1],
        [x2,y2,z2,1],
        [x3,y3,z3,1],
        [ x, y, z,1]],dtype='float')
    D0 = det(A0)
    D1 = det(A1)
    D2 = det(A2)
    D3 = det(A3)
    D4 = det(A4)
    def sign(x):
        if x < 0:
            return -1
        elif x > 0:
            return 1
        else:
            return 0
    s0 = sign(D0)
    s1 = sign(D1)
    s2 = sign(D2)
    s3 = sign(D3)
    s4 = sign(D4)
    #alpha,beta,gamma,delta barycentric coordinates
    barycentric = (1.0*D1/D0,1.0*D2/D0,1.0*D3/D0,1.0*D4/D0)
    doc = {}
    doc['barycentric'] = barycentric
    doc['degenerate'] = (D0 == 0)
    doc['on_boundary'] = []
    i = 1
    for D in [D1,D2,D3,D4]:
        if D == 0:
            doc['on_boundary'].append(i)
        i += 1
    doc['outside_boundary'] = []
    doc['inside_boundary'] = []
    i = 1
    for D in [D1,D2,D3,D4]:
        if not (sign(D) == sign(D0)):
            doc['outside_boundary'].append(i)
        else:
            doc['inside_boundary'].append(i)
        i += 1
    if len(doc['inside_boundary']) == 4:
        doc['test'] = True
    else:
        doc['test'] = False
    return doc
