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

# A rule is a list (LHS,RHS,p) where
# LHS -> RHS with probability p.
start1 = "S"
rules1 = [
    ("S","[DxDxDx]",.9),
    ("D","[EyEyEy]",.9),
    ("E","[FzFzFz]",.9),
    ("F","aca",.9),
    ("[","<(",1),
    ("]",")>",1)
    ]

start2 = "S"
rules2 = [
    ("S","o[HHH]",1),
    ("H","FoG",1),
    ("G","zFxx",1),
    ("F","[DDDDD]",.9),
    ("D","Exyz",.9),
    ("E","aca",.9),
    ("[","<(",1),
    ("]",")>",1)
    ]

start3 = "D"
rules3 = [
    ("D","N",1),
    ("N","[E]O",1),
    ("O","ffffff",1),
    ("E","XZF",1),
    ("F","XZG",1),
    ("G","XZH",1),
    ("H","XZIX", 1),
    ("I","YJ",1),
    ("J","XWK",1),
    ("K","XWL",1),
    ("L","XWM",1),
    ("M","XW", 1),
    ("X","aaaa",1),
    ("Y","yyyy",1),
    ("Z","zzzz",1),
    ("W","xxxx",1),
    ("[","<(",1),
    ("]",")>",1)
    ]

start4 = "S"
rules4 = [
    ("S","[CC]",1),
    ("C","BBBB",1),
    ("B","aO",1),
    ("O","xGy",1),
    ("G","FFFF",1),
    ("F","ffff",1)

    ]  

s1 = "[*a*f**8*x**4*]"
s2 = "x**3*y**2*f**2*a**3"
s3 = "[*a*x*f**16*y*a*x*f**16*]"
s4 = "af**3*a*a*f**3*a"
s6 = less_rapid_growth(3,rules4)(start4)
s7 = dec(enc2(s6))

ob = 'a'
fly = Verb(s7,ob)

bob = "xfyfzffc"
ball = "M"

for v_s in [s1,s2,s3,s4,s6]:
    print("v: ", v_s)
    print("E(v): ", E(v_s))
    S = Sentence(s=bob,v=v_s,o=ball,verbose=True)
    print("S =", str(S))
    print("="*30)
print()
print()
for v_s in [s1,s2,s3,s4,s6]:
    print("v: ", v_s)
    print("E(v): ", E(v_s))
    S = Sentence(s=bob,v=v_s,o=ball,verbose=False)
    print("S =", str(S))
    print("="*30)
