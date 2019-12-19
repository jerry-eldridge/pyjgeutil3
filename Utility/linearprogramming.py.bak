import scipy.optimize

def SetCover(U,S):
    """
    Minimize: c^T*x
    Subject to: A_ub*x <= b_ub
    A_eq*x == b_eq
    (Use None for no bound in that direction)

    https://en.wikipedia.org/wiki/Linear_programming#Integer_unknowns

    res = scipy.optimize.linprog(c,A_ub=A_ub,b_ub=b_ub,
        bounds=bounds, options={"disp":True})
    print res

    https://en.wikipedia.org/wiki/Set_cover_problem
    U = [1,2,3,4,5]
    S = [[1,2,3],[2,4],[3,4],[4,5]]
    Si = S[i]
    Xi = 0 or 1 to include set
    Minimize: X0 + X1 + X2 + X3
    Subject to:
        X0 >= 1 # 1 in S0
        X0 + X1 >= 1 # 2  in S0 and S1
        X0 + X2 >= 1 # 3 in S0 and S2
        X1 + X2 + X3 >= 1 # 4 in S1,S2,S3
        X3 >= 1 # 5 in S3
        1 >= Xi >= 0 # really Xi in [0,1]

    https://en.wikipedia.org/wiki/Set_cover_problem
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
    """
    c = [1]*len(S)
    A_ub = []
    for u in U:
        row = []
        for Si in S:
            if u in Si:
                row.append(-1)
            else:
                row.append(0)
        A_ub.append(row)
    b_ub = [-1]*len(U)
    # None in bounds represents oo or -oo
    # bounds is a tuple of (a,b) where b >= xi >= a
    bounds = tuple([(0,1)]*len(S))
    res = scipy.optimize.linprog(c,A_ub=A_ub,b_ub=b_ub,
    bounds=bounds, options={"disp":False})
    X = res.x
    slack = res.slack
    try:
        L = []
        for i in range(len(X)):
            if round(X[i]) == 1:
                L.append(i)
        Cover = map(lambda v: S[v], L)
    except:
        Cover = []
    return Cover

def SetPacking(U,S):
    """
    Minimize: c^T*x
    Subject to: A_ub*x <= b_ub
    A_eq*x == b_eq
    (Use None for no bound in that direction)

    https://en.wikipedia.org/wiki/Linear_programming#Integer_unknowns

    res = scipy.optimize.linprog(c,A_ub=A_ub,b_ub=b_ub,
        bounds=bounds, options={"disp":True})
    print res

    https://en.wikipedia.org/wiki/Set_packing
    U = [1,2,3,4,5]
    S = [[1,2,3],[2,4],[3,4],[4,5]]
    Si = S[i]
    Xi = 0 or 1 to include set
    Minimize: -(X0 + X1 + X2 + X3)
    Subject to:
        X0 <= 1 # 1 in S0
        X0 + X1 <= 1 # 2  in S0 and S1
        X0 + X2 <= 1 # 3 in S0 and S2
        X1 + X2 + X3 <= 1 # 4 in S1,S2,S3
        X3 <= 1 # 5 in S3
        1 >= Xi >= 0 # really Xi in [0,1]
        
    https://en.wikipedia.org/wiki/Set_packing
    http://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html
    """
    c = [-1]*len(S)
    A_ub = []
    for u in U:
        row = []
        for Si in S:
            if u in Si:
                row.append(1)
            else:
                row.append(0)
        A_ub.append(row)
    b_ub = [1]*len(U)
    # None in bounds represents oo or -oo
    # bounds is a tuple of (a,b) where b >= xi >= a
    bounds = tuple([(0,1)]*len(S))
    res = scipy.optimize.linprog(c,A_ub=A_ub,b_ub=b_ub,
    bounds=bounds, options={"disp":False})
    X = res.x
    slack = res.slack
    try:
        L = []
        for i in range(len(X)):
            if round(X[i]) == 1:
                L.append(i)
        MaxPacking = map(lambda v: S[v], L)
    except:
        MaxPacking = []
    return MaxPacking

