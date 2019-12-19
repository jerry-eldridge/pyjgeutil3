# We use [1] to obtain a test for two cylinders intersecting
#
# References:
# [1] https://www.youtube.com/watch?v=HC5YikQxwZA
# "Shortest distance between two Skew lines in 3D space"
# (DLBmaths) for obtaining shortest distance

from math import sqrt
from numpy import array,zeros
from scipy.optimize import fmin

def norm(pt):
    val = sqrt(pt[0]**2 + pt[1]**2 + pt[2]**2)
    return val

def getpt(x,v,s):
    pt = x + s*v
    return pt

def dist(a,*args):
    try:
        x1,v1,x2,v2 = args
    except:
        print "Error: no args (x1,v1,x2,v2) provided"
        return 1e80
    s = a[0]
    t = a[1]
    pt1 = getpt(x1,v1,s)
    pt2 = getpt(x2,v2,t)
    r12 = pt2 - pt1
    d = norm(r12)
    return d

# cylinder from pt11 to pt12 of radius r1
# cylinder from pt21 to pt22 of radius r2
# return boolean if cylinders intersect
# Check if closest points (s,t) between cylinders are on
# both cylinders line segment. If not return false.
# else if distance between closest points is less than
# sum or cylinder radii return true else false.
def CylinderIntersectionTest(pt11,pt12,r1, pt21, pt22, r2):
    x1 = pt11
    v1 = pt12 - pt11
    x2 = pt21
    v2 = pt22 - pt21
    pt = (0,0)
    tup = (x1,v1,x2,v2)
    a = fmin(dist,pt,args=tup,disp=False)
    print "a: ", a
    d = dist(a, x1,v1,x2,v2)
    print "d,r1,r2: ", d,r1,r2
    test1 =(a[0] >= 0) and (a[0] <= 1) and \
           (a[1] >= 0) and (a[1] <= 1)
    test2 = d < (r1 + r2)
    test = test1 and test2
    return test

"""
pt11 = array([1,3,0])
pt12 = array([2,7,0])
pt21 = array([0,2,0])
pt22 = array([3,3,0])
r1 = 0.5
r2 = 0.5
print CylinderIntersectionTest(pt11,pt12,r1,pt21,pt22,r2)
"""




