import numpy as np

# Gram-Schmidt Process wikipedia article
# https://en.wikipedia.org/wiki/Gram%E2%80%93Schmidt_process
dot = lambda A,B: np.inner(A,B)

def proj(u):
    def f(v):
        return (1.0*dot(v,u)/dot(u,u))*u
    return f

def norm(u):
    return np.linalg.norm(u)

def GramSchmidtProcess(v):
    """
    Produces an orthonormal basis from basis v in R**n
    """
    v = map(lambda vi: np.array(vi),v)
    a = norm(v[0])
    u = [1.0*v[0]/a]
    n = len(v)
    for k in range(1,n):
        uk = v[k]
        for j in range(k):
            uk = uk-proj(u[j])(v[k])
        a = norm(uk)
        uk = 1.0*uk/a
        u.append(uk)
    u = map(list,u)
    return u


