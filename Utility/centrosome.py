import numpy as np
import collections as c

from math import fmod,floor,ceil

def lerp(A,B,t):
    C = list(np.array(A)*(1-t) + np.array(B)*t)
    return C

# [1] https://en.wikipedia.org/wiki/Microtubule
# which is similar in functions to Actin
class Microtubule:
    def __init__(self,O=[0,0]):
        self.Q = c.deque()
        self.flag_minus = False
        self.flag_plus = False
        self.O = O
        return
    def push_minus(self,val):
        if not self.flag_minus:
            self.Q.appendleft(val)
        return
    def pop_minus(self):
        if not self.flag_minus:
            val = self.Q.popleft()
            return val
        return None
    def push_plus(self, val):
        if not self.flag_plus:
            self.Q.append(val)
        return
    def pop_plus(self):
        if not self.flag_plus:
            val = self.Q.pop()
            return val
        return None
    def __str__(self):
        return str(list(self.Q))
    def __repr__(self):
        L = list(self.Q)
        v = np.array(self.O)
        for i in range(len(L)):
            v = v + np.array(L[i])
        return str(v)
    def cap_minus(self):
        self.flag_minus = True
        return
    def uncap_minus(self):
        self.flag_minus = False
        return
    def cap_plus(self):
        self.flag_plus = True
        return
    def uncap_plus(self):
        self.flag_plus = False
    def curve(self,t):
        t2 = fmod(t,1) # map t to [0,1] by modulo 1
        L = list(self.Q)
        O = L[0]
        L2 = []
        for i in range(len(L)):
            vi = list(np.array(L[i]) - \
                      np.array(O) + \
                      np.array(self.O))
            L2.append(vi)
        n = len(L2)
        i1 = floor(t2*(n-1))
        i2 = ceil(t2*(n-1))
        # C = L[i1] would not be continous curve
        # create continuous (but its not smooth)
        # curve C
        A = L2[i1]
        B = L2[i2]
        t3 = fmod(t2*(n-1),1)
        C = lerp(A,B,t3)
        return C

# [2] https://en.wikipedia.org/wiki/Centrosome
class Centrosome:
    def __init__(self,O):
        self.B = [] # microtubule bundle
        self.O = O
        return
    def add_fiber(self,O):
        F = Microtubule(O)
        self.B.append(F)
        return
    def sub_fiber(self):
        if len(self.B) == 0:
            return
        F = self.B[0]
        self.B = self.B[1:]
        del F
        return

def DisplayFiber(C,i,dt=.1,tmin=0,tmax=1):
    assert(i in range(len(C.B)))
    F = C.B[i]
    t = tmin # should be in range [0,1]
    while t <= tmax:
        pt = F.curve(t)
        print(f"t = {t}, curve(t) = {pt}")
        t = t + dt
    print()
    return
