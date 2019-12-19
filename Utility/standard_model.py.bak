import u1 as f1
import su2 as f2
import su3 as f3

u1 = f1.u1
su2 = f2.su2
su3 = f3.su3

# direct product of groups u1 x su2 x su3
class standard_model:
    def __init__(S,p):
        assert(len(p) == 3)
        S.p = p
        return
    def __add__(S,p):
        q = [u1(0),su2([0,0,0]),su3([0,0,0,0, 0,0,0,0])]
        q = standard_model(q)
        for i in range(3):
            q.p[i] = S.p[i] + p.p[i]
        return q
    def __neg__(S):
        q = [u1(0),su2([0,0,0]),su3([0,0,0,0, 0,0,0,0])]
        q = standard_model(q)
        for i in range(3):
            q.p[i] = -S.p[i]
        return q
    def __sub__(S,p):
        q = S + (-p)
        return q
    def __mul__(S,p):
        q = [u1(0),su2([0,0,0]),su3([0,0,0,0, 0,0,0,0])]
        q = standard_model(q)
        for i in range(3):
            q.p[i] = S.p[i] * p.p[i]
        return q
    def __str__(S):
        L = map(str,S.p)
        s2 = "("+",".join(L)+")"
        return s2

def bracket(p1,p2):
    p = p1*p2 -  p2*p1
    return p
