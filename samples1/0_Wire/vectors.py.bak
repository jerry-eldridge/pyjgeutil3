from numpy import zeros,array,ones, eye, dot
from math import pi,cos,sin,sqrt,atan2,acos,asin

# "Introduction to Algorithms", Cormen et al (turned_left)
# "OpenGL Programming Guide", 7ed, Shreiner (rotation matrix,
# frustrum matrix)
#

def lerp(A,B,t):
    C = array(A)*(1-t) + array(B)*t
    return list(C)

def pnorm(A,p):
    """
    The regular l**p norm of vector A (distance formula).
    """
    try:
        N = A.shape[0]
    except:
        N = len(A)
    S = 0
    for i in range(N):
        S += abs(A[i])**p
    return S**(1.0/p)

def norm(A):
    """
    The regular l**2 norm of vector A (distance formula).
    """
    return pnorm(A,2)
def metric(A,B):
    """
    Distance metric between vectors A and B
    Eg,
    A = [1,2,0]
    B = [10,20,20]
    """
    C = array(A)- array(B)
    return norm(list(C))
def Distance(A,B):
    return metric(A,B)
def cross(A,B):
    """
    Cross product between vectors A and B
    """
    C = array([
        A[1]*B[2]-B[1]*A[2],
        -(A[0]*B[2]-B[0]*A[2]),
        A[0]*B[1]-B[0]*A[1]])
    return C
def dotprod(A,B):
    """
    Dot product between vectors A and B
    """
    try:
        N = A.shape[0]
    except:
        N = len(A)
    S = 0
    for i in range(N):
        S += A[i]*B[i]
    return S

def normal(A):
    """
    Normal vector to vector A
    """
    n = cross([0,0,1],A)
    n = n/norm(n)
    return n

def reflect(v_i,T):
    """
    Reflect incidence vector v_i about normal to tangent T
    """
    N = normal(T)
    vx = dotprod(v_i,T)*T/norm(T)**2
    vy = dotprod(v_i,N)*N/norm(N)**2
    v_f = -vx + vy
    return v_f

def angle(A,B):
    """
    Angle between vectors A and B in degrees
    """
    d = dotprod(A,B)/(norm(A)*norm(B))
    theta = acos(d)
    return theta*180/pi # degrees

def DirectionCosines(A):
    """
    orientation angles between x axis, y axis and z axis and 3D
    vector A.
    """
    return [angle(A,[1,0,0]),angle(A,[0,1,0]), angle(A,[0,0,1])]

def turned_left(p0, p1, p2):
    """
    Returns turned left 1,went straight 0,or turned right -1
    p0,p1,p2 are lists converted in procedure to numpy arrays
    """
    p0,p1,p2 = map(array,[p0,p1,p2])
    v = cross(p1-p0,p2-p0)[2]
    if v <> 0:
        v = abs(v)/v
    return v

def rotation_matrix(degrees,x,y,z):
    """
    4x4 rotation matrix for axis [x,y,z] rotated by angle, degrees
    called R, then an extended coordinate X = [x0,x1,x2,1] is
    XP = R*X and rotated point is [XP[0],XP[1],XP[2]].
    """
    v = array([[x,y,z]]).T
    u = v/norm(v)
    S = array([
        [0,-u[2],u[1]],
        [u[2],0,-u[0]],
        [-u[1],u[0],0]])
    I = array([
        [1,0,0],
        [0,1,0],
        [0,0,1]])
    uu = u.dot(u.T)
    M = uu+cos(degrees*pi/180)*(I-uu)+sin(degrees*pi/180)*S
    R = zeros((4,4),dtype="float32")
    R[:3,:3]=M
    R[3,3] = 1
    return R
def translation_matrix(x,y,z):
    """
    4x4 translation matrix that maps a point pt from
    pt[0] += x
    pt[1] += y
    pt[2] += z
    pt[3] = pt[3] # w = 1
    """
    T = eye(4,4,dtype="float32")
    T[0,3] = x
    T[1,3] = y
    T[2,3] = z
    T[3,3] = 1
    return T
