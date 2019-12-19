from scipy.optimize import minimize
from vectors import norm
from numpy import array,zeros

def RaySphereIntersection(r_ray,r_d,r_sphere,R):
    def Energy(X):
        t = X
        if t < 0 or t > 1:
            return 1e8
        rray = array(list(r_ray))
        rd = array(list(r_d))
        r = rray + t*rd
        rsphere = array(list(r_sphere))
        E = norm(r-rsphere)**2 - R**2
        return E
    t = minimize(Energy,[0]).x[0]
    r = list(array(list(r_ray)) + t*array(list(r_d)))
    E = Energy(t)
    return E <= 0

def PathSphereIntersection(doc,path,r_sphere,R):
    pts = doc['pts']
    flag = False
    for e in path:
        u,v = e
        r_ray = pts[u]
        r_d = list(array(pts[v])-array(pts[u]))
        flag = flag or RaySphereIntersection(r_ray,r_d,r_sphere,R)
        if flag:
            #print path,u,v
            return flag
    return flag
