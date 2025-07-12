import sympy as sp
import numpy as np
from sympy.combinatorics import Permutation as perm
from copy import deepcopy
from collections import Counter

def convolve(x,y):
    n1 = len(x)
    n2 = len(y)
    L = []
    if n1 > n2:
        for n in range(n1):
            for m in range(n2):
                L.append(x[n-m]*y[m])
    else:
        for n in range(n2):
            for m in range(n1):
                L.append(x[m]*y[n-m])
    return L

class WedgeProductTerm:
    def __init__(self, expr, L, n, names=None):
        self.n = n
        self.L = L
        self.expr = expr
        if names is None:
            names = [str(i) for i in range(self.n)]
        self.names = names
        assert(self.n == len(self.names))
    def hodge_star(self):
        x = self.reduce()
        L = x.L
        Ls = list(set(list(range(x.n)))-set(L))
        Ls.sort()
        return WedgeProductTerm(x.expr,Ls,x.n,x.names)
        
    def reduce(self):
        L2 = deepcopy(self.L)
        L3 = deepcopy(list(set(self.L)))
        L2.sort()
        L3.sort()
        if L2 != L3:
            L = []
            return WedgeProductTerm(0,L,
                        self.n,self.names)
        else:
            n = self.n
            L = L2
            I = deepcopy(self.L)
            pi = list(range(n))
            c = 0
            for i in range(n):
                if i not in I:
                    continue
                else:
                    pi[i] = I[c]
                    c = c + 1
            pi = perm(pi)
            s = pi.signature()
            expr = s*self.expr
            return WedgeProductTerm(expr,L,
                        n,self.names)
        return self
    def __mul__(self, y):
        assert(self.n == y.n)
        assert(self.names == y.names)
        expr = self.expr * y.expr
        xx = self.reduce()
        yy = y.reduce()
        L = xx.L + yy.L
        n = self.n
        return WedgeProductTerm(expr,L,n,self.names)
    def form_part(self):
        L = [self.names[self.L[i]] \
                 for i in range(len(self.L))]
        t = ' w '.join(L)
        return t
    def coeff_part(self):
        return self.expr
    def __str__(self):
        t = self.form_part()
        s = f"({self.coeff_part()})*({t})"
        return s
    def __repr__(self):
        return str(self)

class Form:
    def __init__(self,L,n,names=None):
        self.L = L
        self.n = n
        if names is None:
            names = [str(i) for i in range(self.n)]
        self.names = names
    def reduce(self):
        self.L = [self.L[i].reduce() for i in range(len(self.L))]
        self.L.sort(key=lambda x: x.form_part())
        S = [self.L[i].form_part() for i in range(len(self.L))]
        C = [self.L[i].coeff_part() for i in range(len(self.L))]
        S2 = list(set(S))
        S2.sort()
        d = {}
        d2 = {}
        for i in range(len(self.L)):
            key = S[i]
            coeff = C[i]
            d2[key] = self.L[i]
            if key in d.keys():
                d[key] = d[key] + coeff
            else:
                d[key] = coeff
        L = []
        K = list(d2.keys())
        K.sort()
        for i in range(len(K)):
            key = K[i]
            term = d2[key]
            n2 = term.n
            L2 = term.L
            expr2 = d[key]
            if expr2 == 0:
                continue
            names2 = term.names
            L.append(WedgeProductTerm(expr2,L2,n2,names2))
        if len(L) == 0:
            L = [WedgeProductTerm(0,[],self.n,self.names)]
        return Form(L,self.n,self.names)
    def __add__(self, y):
        if type(y) == Form:
            L = self.L + y.L
            n = self.n
            names = self.names
            return Form(L,n,names).reduce()
        if type(y) == WedgeProductTerm:
            L = self.L + [y]
            n = self.n
            names = self.names
            return Form(L,n,names).reduce()
    def __mul__(self, y):
        if type(y) == Form:
            L = convolve(self.L , y.L)
            n = self.n
            names = self.names
            return Form(L,n,names).reduce()
        if type(y) == WedgeProductTerm:
            L = convolve(self.L , [y])
            n = self.n
            names = self.names
            return Form(L,n,names).reduce()
        L = [WedgeProductTerm(self.L[i].expr*y,
                self.L[i].L,
                self.n,
                self.names) for i in range(len(self.L))]
        return Form(L,self.n,self.names).reduce()
        
    def __str__(self):
        s = ' + '.join(list(map(str,self.L)))
        return s
    def __repr__(self):
        return str(self)

