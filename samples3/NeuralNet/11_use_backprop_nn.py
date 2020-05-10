import backprop_nn as bpnn

LO = 0.1
HI = 0.9

import datetime

bits = [1,0]

if bits[0] or bits[1]:
    pat = [[[LO,LO],[LO]],
       [[LO,HI],[HI]],
       [[HI,LO],[HI]],
       [[HI,HI],[LO]]]

if bits[0]:
    nn1 = bpnn.NN([2,5,1])
    print(nn1.S)
    t0 = datetime.datetime.now()
    print("Please wait...training...")
    nn1.train(pat,eta=20.0, N = 100,verbose=False,
             method='gd')
    t1 = datetime.datetime.now()
    print("train: Elapsed time:", (t1-t0).total_seconds()*1000, "ms")
    for tup in pat:
        xi,yi = tup
        print(tup, nn1.predict(xi),yi)

if bits[1]:
    nn2 = bpnn.NN([2,5,1])
    import datetime
    t0 = datetime.datetime.now()
    print("Please wait...training...")
    nn2.train(pat,eta=20.0, N = 100,verbose=False,
             method='nm')
    t1 = datetime.datetime.now()
    print("train: Elapsed time:", (t1-t0).total_seconds()*1000, "ms")
    for tup in pat:
        xi,yi = tup
        print(tup, nn2.predict(xi),yi)
