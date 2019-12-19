import numpy as np
from scipy.linalg import expm

# O(1,3)
act = lambda A,X: map(lambda z: z.real,list(np.einsum('ij,j->i',A,X)))
class LorenzGroup:
    def __init__(S,theta,beta):
        assert(len(theta)==3 and len(beta)==3)
        i = complex(0,1)
        S.J1 = i*np.array([
            [0,0,0,0],
            [0,0,0,0],
            [0,0,0,-1],
            [0,0,1,0]])
        S.J2 = i*np.array([
            [0,0,0,0],
            [0,0,0,1],
            [0,0,0,0],
            [0,-1,0,0]])
        S.J3 = i*np.array([
            [0,0,0,0],
            [0,0,-1,0],
            [0,1,0,0],
            [0,0,0,0]])
        S.K1 = i*np.array([
            [0,-1,0,0],
            [-1,0,0,0],
            [0,0,0,0],
            [0,0,0,0]])
        S.K2 = i*np.array([
            [0,0,-1,0],
            [0,0,0,0],
            [-1,0,0,0],
            [0,0,0,0]])
        S.K3 = i*np.array([
            [0,0,0,-1],
            [0,0,0,0],
            [0,0,0,0],
            [-1,0,0,0]])
        S.theta = np.array(theta)
        S.beta = np.array(beta)
        S.A = i*(S.theta[0]*S.J1+S.theta[1]*S.J2+\
                 S.theta[2]*S.J3)+i*(S.beta[0]*S.K1+\
                S.beta[1]*S.K2+S.beta[2]*S.K3)
        S.transform = expm(S.A)
    def __add__(S,q):
        theta = S.theta + q.theta
        beta = S.beta + q.beta
        q2 = LorenzGroup(theta,beta)
        return q2
    def __neg__(S):
        theta = -S.theta
        beta = -S.beta
        q2 = LorenzGroup(theta,beta)
        return q2
    def __sub__(S,q):
        q2 = S + (-q)
        return q2
    def __rmul__(S,x):
        theta = x*S.theta
        beta = x*S.beta
        q2 = LorenzGroup(theta,beta)
        return q2
    def __str__(S):
        s = '[%.4f,%.4f,%.4f],[%.4f,%.4f,%.4f]' % tuple(list(S.theta)+list(S.beta))
        return s
    
def slerp(q1,q2,t):
    """
    q = slerp(q1,q2,t) - spherical lerp two quaternions
    q1 and q2 blending them for t in interval [0,1].
    q1 = slerp(q1,q2,0) and q2 = slerp(q1,q2,1)
    creating a path from q1 to q2 parametrized by t.
    Thus q.rotation_matrix() is a path from the
    rotation of q1 to rotation of q2.
    """
    # use right scalar multiplication
    q = q1*(1-t)+q2*t
    return q

o13 = LorenzGroup # o(1,3)
