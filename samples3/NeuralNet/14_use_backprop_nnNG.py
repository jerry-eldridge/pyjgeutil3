import backprop_nn as bpnn

LO = 0.1
HI = 0.9

import datetime

bits = [1,False]

def g(N,S):
    xi = [LO]*N
    for i in list(S):
        j = i-1
        xi[j] = HI
    return xi

if bits[0] == 1:
    M = 3 # M classes, classes are 1 to M.
    N = 3 # N inputs, inputs are set of N objects
          # in X = range(1,N+1).
    # [...[xi,yi]...] xi is inputs yi is class 
    data = [[[1,2,3],[1]],[[1,3],[1]],[[2],[1]],
            [[3],[1]],
        [[3,2],[3]],[[1],[2]],[[2,1],[3]]]
    pat = []
    for tup in data:
        xi = g(N,tup[0])
        yi = g(M,tup[1])
        pat.append([xi,yi])

if bits[0]==1:
    import datetime
    fn_model = "subset-learn-1.txt"
    t0 = datetime.datetime.now()
    nn1 = bpnn.NN([3,4,4,3],
            A=["sigmoid","sigmoid","sigmoid"])
    train = bits[1]
    if train:
        print("Please wait...training...")
        nn1.train(pat,eta=20.0, N = 100,verbose=False,
             method='nm')
        nn1.save(fn_model)
    else:
        nn1 = nn1.load(fn_model)
        nn1.save("t"+fn_model)

    
    t1 = datetime.datetime.now()
    print("train: Elapsed time:", (t1-t0).total_seconds()*1000, "ms")
    #for tup in pat:
    #    xi,yi = tup
    #    print(tup, nn1.predict(xi),yi)

    from copy import deepcopy
    import numpy as np
    def f(N,S):
        xi = g(N,S)
        y = nn1.predict(xi)
        k = np.argmax(np.array(yi))
        return [k+1]
    for tup in data:
        S,c = tup
        xi = g(N,tup[0])
        yi = g(M,tup[1])
        print(S,f(N,S),c)
