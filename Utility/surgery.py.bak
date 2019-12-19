import graph
import line_intersection
from copy import deepcopy
import generalized_cross_product
import vectors
import line_intersection
from numpy import array

def RemoveEdgesWithKnife(doc, Ax, Ay, Bx, By):
    """
    For a graph document in a 2D embedding in the plane
    with doc["V"], doc["E"] and doc["pts"] defined,
    remove edges of doc["E"] such that for edge
    e in doc["E"] and u,v = e, form

    Cx,Cy = doc["pts"][u][:2]
    Dx,Dy = doc["pts"][v][:2]

    and do

    flag,X,Y = line_intersection.SegmentIntersect(Ax,Ay,Bx,By,Cx,Cy,Dx,Dy)

    and if flag, then remove e. The knife is given
    by line segment AB with A = [Ax,Ay] and B = [Bx,By].
    """
    doc1 = deepcopy(doc)
    ES = []
    for e in doc["E"]:
        u,v = e
        Cx,Cy = doc["pts"][u][:2]
        Dx,Dy = doc["pts"][v][:2]
        flag,X,Y = line_intersection.SegmentIntersect(Ax,Ay,Bx,By,Cx,Cy,Dx,Dy)
        if not flag:
            ES.append(e)
    doc1["E"] = ES
    return doc1

def SliceWithKnife(doc, Ax, Ay, Bx, By, alpha=0.15,beta=0.15):
    """
    New points added at lerp t = alpha and t = beta
    with default alpha = 0.25 and beta = 0.25 if knife
    AB slices an edge.

    For a graph document doc in a 2D embedding in the plane,
    with doc["V"],doc["E"],doc["pts"] defined, slice
    the edges of doc with knife. The knife is given
    by line segment AB with A = [Ax,Ay] and B = [Bx,By].

    doc1 = deepcopy(doc)

    For e in doc1["E"] and u,v = e, 

    Cx,Cy = doc1["pts"][u][:2]
    Dx,Dy = doc1["pts"][v][:2]

    flag,X,Y = line_intersection.SegmentIntersect(Ax,Ay,Bx,By,Cx,Cy,Dx,Dy)

    then if flag, then break line segments into separated
    two segments and

    orient CD such that C is on interior of plane n*(x-mid) < 0
    # add Utility package folder with sys.path.insert(0, <utility_path>)
    AB = list(array([Ax,Ay]) - array([Bx,By]))
    epsilon = generalized_cross_product.Epsilon(2) # do once to get Cross   
    normal = epsilon_levicivita_TMP.Cross([AB])
    n = normal/vectors.norm(normal)
    mid = vectors.lerp([Cx,Cy],[Dx,Dy],0.5)
    xm = list(array(x) - array(mid))
    interior = vectors.dotprod(n,xm)
    if not interior:
        #swap Cx,Cy with Dx,Dy if not interior
        tx = Cx
        ty = Cy
        Cx = Dx
        Cy = Dy
        Dx = tx
        Dy = ty

    pt_1 = vectors.lerp([Cx,Cy,0],[Dx,Dy,0], alpha=0.25)
    pt_2 = vectors.lerp([Cx,Cy,0],[Dx,Dy,0], beta=0.75)
    
    doc1,u2 = graph.SplitVertex(doc1,u)
    doc1["pts"].append(pt_1) # assign pt_1 to u2
    doc1,v2 = graph.SplitVertex(doc1,v)
    doc1["pts"].append(pt_2) # assign pt_2 to v2

    and returns:
    
    doc1 = SliceWithKnife(doc, Ax, Ay, Bx, By) 
    """
    doc1 = deepcopy(doc)
    ES = []
    VS = []
    for e in doc1["E"]:
        u,v = e
        Cx,Cy = doc1["pts"][u][:2]
        Dx,Dy = doc1["pts"][v][:2]
        flag,X,Y = line_intersection.SegmentIntersect(Ax,Ay,Bx,By,Cx,Cy,Dx,Dy)
        if flag:
            AB = list(array([Ax,Ay]) - array([Bx,By]))
            normal = generalized_cross_product.cross2(array(AB))
            n = normal/vectors.norm(normal)+[0]
            mid = vectors.lerp([Cx,Cy,0],[Dx,Dy,0],0.5)
            # use x = [Cx,Cy] to check if on interior side
            xm = list(array([Cx,Cy,0]) - array(mid))
            interior = vectors.dotprod(n,xm)
            if not interior:
                #swap Cx,Cy with Dx,Dy if not interior
                tx = Cx
                ty = Cy
                Cx = Dx
                Cy = Dy
                Dx = tx
                Dy = ty
            pt_1 = vectors.lerp([X,Y,0],[Cx,Cy,0], alpha)
            pt_2 = vectors.lerp([X,Y,0],[Dx,Dy,0], beta)
            doc1,u2 = graph.SplitVertex(doc1,u)
            doc1["pts"].append(pt_1) # assign pt_1 to u2
            doc1,v2 = graph.SplitVertex(doc1,v)
            doc1["pts"].append(pt_2) # assign pt_2 to v2
            ES.append([u,u2])
            ES.append([v2,v])
            VS.append(u2)
            VS.append(v2)
        else:
            ES.append(e)
    doc1["E"] = ES
    doc1["V"] = doc["V"]+VS
    
    for k in range(len(doc1["pts"])):
        doc1["pts"][k] = map(int,map(round,doc1["pts"][k]))
    return doc1
