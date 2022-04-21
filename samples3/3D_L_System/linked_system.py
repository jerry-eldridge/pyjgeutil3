import affine as aff

import numpy as np
from copy import deepcopy

from functools import reduce

from math import cos,sin,pi,fmod

import random

seed = 123123123
random.seed(seed)

# works with compressed string like above's s1
def enc(s1):
    s2 = s1.replace('**',':')
    L = list(map(lambda s: tuple(s.split(':')),s2.split('*')))
    for i in range(len(L)):
        tup = L[i]
        if len(tup) == 1:
            L[i] = (tup[0],1)
    L2 = list(map(lambda tup: (tup[0],int(tup[1])), L))
    return L2

def dec2(L):
    s1 = ''
    for tup in L:
        val = tup[0]*tup[1]
        s1 = s1 + val
    return s1

def enc2(s):
    s2 = ''
    if len(s) < 1:
        return s
    tup0 = (s[0],1)
    L = []
    for i in range(1,len(s)):
        a = s[i-1]
        b = s[i]
        if a == b:
            tup = (tup0[0],tup0[1]+1)
        else:
            tup = (b,1)
            L.append(tup0)
        tup0 = tup
    L.append(tup0)
    return L

def dec(L):
    s1 = ''
    for tup in L:
        if tup[1] == 0:
            continue
        elif tup[1] == 1:
            s1 = s1 + '*' + str(tup[0])
        else:
            val = tup[0] + '**' + str(tup[1])
            s1 = s1 + '*' + val
    if len(s1) > 0:
        s1 = s1[1:]
    return s1

def E(s):
    L = enc(s)
    s2 = dec2(L)
    return s2

from functools import reduce

from math import cos,sin,pi,fmod

import random

seed = 123123123
random.seed(seed)

# [1] https://en.wikipedia.org/wiki/L-system
def apply_rule(s,LHS,RHS):
    L = s.split(LHS)
    s2 = RHS
    s3 = s2.join(L)
    return s3

def r(s,rules):
    for rule in rules:
        LHS,RHS, p = rule
        s2 = apply_rule(s,LHS,RHS)
        s = s2
    return s

def extremely_rapid_growth(i,rules):
    def f(s):
        val = reduce(lambda n,m: r(n,rules),
                    range(i), s)
        return val
    return f

def apply_rule2(s,LHS,RHS,p):
    L = s.split(LHS)
    s2 = RHS
    s3 = ''
    flag = False
    for i in range(len(L)-1):
        x = L[i]
        y = RHS
        px = random.uniform(0,1)
        if px <= p:
            s3 = s3 + x + y
            flag = True
        else:
            s3 = s3 + x + LHS
            flag = False
    z = L[-1]
    if flag:
        s3 = s3 + z
    else:
        s3 = s3 + z
    return s3

def r2(s,rules):
    for rule in rules:
        LHS,RHS, p = rule
        s2 = apply_rule2(s,LHS,RHS,p)
        s = s2
    return s

def less_rapid_growth(N,rules):
    def f(t):
        s = t
        for i in range(N):
            s2 = r2(s,rules)
            s = s2
        return s
    return f

def SVO(s,v,o):
    s2 = s + v(o)
    return s2

def Display(s):
    print("s = \"%s\"" % s)
    s2 = E(s)
    print("s2 = \"%s\"" % s2)
    print("="*30)
    return

def get_action(s,o, verbose=False):
    L = s.split(o)
    if verbose:
        f = lambda o: "<VERB txt=\""+o.join(L)+"\" /VERB>"
    else:
        f = lambda o: o.join(L)
    return f


def Verb(s,ob,verbose=False):
    f = get_action(E(s),ob,verbose)
    return f

class Sentence:
    def __init__(self, s,v,o,verbose=False):
        if verbose:
            self.s = "<SUBJECT/>"
            self.o = "<OBJECT/>"
            self.vv = v
            self.v = Verb(E(self.vv),'a',verbose=True)
        else:
            self.s = s
            self.o = o
            self.vv = v
            self.v = Verb(E(self.vv),'a',verbose=False)
        self.snt = SVO(s=self.s,v=self.v, o=self.o)
        return
    def set_s(self,s2):
        self.s = s2
        self.snt = SVO(s=self.s,v=self.v, o=self.o)
        return
    def set_o(self,o2):
        self.o = o2
        self.snt = SVO(s=self.s,v=self.v, o=self.o)
        return
    def set_vv(self,vv2):
        self.vv = vv2
        self.v = Verb(E(self.vv),'a',verbose=False)
        self.snt = SVO(s=self.s,v=self.v, o=self.o)
        return
    def __str__(self):
        s = self.snt
        return s