######################################################
# [1] Microsoft Copilot, a large language model
# (Note these functions were defined with Copilot
# provided my existing code)
#
# exterior derivative
def exterior_derivative(form):
    terms = []
    for term in form.L:
        for i in range(term.n):
            var_name = term.names[i]
            dx_i = WedgeProductTerm(1, [i], \
                        term.n, term.names)
            d_expr = sp.diff(term.expr, var_name[1:])
            new_term = WedgeProductTerm(d_expr, \
                term.L + [i], term.n, term.names).reduce()
            terms.append(new_term)
    return Form(terms, form.n, form.names).reduce()

d = exterior_derivative

# curvature(A) = d(A) + A /\ A
def curvature(A):
    dA = exterior_derivative(A)
    return (dA + A * A).reduce()

#
################################################

# The hodge star "*form".
def hodge_star(form):
    form2 = form.reduce()
    L = form2.L
    n = form2.n
    names = form2.names
    Ls = [form2.L[i].hodge_star() for i in \
          range(len(form2.L))]
    return Form(Ls, n, names).reduce()

star = hodge_star

var_names = sp.symbols('t,x,y,z')
t,x,y,z = var_names
wpt = WedgeProductTerm

n0 = 4
names0 = ["d"+str(var_names[i]) \
          for i in range(len(var_names))]
phi = 2 # sp.Function('phi')(t,x,y,z)
Ax = y # sp.Function('Ax')(t,x,y,z)
Ay = z # sp.Function('Ay')(t,x,y,z)
Az = x # sp.Function('Az')(t,x,y,z)

A0 = wpt(phi,[0],n0,names0)
A1 = wpt(Ax,[1],n0,names0)
A2 = wpt(Ay,[2],n0,names0)
A3 = wpt(Az,[3],n0,names0)
A = Form([A0,A1,A2,A3],n=n0,names=names0)
#print(f"A (potential) = {A.reduce()}")
F = d(A)
#print(f"F (field strength) = {F.reduce()}")

A0, A1, A2, A3 = [sp.Function(f'A{i}')(t,x,y,z) \
                  for i in range(4)]
A0 = 1
A1 = 0
A2 = x**2*y/2+-y*t
A3 = -y+x**2*z/2

A_form = Form([
    wpt(A0, [0], n0, names0),
    wpt(A1, [1], n0, names0),
    wpt(A2, [2], n0, names0),
    wpt(A3, [3], n0, names0)
], n=n0, names=names0)

F_2 = exterior_derivative(A_form)
# Compare F_guess with your known F and solve for A_i
dF2 = d(F_2)

print(f"F = E_x*dt w dx + E_y*dt w dy + E_z*dt w dz "+\
      "+ B_x*dy w dz + B_y*dz w dx + B_z*dx w dy")
E_x = 0
E_y = y
E_z = 0
B_x = 1
B_y = z*x
B_z = -y*x
F0 = wpt(E_x, [0], n0, names0)
F1 = wpt(E_y, [0,2], n0, names0)
F2 = wpt(E_z, [0,3], n0, names0)
F3 = wpt(B_x, [2,3], n0, names0)
F4 = wpt(B_y, [3,1], n0, names0)
F5 = wpt(B_z, [1,2], n0, names0)
F = Form([F0,F1,F2,F3,F4,F5],n=n0,names=names0)
dF = d(F)
starF = star(F)
d_starF = d(starF)
kappa = curvature(A)
print(f"kappa = curvature(A) = {kappa}")
print(f"F (field strength) = {F.reduce()}")
print(f"F_2 = {F_2}")
print(f"d(F) (should vanish) = {dF.reduce()} == 0")
print(f"d(F_2) (should vanish) = {dF.reduce()} == 0")
print(f"*F (Hodge dual) = {starF.reduce()}")
print(f"d(*F) (inhomogeneous equation) = "+\
      f"{d_starF.reduce()} == J")
L = (F * star(F))*(-1/2)
print(f"L (lagrangian) = {L}")
