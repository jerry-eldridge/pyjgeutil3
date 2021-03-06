from scipy.spatial import KDTree

def MergePoints(pts,epsilon=1e-2):
    kdtree = KDTree(pts)
    L = list(range(len(pts)))
    for pt in [pts[k] for k in L]:
        ball = kdtree.query_ball_point(pt,epsilon)
        if len(ball) > 1:
            ball = ball[1:]
            for k in ball:
                try:
                    L.remove(k)
                except:
                    continue
    return [[pts[k] for k in L],L]

pts = [[2,3],[2,3.2],[3,3],[3,2.9]]

print(MergePoints(pts,epsilon=0.01))
print(MergePoints(pts,epsilon=0.3))
print(MergePoints(pts,epsilon=1.3))
