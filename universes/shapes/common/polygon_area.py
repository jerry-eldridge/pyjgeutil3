# http://en.wikipedia.org/wiki/Centroid#Centroid_of_polygon
def PolygonCentroid(p):
    np = len(p)
    if np == 0:
        return [0,0], 0
    A = 0
    for i in range(np-1):
        A += (p[i][0]*p[i+1][1]-p[i+1][0]*p[i][1])
    i = np-1
    A += (p[i][0]*p[0][1]-p[0][0]*p[i][1])
    A /= 2.0

    Cx = 0
    Cy = 0
    for i in range(np-1):
        Cx += (p[i][0]+p[i+1][0])*(p[i][0]*p[i+1][1]-p[i+1][0]*p[i][1])
        Cy += (p[i][1]+p[i+1][1])*(p[i][0]*p[i+1][1]-p[i+1][0]*p[i][1])
    i = np-1;
    Cx += (p[i][0]+p[0][0])*(p[i][0]*p[0][1]-p[0][0]*p[i][1])
    Cy += (p[i][1]+p[0][1])*(p[i][0]*p[0][1]-p[0][0]*p[i][1])
    epsilon = 0.0001
    if abs(A) > epsilon:
        Cx /= (6.0*A)
        Cy /= (6.0*A)

    centroid = [Cx,Cy]
    return centroid,A

def PointInPolygonTest(p,x,y):
     """
http://local.wasp.uwa.edu.au/~pbourke/geometry/insidepoly/ Point in 
Polygon Test
     "The following code is by Randolph Franklin, it returns 1 for 
interior points and 0 for exterior points."
     -- pbourke webpage. Code below based on the webpage code.
     The Python code based on
https://github.com/jerry-eldridge/emma/blob/master/build/core/polygon.cpp
     """
     N = len(p)
     c = 0
     i = 0
     j = N-1
     while i < N:
         support = ((((p[i][1] <= y) and (y < p[j][1])) \
                     or ((p[j][1] <= y) and (y < p[i][1]))) \
                    and (x < (p[j][0] - p[i][0]) * (y - p[i][1]) / 
(p[j][1] - p[i][1]) + p[i][0]))
         if support:
             c = not c
         j = i
         i += 1
     return c
