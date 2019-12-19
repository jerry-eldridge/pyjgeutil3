import graph
import stack
import queue

def AllPaths(G,start,goal,nedges):
    depth = nedges+2
    path = [start]
    S = stack.Stack()
    S.Push(path)
    paths = []
    while not S.Empty():
        if len(path) == depth:
            break
        path = S.Pop()
        if (path[-1]==goal) and (path[0]==start):
            if path not in paths:
                paths.append(path)
        u = path[-1]
        adj = graph.OutAdj(G,u)
        for v in adj:
            path2 = path+[v]
            S.Push(path2)
    return paths