def frustrum_matrix(left,right,bottom,top,near,far):
    """
    4x4 frustrum matrix that maps a point pt
    to perspective transform from 3D to 2D
    x = x/z
    y = y/z
    z = 1
    w = 1
    though uses a frustrum square (left,top) to (right,bottom)
    of depth far to near.
    
    T = eye(4,4,dtype="float32")
    rl = (right-left)*1.0
    tb = (top-bottom)*1.0
    fn = (far-near)*1.0
    T[0,0] = 2*near/rl
    T[0,2] = (right+left)/rl
    T[1,1] = 2*near/tb
    T[1,2] = (top+bottom)/tb
    T[2,2] = -(far+near)/fn
    T[2,3] = -2*far*near/fn
    T[3,2] = -1
    T[3,3] = 0
    """
    T = eye(4,4,dtype="float32")
    rl = (right-left)*1.0
    tb = (top-bottom)*1.0
    fn = (far-near)*1.0
    T[0,0] = 2*near/rl
    T[0,2] = (right+left)/rl
    T[1,1] = 2*near/tb
    T[1,2] = (top+bottom)/tb
    T[2,2] = -(far+near)/fn
    T[2,3] = -2*far*near/fn
    T[3,2] = -1
    T[3,3] = 0
    return T
def scale_matrix(sx,sy,sz):
    """
    4x4 scale matrix that scales a point pt
    x = sx*x
    y = sy*y
    z = sz*z
    w = 1
    """
    T = eye(4,4,dtype="float32")
    T[0,0] = sx
    T[1,1] = sy
    T[2,2] = sz
    T[3,3] = 1
    return T

def rotate(A,ref,degrees):
    """
    Rotate a vector A about a reference vector ref by
    degrees angle.
    """
    axis = cross(ref,A)
    if norm(axis) == 0:
        return array(A)
    axis = axis/norm(axis)
    R = rotation_matrix(degrees,axis[0],axis[1],axis[2])
    X = array([A[0],A[1],A[2],1]).T
    XP = R.dot(X)
    B = XP[:3].T
    return B

def refract(v_i,T,n_i,n_f):
    """
    Refract an incidence vector about normal to tangent T
    where incidence dielectric has refractive index n_i
    and final dielectric has refractive index n_f. Eg,
    n_air = 1.00027712 and n_water = 1.33283 (temp=20C).

    Eg,
    n_air = 1.00027712
    n_water = 1.33283
    T = array([1,0,0])*50
    v_i = array([100,20,0])
    v_r = refract(v_i,T,n_air,n_water)

    http://en.wikipedia.org/wiki/Snell%27s_law
    mentions a way to calculate v_refract and v_reflect
    but the methods require sometimes reversing the normal
    which causes bad results. In this method, we just
    rotate the incidence ray and reflect any ray with n_i > n_f.
    """
    N = normal(T)
    if (dotprod(v_i,N)<0):
        N = -N
    a_i = angle(v_i,N) # angle in radians
    try:
        a_r = asin(1.0*sin(a_i*pi/180.0)*n_i/n_f)*180.0/pi
    except:
        return reflect(v_i,T)
    if n_i == n_f:
        return -v_i
    v_f = rotate(v_i,N,-a_i+180+a_r)
    return v_f

def component(b,a):
    """
    The component of a in b direction
    """
    return dotprod(a,b)/norm(b)
def component_curry(b):
    """
    The curried form of component(b,a) = component_curry(b)(a)
    """
    def f(a):
        return component(b,a)
    return f

def perpendicular(A,B):
    """
    The perpendicular component of B in A direction
    """
    Bpar = component(A,B)*array(A)/norm(A)
    Bper = array(B) - Bpar
    return list(Bper)

def parallel(A,B):
    """
    The parallel component of B in A direction
    """
    Bpar = component(A,B)*array(A)/norm(A)
    Bper = array(B) - Bpar
    return list(Bpar)

def perpendicular_curry(A):
    """
    Curried form of perpendicular(A,B) = perpendicular_curry(A)(B)
    """
    def f(B):
        return perpendicular(A,B)
    return f

def parallel_curry(A):
    """
    Curried form of parallel(A,B) = parallel_curry(A)(B)
    """
    def f(B):
        return parallel(A,B)
    return f

