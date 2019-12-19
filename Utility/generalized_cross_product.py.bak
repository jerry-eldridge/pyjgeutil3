from numpy import array,zeros,einsum
import os.path
from math import pi, sqrt, acos

def LeviCivita(x,N):
    prod = 1
    for j in range(N):
        for i in range(N):
            if j > i:
                prod *= (x[j] - x[i])
    if prod:
        return prod/abs(prod)
    else:
        return 0

def Epsilon2():
    N = 2
    epsilon = zeros([N,N],dtype='float')
    for i in range(N):
        for j in range(N):
            for k in range(N):
                epsilon[i,j] = LeviCivita([i,j],N)
    return epsilon 

def Epsilon3():
    N = 3
    epsilon = zeros([N,N,N],dtype='float')
    for i in range(N):
        for j in range(N):
            for k in range(N):
                epsilon[i,j,k] = LeviCivita([i,j,k],N)
    return epsilon

def Epsilon4():
    N = 4
    epsilon = zeros([N,N,N,N],dtype='float')
    for i in range(N):
        for j in range(N):
            for k in range(N):
                for l in range(N):
                    epsilon[i,j,k,l] = LeviCivita([i,j,k,l],N)
    return epsilon

def Epsilon(N):
    """
    Note this creates a python script
    "epsilonTMP12345.py" containing a definition
    of epsilon which this routine returns.

    Note if you were to use such, you would want to
    call this routine only once, say the epsilon
    for use, and use that calculated epsilon.

    That is, if you defined cross(u,v) as
    einsum('i,j,k->k',u,v,epsilon)
    you wouldn't want to use Epsilon(3) instead of
    epsilon explicitly else every cross product
    evaluation would write to the output file.
    Instead you run epsilon = Epsilon(3) once
    to get the 3D epsilon. This also demonstrates
    a technique that could be used to define an N-dimensiona
    cross product of N-1 vectors using epsilon = Epsilon(N),
    but you should only create such for each dimension
    and use that python script only once.

    """
    print """
import epsilon_levicivita_TMP
return epsilon_levicivita_TMP.epsilon
"""
    s = "N = %d\n" % N
    s = s+"""
from numpy import array,zeros,einsum

# This is a temp file do not edit it. To produce a different
# Epsilon(N) and cross(A) you need to delete this temp file
# to produce another one, as it will not create such this exists already.

def LeviCivita(x,N):
    prod = 1
    for j in range(N):
        for i in range(N):
            if j > i:
                prod *= (x[j] - x[i])
    if prod:
        return prod/abs(prod)
    else:
        return 0

"""
    s = s + "epsilon = zeros("+str([N]*N)+",dtype='float')\n"
    s = s + ""
    tab = "    "
    for i in range(N):
        s += tab*i+"for i%d in range(%d):\n" % (i,N)
    indices = "["
    for i in range(N):
        t = "i%d," % i
        indices += t
    indices = indices[:-1]
    indices += "]"
    s += tab*N+"epsilon"+indices+"= LeviCivita("+indices+","+str(N)+")\n"

    t = """
def Cross(A):
# For Cross(A), you input N-1 vectors into numpy
# array A, as A[i] being the ith vector. The shape of
# is (n-1,n) created by numpy.array((N-1,N),dtype='float')
"""
    s += t
    symbols = ''.join(map(chr,range(97,123)))
    indices = ""
    for i in range(N-1):
        t = "%s," % symbols[i]
        indices += t
    t = ''.join(map(chr,range(97,97+N)))
    indices += t+"->"
    t = symbols[N-1]
    indices += t
    s += tab+"B = einsum('"+indices+"',"
    for i in range(N-1):
        t = "A[%d,:]," % i
        s += t
    s += "epsilon)\n"
    s += tab+"return B"

    fn_prefix = "epsilon_levicivita_TMP"
    fn = fn_prefix + ".py"
    print "Writing to a file:", fn
    f = open(fn,'w')
    f.write(s)
    f.close()
    import epsilon_levicivita_TMP
    return epsilon_levicivita_TMP.epsilon

def cross3(u,v):
    """
    u and v have to be same dimensions
    This is the usual cross product
    of two 3D vectors.
    """
    A = array(u)
    B = array(v)
    n = A.shape[0]
    epsilon = Epsilon3()
    return einsum('i,j,ijk->k',A,B,epsilon)

def cross4(u,v,w):
    """
    u and v have to be same dimensions. This
    is a generalization of cross(u,v) in 3D
    to cross(u,v,w) using three 4D vectors
    though unclear if a 4D geometric interpretation
    is the same, it is generalized by

    cross4(u,v,w)[l] = u[i]*v[j]*w[k]*epsilon[i,j,k,l]

    einstein summation where epspilon is the
    levi-civita symbol on four indices.
    """
    A = array(u)
    B = array(v)
    C = array(w)
    n = A.shape[0]
    epsilon = Epsilon4()
    return einsum('i,j,k,ijkl->l',A,B,C,epsilon)

def cross2(u):
    """
    u and v have to be same dimensions. This
    is a generalization of cross(u,v) in 3D
    to cross(u,v,w) using three 4D vectors
    though unclear if a 4D geometric interpretation
    is the same, it is generalized by

    cross4(u,v,w)[l] = u[i]*v[j]*w[k]*epsilon[i,j,k,l]

    einstein summation where epspilon is the
    levi-civita symbol on four indices.
    """
    A = array(u)
    n = A.shape[0]
    epsilon = Epsilon2()
    return einsum('i,ij->j',A,epsilon)

def dotprod(u,v):
    A = array(u)
    B = array(v)
    return einsum('i,i->',A,B)

def norm(u):
    A = array(u)
    return sqrt(dotprod(list(A),list(A)))

def normalize(u):
    val = norm(u)
    A = array(u)
    if val < 1e-8:
        return u
    A = A/val
    return list(A)

def metric(u,v):
    A = array(u)
    B = array(v)
    return norm(list(A-B))

def tripleprod(u,v,w):
    A = array(u)
    B = array(v)
    C = array(w)
    epsilon = Epsilon3()
    return einsum('k,i,j,ijk->',A,B,C,epsilon)

def angle(u,v):
    return acos(dotprod(normalize(u),normalize(v)))*180/pi
