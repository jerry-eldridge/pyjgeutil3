from define_graph import *

def Adj(v):
    L = []
    for e in E:
        if e[0] == v:
            L.append(e[1])
        elif e[1] == v:
            L.append(e[0])
    return L

def Less(u,v):
    return pts[u][1] >= pts[v][1] # y-coordinates are inverted

def UpAdj(v):
    L = []
    for w in Adj(v):
        if Less(v,w):
            L.append(w)
    return L

def all_increasing_paths0(paths,b, a,paths0):
    pathsp = []
    for path in paths:
        v = path[-1]
        if v == b: continue
        for w in UpAdj(v):
            pathp = path + [w]
            pathsp = pathsp + [pathp]
            if pathp[0] == a and pathp[-1] == b:
                paths0.append(pathp)
        pathsp,paths0 = all_increasing_paths0(pathsp,b, a, paths0)
    return pathsp,paths0

def all_increasing_paths(a,b):
    return all_increasing_paths0([[a]],b, a,[])[1]

def DownAdj(v):
    L = []
    for w in Adj(v):
        if Less(w,v):
            L.append(w)
    return L

def all_decreasing_paths0(paths,b, a,paths0):
    pathsp = []
    for path in paths:
        v = path[-1]
        if v == b: continue
        for w in DownAdj(v):
            pathp = path + [w]
            pathsp = pathsp + [pathp]
            if pathp[0] == a and pathp[-1] == b:
                paths0.append(pathp)
        pathsp,paths0 = all_decreasing_paths0(pathsp,b, a, paths0)
    return pathsp,paths0

def all_decreasing_paths(a,b):
    return all_decreasing_paths0([[a]],b, a,[])[1]


