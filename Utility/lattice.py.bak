from all_monotonic_paths import *
from math import sqrt
from numpy import argmin, argmax, array

def cost1(i,j):
    if ([i,j] in E) or ([j,i] in E):
        return 1
    else:
        return 0

def MinOnTwoPaths(p1,p2):
    S1 = set(p1)
    S2 = set(p2)
    S = list(S1.intersection(S2))
    pts2 = []
    for idx in S:
        pts2.append(pts[idx])
    # get argmin for y-inverted coordinates
    K = argmax(array(pts2), axis=0)
    k = K[1]
    return S[k]

def MaxOnTwoPaths(p1,p2):
    S1 = set(p1)
    S2 = set(p2)
    S = list(S1.intersection(S2))
    pts2 = []
    for idx in S:
        pts2.append(pts[idx])
    # get argmax for y-inverted coordinates
    K = argmin(array(pts2), axis=0)
    k = K[1]
    return S[k] 

def join(i,j):
    # get argmax for y-inverted coordinates
    Top = argmin(array(pts), axis=0)
    Top = Top[1]
    paths_i = all_increasing_paths(i,Top)
    paths_j = all_increasing_paths(j,Top)
    val = Top
    for p1 in paths_i:
        for p2 in paths_j:
            sk = MinOnTwoPaths(p1,p2)
            if Less(sk,val):
                val = sk
    return val

def meet(i,j):
    # get argmin for y-inverted coordinates
    Bottom = argmax(array(pts), axis=0)
    Bottom = Bottom[1]
    paths_i = all_decreasing_paths(i,Bottom)
    paths_j = all_decreasing_paths(j,Bottom)
    val = Bottom
    for p1 in paths_i:
        for p2 in paths_j:
            sk = MaxOnTwoPaths(p1,p2)
            if Less(val,sk):
                val = sk
    return val

def Join(i,j):
    k = join(i,j)
    s = '%d \/ %d = join(%d,%d) = %d' % (i,j,i,j,k)
    print s
    return k

def Meet(i,j):
    k = meet(i,j)
    s = '%d /\ %d = meet(%d,%d) = %d' % (i,j,i,j,k)
    print s
    return k

def Infimum(L): # inf(L)
    m = len(L)
    Top = argmin(array(pts), axis=0)
    Top = Top[1]
    val = Top
    for i in L:
        val = meet(val,i)
    return val

def Supremum(L): # sup(L)
    m = len(L)
    Bottom = argmax(array(pts), axis=0)
    Bottom = Bottom[1]
    val = Bottom
    for i in L:
        val = join(val,i)
    return val    

