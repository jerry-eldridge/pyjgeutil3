import my_reduce3 as myr
import numpy as np

#########################################
# [1] JGE

c = myr.c
v = myr.v
lst = myr.cons

def lookup(mem,var):
    tup = (var,types[var])
    value = mem[tup]
    if type(value) == type(()):
            value = f"{value[0]}:{value[1]}"
    return value

class sVars:
    def __init__(self,name):
        self.name = name
        self.x = []
    def create(self):
        n = len(self.x)
        tup = (f"$x{n}",v)
        self.x.append(tup)
        return tup
    def get(self,n):
        if n < len(self.n):
            return self.x[n]
        return None
    def __str__(self):
        return self.name
    def __repr__(self):
        return str(self)

def obj(name):
    return (name,c)

# this is a star graph or topology or network
# where center is (variable,type) and leaves of
# the star graph is a list of [...(variable,type)...].
# [1] https://en.wikipedia.org/wiki/Star_(graph_theory)
def Star(sv, center, leaves):
    k = len(leaves)
    x = []
    for i in range(k):
        xi = sv.create()
        x.append(xi)
    L = []
    for i in range(k):
        obj_i = leaves[i]
        xi = x[i]
        tup = (obj_i, xi)
        L.append(tup)
    for i in range(k):
        xi = x[i]
        tup = (xi,center)
        L.append(tup)
    return L

sv = sVars("Diagram")

# Hasse diagram (LHS -> RHS rules)

# convert cons list to string word
def cons_to_word(s):
    f0 = s.get_f()
    f1 = lambda a,b: str(a)+str(b)
    s.set_f(f1)
    value = s
    s.set_f(f0)
    return value

# ordinary string word to hasse graph. We try
# to compute this where cons is replaced by f.
# cons(word[0],cons(word[1],cons(...,
# cons(word[-1],NIL)...))))
class Alphabet:
    def __init__(self,s):
        self.s = s
    def __str__(self):
        return str(self.s)
    def __repr__(self):
        return str(self)

def word_to_hasse(sv,word,identity):
    if len(word) == 0:
        return []
    hasse = []
    z = ("z",v)

    k = len(word)
    
    y = []
    for i in range(k):
        yi = sv.create()
        y.append(yi)
    z = []
    for i in range(k):
        zi = sv.create()
        z.append(zi)
        
    L = list(word)
    # yi = identity
    yi = (identity,c)
    for i in range(k-1,-1,-1):
        # y[i] <- yi
        tup2 = (yi, y[i])
        hasse.append(tup2)
        xi = (Alphabet(L[i]),c)
        # z[i] <- (xi,y[i])
        tup3 = (xi, z[i])
        hasse.append(tup3)
        tup4 = (y[i], z[i])
        hasse.append(tup4)
        # yi = z[i]
        yi = z[i]
    # ("y",v) <- z[0]
    tup = (z[0],("y",v))
    hasse.append(tup)
    
    return hasse

hasse1 = word_to_hasse(sv,"apple",Alphabet(""))
#print(hasse1)

types1 = {}
for tup in hasse1:
    a,b = tup
    types1[a[0]] = a[1]
    types1[b[0]] = b[1]

# Run Dynamic Reduce

# assume a binary operation on the monoid M
# input two lists and output a list
def f(x,y):
    f0 = lambda x,y: "cons("+str(x)+","+str(y)+")"
    f0 = lambda x,y: str(x) + str(y)
    z = myr.cons(x,y,f0)
    return z

M1 = myr.Monoid(identity='NIL',\
        func = lambda x,y: f(x,y),
        domain_type = type(()))

mem1 = myr.dynamic_reduce(hasse1, types1, \
        M1.f, M1.id)

print("Dynamic Programming (Variable Values):")
for var in types1.keys():
    tup = (var,types1[var])
    # a is a (value,type) tuple
    a = mem1[tup]
    # value is of type myr.cons, type is type string
    value = a[0]
    # s is of type string
    s = str(value)
    s2 = s # s2 is type string
    print(f"mem<{var}> is {(s2,type(value))}")
        
#
###############################################
