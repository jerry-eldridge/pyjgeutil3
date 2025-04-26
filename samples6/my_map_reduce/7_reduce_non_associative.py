import my_reduce3 as myr
import numpy as np

#########################################
# [1] JGE

c = myr.c
v = myr.v

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

##hasse = [
##    (('2', c), ("x", v)),
##    (('4', c), ("x", v)),
##    (("5", c), ("x", v)),
##    (("y", v), ("x", v)),
##    (("4", c), ("y", v)),
##    (("x", v), ("z", v)),
##    (('y', v), ("z", v))
##    ]

# these are 3D vectors
c_1 = [1,2,3]
c_2 = [2,1,3]
c_3 = [2,3,1]
hasse = [
    *Star(sv, ("x",v),
          [(str(c_1),c), (str(c_2),c),\
           (str(c_3),c),("y",v)]),
    *Star(sv, ("y",v),
          [(str(c_2),c)]),
    *Star(sv, ("z",v),
          [("x",v), ("y",v)]),
]

##hasse = [ *Star(sv, ("S1",v), [("A",c), ("B",c),("E",c)]), *Star(sv,
##    ("S2",v), [("C",c), ("D",c)]), *Star(sv, ("S3",v), [("S1",v),
##    ("S2",v)]), ]

types = {}
for tup in hasse:
    a,b = tup
    types[a[0]] = a[1]
    types[b[0]] = b[1]

# Run Dynamic Reduce

# assume a binary operation on the monoid M
def f(x,y):
    a = np.array(x)
    b = np.array(y)
    cc = np.cross(a,b)
    z = list(map(float,list(cc)))
    return z

M = myr.Monoid(identity='NIL',\
        func = lambda x,y: \
            f(eval(str(x)),eval(str(y))),\
        domain_type = type(()))

mem = myr.dynamic_reduce(hasse, types, \
        M.f, M.id)
print("Dynamic Programming (Variable Values):")
for var in types.keys():
    tup = (var,types[var])
    a = mem[tup]
    if a[1] == c:
        L = eval(str(a[0]))
        value = (str(np.array(L)),c)
        s = f"{value[0]}:{value[1]}"
        print(f"mem<{var}> is {s}")


print(f"The manual way to compute result:")
y = c_2 # this is an input constant
print(f"y = {y}")
# 'cons' are converted into 'f'.
x = f(c_1,f(c_2,f(c_3,y)))
print(f"x = {x}")
z = f(x,y) # cons(x,y) converted to f(x,y)
print(f"z = {z}")

#
###############################################
