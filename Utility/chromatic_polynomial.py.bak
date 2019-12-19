"""
Recursive calculation of pi_k(G) using graph diagrams for
a cycle graph, graph.Cn(4) and star graph.Sk(3).

[1] Bondy and Murty, Graph Theory with Applications,
North-Holland, 1976

A Chromatic Polynomial for a graph can be obtained by
reducing the graph G to graph minors that are complete
graphs and counting the number of such, and for
a graph.Kn(4), graph.Kn(3), graph.Kn(2), graph.Kn(1),
etc, the chromatic polynomial is graph.Kn(n) is
k!/(k-n)! where k is the polynomial symbol, and
the coefficient is count of number of such complete
graphs. Eg, three triangles is 3*(k!/(k-3)!) and
two edges is 2*(k!/(k-2)!) so together you add
terms. We use the graph.py and sympy libraries.
We use P(n,k) to represent the number of permutations
of n items with k elements. Above is then 3*P(k,3)
+ 2*P(k,2) for example.
"""
from sympy import Symbol
import graph
from copy import deepcopy
from collections import Counter

k = Symbol('k')
def P(n,k):
    pi = 1
    for i in range(k):
        pi = pi*(n-i)
    return pi

#https://docs.python.org/2/library/collections.html#collections.Counter
def ChromaticPolynomialGraphs(doc):
    """
    Obtains the Graphs at the end of a derivation of
    the Chromatic Polynomial in the recursive calculation
    of pi_k(G).
    """
    n = len(doc["V"])
    L = [str((n,doc["E"]))]
    R = Counter([])
    while len(L) > 0:
        tup = L[0]
        L = L[1:]
        tup = eval(tup)
        n,E = tup
        doc1 = {}
        doc1["V"] = range(n)
        doc1["E"] = E
        GC = graph.LexOrder(graph.Complement(doc1))
        if len(GC["E"]) > 0:
            e = GC["E"][0]
            u,v=e
            doc1["E"].append([u,v])
            doc1["E"].append([v,u])
            doc1 = graph.LexOrder(doc1)
            n1 = len(doc1["V"])
            doc2 = graph.ContractEdge(doc1,e)
            doc2 = graph.LexOrder(doc2)
            n2 = len(doc2["V"])
            T = [str((n1,doc1["E"])),str((n2,doc2["E"]))]
            L = L + T
        else:
            R = R + Counter([str(tup)])
    return R

def ChromaticPolynomial(G):
    """
    ChromaticPolynomial(G) - obtains the graphs by adding
    an edge to Complement(G) as doc1 and contracting that
    edge as doc2. Then recursive it repeats until it obtains
    just complete graphs. It counts the number, a_n, of each
    complete graph K_n and forms a polynomial with a_n
    as coefficient of P(k,n) = k*(k-1)*(k-2)*...*(k-n+1)
    the number of permutations of k elements with n subsets.
    The polynomial is in k over the integers, as polynomial
    ring ZZ[k]. That is, this is the same as polynomials
    using symbol x, with ZZ[x] denoting coefficients that
    are integers (ZZ) of powers of x**i, except the convention
    here is to use ZZ[k] with k = Symbol(k). For computing
    the algebra, by simplifying and factoring, the Python
    sympy library was used.
    """
    S = ChromaticPolynomialGraphs(G)
    p = 0
    k = Symbol('k')
    for key in S.keys():
        n = eval(key)[0]
        an = S[key]
        p += an*P(k,n)
    p = p.expand().factor()
    return p

