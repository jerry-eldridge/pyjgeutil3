#import sys
#sys.path.insert(0,r"C:\_PythonJGE\Utility")
import set_bits as sb
import random
from copy import deepcopy

random.seed()

def PowerSet(n,base=2):
    """
    Creates the powerset for range(n) using base=2 as
    the numerical base. That is, an element with base=2
    is either in the set or not. base=3 is three states,etc.
    """
    PV = []
    for k in range(base**n):
        v = sb.Base(k,base,n)
        PV.append(v)
    return PV

def TopoIndices(T,n):
    I = []
    for k in range(n+1):
        for i in T:
            L = sb.Indices(i,1)
            if len(L)==k:
                I.append(L)
    return I

def PrintPowerSet(T,n):
    I = TopoIndices(T,n)
    for S in I:
        print S
    return

def TopoAdd(T,v):
    k = sb.Number(v,2)
    T.append(k)
    return T

def Topology(bases,n):
    """
    Returns the topology given basis sets. All
    the sets (as lists) of returned document
    are from point set doc["V"] and open sets
    doc["E"]
    """
    E = deepcopy(bases)
    if [] not in E:
        E.append([])
    if range(n) not in E:
        E.append(range(n))
    T = []
    S = []
    base = 2
    N = 2**n
    PV = PowerSet(n,base) 
    S = []
    for e in E:
        v = [0]*n
        for i in e:
            v[i] = 1
        T.append(v)
        s = PV.index(v)
        S.append(s)

    for k in range(1000*N):
        j1 = random.randint(0,N-1)
        j2 = random.randint(0,N-1)
        v1 = PV[j1]
        v2 = PV[j2]
        if v1 not in T:
            continue
        if v2 not in T:
            continue
        v = sb.Meet(v1,v2)
        k = sb.Number(v,2)
        if k not in S:
            S.append(k)
        v = sb.Join(v1,v2)
        k = sb.Number(v,2)
        if k not in S:
            S.append(k)
        T = map(lambda i: PV[i], S)
    O = TopoIndices(T,n)
    X = range(n)
    doc1 = {}
    doc1["X"] = X
    doc1["O"] = O
    return doc1

def Complement(doc):
    doc1 = deepcopy(doc)
    n = len(doc1["X"])
    FF = []
    for O in doc1["O"]:
        F = list(set(range(n))-set(O))
        FF.append(F)
    doc1["O"]=FF
    return doc1

def closure(doc,S):
    """
    https://en.wikipedia.org/wiki/Closure_(topology)

    closure(S) = intersection of all closed sets
    containing S (denoted cl(S))
    """
    TT = Complement(doc)
    CL = set(TT["X"])
    for F in TT["O"]:
        if set(S) <= set(F):
            CL = CL & set(F)
    return list(CL)

def interior(doc,S):
    """
    https://en.wikipedia.org/wiki/Interior_(topology)

    interior(S) = union of all open sets containing S
    (denoted int(S))
    """
    INT = set([])
    for O in doc["O"]:
        if set(O) <= set(S):
            INT = INT | set(O)
    return list(INT)
    
def boundary(doc,S):
    """
    https://en.wikipedia.org/wiki/Boundary_(topology)
    """
    S1 = set(interior(doc,S))
    S2 = set(closure(doc,S))
    BDY = S2 - S1
    return list(BDY)

def TopologyConnected(T):
    import linearprogramming as lp
    MaxPacking = lp.SetPacking(T['X'],T['O'])
    S = set([])
    for Si in MaxPacking:
        S = S | set(Si)
    X = set(T['X'])
    if X == S:
        return False,MaxPacking
    else:
        return True,MaxPacking

def TopologyConnected2(T):
    c = 0
    for O1 in T['O']:
	for O2 in T['O']:
		if set(O1).union(set(O2))==set(T['X']) and \
                   set(O1).intersection(set(O2)) == set([]):
			c += 1
    return (c == 0)