def draw(s, t, q, flag=False):
    S1 = []
    S2 = []
    pos = deepcopy(t)
    if flag:
        N0 = 16
    else:
        N0 = 8
    angle = 360./N0
    heading = 0
    r = 50
    pos_curve = []
    q_curve = []
    for i in range(len(s)):
        pos_curve.append(pos)
        q_curve.append(str(q))
        c = s[i]
        if c in ["a","b"]:
            r2 = 35
            O = [r2,0,0]
            pts1 = aff.Rotate([O],q,align=False)
            pts2 = aff.Translate(pts1,*pos,align=False)
            B = pts2[0]
            pos = deepcopy(B)
        if c in ["c"]:
            r2 = 35
            O = [r2,0,0]
            pts1 = aff.Rotate([O],q,align=False)
            pts2 = aff.Translate(pts1,*pos,align=False)
            B = pts2[0]
            pos = deepcopy(B)
        elif c == 'z':
            axis1 = [0,0,1]
            heading = fmod(heading + angle, 360)
            if flag:
                degrees = angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == 'k':
            axis1 = [0,0,1]
            heading = fmod(heading - angle, 360)
            if flag:
                degrees = -angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == 'y':
            axis1 = [0,1,0]
            heading = fmod(heading + angle, 360)
            if flag:
                degrees = angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == 'j':
            axis1 = [0,1,0]
            heading = fmod(heading - angle, 360)
            if flag:
                degrees = -angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == 'x':
            axis1 = [1,0,0]
            heading = fmod(heading + angle, 360)
            if flag:
                degrees = angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == 'i':
            axis1 = [1,0,0]
            heading = fmod(heading - angle, 360)
            if flag:
                degrees = -angle
            else:
                degrees = heading
            qi = aff.HH.rotation_quaternion(degrees,
                    axis1[0],axis1[1],axis1[2])
            if flag:
                q = qi*q
            else:
                q = qi
        elif c == '<':
            S1.append(pos)
        elif c == '>':
            val = S1[-1]
            S1 = S1[:-1]
            pt = val
            pos = deepcopy(pt)
        elif c == 'o':
            O = [0,0,0]
            pos = deepcopy(O)
        elif c == 'r':
            q = aff.HH.rotation_quaternion(0,
                axis[0],axis[1],axis[2])
        elif c == '(':
            S2.append(q)
        elif c == ')':
            val = S2[-1]
            S2 = S2[:-1]
            qq = val
            q = qq
        elif c == 'f':
            r2 = 35
            O = [r2,0,0]
            pts1 = aff.Rotate([O],q,align=False)
            pts2 = aff.Translate(pts1,*pos,align=False)
            B = pts2[0]
            pos = deepcopy(B)
        elif c == 'b':
            r2 = 35
            O = [-r2,0,0]
            pts1 = aff.Rotate([O],q,align=False)
            pts2 = aff.Translate(pts1,*pos,align=False)
            B = pts2[0]
            pos = deepcopy(B) 
        else:
            continue
    pos_curve.append(pos)
    q_curve.append(str(q))
    return deepcopy(pos),q,pos_curve,q_curve

def Shape0(s,flag=True):
    #print("|s| = ",len(s))
    #print("s = \"%s\"" % s)

    t0 = [0,0,0]
    axis0 = [0,0,1]
    q0 = aff.HH.rotation_quaternion(0,
        axis0[0],axis0[1],axis0[2])

    ## gradual growth
    #s = less_rapid_growth(2,rules)(start)
    t2,q2,pos_curve2,q_curve2 = draw(s,t0,q0,flag)
    return t2,q2,pos_curve2,q_curve2

def Shape1(t,q,s=[1,1,1]):
    global t0,q0
    t2 = list(np.array(t0)+np.array(t))
    q2 = q*q0
    s2 = deepcopy(s)
    return t2,q2,s2

# shapes are vertices and joint_angles are
# edges between those vertices, but they form
# a path graph.
def PathSystem(shapes,joint_angles):
    assert(len(shapes) == 1+len(joint_angles))
    s = ""
    for i in range(len(joint_angles)):
        v1 = shapes[i]
        nx,ny,nz = joint_angles[i]
        if nx >= 0:
            a = "x"
        else:
            a = "i"
            nx = -nx
        if ny >= 0:
            b = "y"
        else:
            b = "j"
            ny = -ny
        if nz >= 0:
            c = "z"
        else:
            c = "k"
            nz = -nz
        v2 = "%s**%d*%s**%d*%s**%d" % (c,nz,b,ny,a,nx)
        v = v1 + "*" + v2
        s = s + "*" + v
    s = s + "*" + shapes[-1]
    s2 = E(s)
    if len(s2) < 1:
        s2 = s2[1:]
    return s2
