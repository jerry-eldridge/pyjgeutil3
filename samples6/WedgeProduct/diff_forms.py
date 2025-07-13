import sympy as sp
import numpy as np
from sympy.combinatorics import Permutation as perm
from copy import deepcopy
from collections import Counter
from functools import reduce

# [1] Microsoft Copilot, a large language model

# [2] book{Lee12,
# author = "Lee, John",
# title = "Introduction to Smooth Manifolds
# (Graduate Texts in Mathematics, Vol 218)",
# publisher = "Springer",
# year = "2012"
# }

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
    def deg(self):
        L2 = deepcopy(self.L)
        L3 = deepcopy(list(set(self.L)))
        L2.sort()
        L3.sort()
        if L2 != L3:
            return 0
        else:
            I = deepcopy(self.L)
            pi = list(range(self.n))
            c = 0
            for i in range(self.n):
                if i not in I:
                    continue
                else:
                    pi[i] = I[c]
                    c = c + 1
            pi = perm(pi)
            s = pi.signature()
            return s
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
            s = self.deg()
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

def exterior_derivative(form):
    form = form.reduce()
    terms = []
    for term in form.L:
        # graded Leibniz rule
        # d(f*omega) = d(f) w omega + f w d(omega)
        # = d(f) w omega (since omega is just a
        # wedge product of basis vectors.
        f = term.expr
        df = Form([WedgeProductTerm(\
            sp.diff(f,term.names[i][1:]),[i],\
            term.n, term.names) \
            for i in range(term.n)],
            term.n, term.names)
        omega = Form([WedgeProductTerm(1, term.L, \
            term.n,term.names)],
            term.n, term.names)
        term2 = df * omega
        terms.append(term2)
    s = terms[0]
    for term in terms[1:]:
        s = s + term
    s = s.reduce()
    return s

d = exterior_derivative

# curvature(A) = d(A) + A /\ A
def curvature(A):
    dA = exterior_derivative(A)
    return (dA + A * A).reduce()

# The hodge star "*form".
def hodge_star(form):
    form2 = form.reduce()
    L = form2.L
    n = form2.n
    names = form2.names
    Ls = [form2.L[i].hodge_star() for i in \
          range(len(form2.L))]
    return Form(Ls, n, names).reduce()

# hodge star
star = hodge_star

# codifferential
# https://en.wikipedia.org/wiki/Hodge_star_operator#Codifferential
delta = lambda A: star(d(star(A)))

# Laplace-de Rham operator
# https://en.wikipedia.org/wiki/Laplace%E2%80%93Beltrami_operator
# (Laplace-Beltrami operator), see Laplace-de Rham operator
hodge_dirac = lambda A: d(A) + delta(A)
Delta = lambda A: hodge_dirac(hodge_dirac(A))

# inner g
# https://en.wikipedia.org/wiki/Hodge_star_operator
inner_k =lambda a,b: a * star(b)
g_k = inner_k

# F_map : M -> N, omega is differential form on N
# and names0 is the names on N. See [2]. 
def pullback(F_map,names_M,names_N):
    v_M = sp.symbols(','.join(names_M))
    v_N = sp.symbols(','.join(names_N))
    def f(omega):
        L = omega.L
        n = omega.n
        names=omega.names
        M2 = []
        L_F = F_map(*v_M)
        print(f"F_map({','.join(names_M)}) = "+\
              f"({','.join(list(map(str,L_F)))})")
        for term in L:
            expr2 = term.expr
            L2 = term.L
            for k in range(len(v_N)):
                expr2 = expr2.replace(v_N[k],\
                            L_F[k]).expand()
            #print(f"expr2 = {expr2}")
            L3 = [L_F[i] for i in L2]
            names1 = ["d"+names_N[i] \
                      for i in range(len(names_N))]
            names2 = ["d"+names_M[i] \
                      for i in range(len(names_M))]
            L4 = [d(Form([WedgeProductTerm(\
                L_F[i],[],len(names2),names2)], \
                len(names2),names2))
                for i in L2]
            one = Form([WedgeProductTerm(1,[],\
                    len(names2),names2)],len(names2),\
                    names2)
            expr3 = reduce(lambda s,v: s*v,L4,one)
            #print(expr3,'e3')
            expr4 = Form([WedgeProductTerm(\
                expr2,[],len(names2),names2)],\
                len(names2),names2)
            #print(expr4,'e4')
            expr5 = expr4 * expr3
            M2.append(expr5)
        expr6 = M2[0]
        for x in M2[1:]:
            expr6 = expr6 + x
        return expr6
    return f

