import my_reduce3 as myr

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

# a permutation on n elements uses symbols of
# integers from 0,1,2,...n-1. Thus these permutations
# are a shuffling of n = 5 elements.
pi_1 = [0,2,1,3,4]
pi_2 = [0,2,4,3,1]
pi_3 = [0,3,2,1,4]
hasse = [
    *Star(sv, ("x",v),
          [(str(pi_1),c), (str(pi_2),c),\
           (str(pi_3),c),("y",v)]),
    *Star(sv, ("y",v),
          [(str(pi_2),c)]),
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

# Identity Element: For summation, identity is 0
from sympy.combinatorics.permutations import Permutation
def f(x,y):
    a = Permutation(x)
    b = Permutation(y)
    cc = a*b
    z = list(cc)
    return z
M = myr.Monoid(identity='NIL',\
        func = lambda x,y: \
            f(eval(str(x)),eval(str(y))),\
        domain_type = type(()))

mem = myr.dynamic_reduce(hasse, types, \
        M.f, M.id)
print("Dynamic Programming (Variable Values):")
word = "abcde"
for var in types.keys():
    tup = (var,types[var])
    a = mem[tup]
    if a[1] == c:
        L = eval(str(a[0]))
        sigma = Permutation(L)
        word2 = ''.join(sigma(word))
        print(f"mem<{var}>('abcde') is {word2}")

#
###############################################
