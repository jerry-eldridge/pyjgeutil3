"""
http:#en.wikipedia.org/wiki/A*_search_algorithm
"""
from math import sqrt

def neighbor_nodes(V,E,current):
    S = set([])
    for e in E:
        S.add(str(e))
    L = []
    for v in V:
        if (str([current,v]) in S) or (str([v,current]) in S):
            L.append(v)
    return L

def heuristic_cost_estimate(X,Y,start,goal):
    return sqrt((X[start]-X[goal])**2 + (Y[start]-Y[goal])**2)
    
def A_star(doc,start,goal):
    V = doc['V']
    E = doc['E']
    pts = doc['pts']
    X = map(lambda tup: tup[0], pts)
    Y = map(lambda tup: tup[1], pts)
    emptyset = set([])
    closedset = emptyset    # The set of nodes already evaluated.
    openset = set([start])    # The set of tentative nodes to be evaluated, initially containing the start node
    came_from = {}    # The map of navigated nodes.
    g_score = {}
    f_score = {}
    g_score[start] = 0    # Cost from start along best known path.
    # Estimated total cost from start to goal through y.
    f_score[start] = g_score[start] + heuristic_cost_estimate(X,Y,start, goal)

    while len(list(openset)) <> 0:
        L = list(openset)
        L = sorted(L, key=lambda node: f_score[node])
        current = L[0]
        if current == goal:
            path = reconstruct_path(came_from, goal)
            path.reverse()
            return path
        openset.remove(current)
        closedset.add(current)
        for neighbor in neighbor_nodes(V,E,current):
            if neighbor in closedset:
                continue
            tentative_g_score = g_score[current] + heuristic_cost_estimate(X,Y,current,neighbor)

            if (neighbor not in openset) or (tentative_g_score < g_score[neighbor]):
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g_score
                f_score[neighbor] = g_score[neighbor] + heuristic_cost_estimate(X,Y,neighbor, goal)
                if neighbor not in openset:
                    openset.add(neighbor)
 
    return []
 
def reconstruct_path(came_from,current):
    total_path = [current]
    while current in came_from:
        current = came_from[current]
        total_path.append(current)
    return total_path

