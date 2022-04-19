from functools import reduce
from copy import deepcopy

import random
seed = 1231234
random.seed(seed)

def apply_rule(s,LHS,RHS):
    L = s.split(LHS)
    s2 = RHS
    s3 = s2.join(L)
    return s3

def r(s):
    s2 = apply_rule(s,"A","B-[A-B]\n")
    s3 = apply_rule(s2,"B","A+[B-A]\n")
    return s3

def S(i):
    def f(s):
        val = reduce(lambda n,m: r(n), range(i), s)
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

def r2(s):
    #s2 = apply_rule2(s,"A","Aa",.9)
    #s3 = apply_rule2(s2,"A",".",.1)
    s2 = apply_rule2(s,"A","ABA",.6)
    s3 = apply_rule2(s2,"B","BB",.2)
    s4 = apply_rule2(s3,"A","",.1)
    s5 = apply_rule2(s4,"B","",.2)
    return s3

def S2(i):
    def f(s):
        val = reduce(lambda n,m: r2(n), range(i), s)
        return val
    return f

def Display(N):
    start = "A"
    s = start
    for i in range(N):
        s2 = r2(s)
        t = 'i=%03d,\ns=\"\"\"\n%s\n\"\"\"' % (i,s2)
        print(t)
        s = s2
    return s 

N = 5
Display(N)
