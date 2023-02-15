import backprop_nn as bpnn

nn = bpnn.NN([2,5,1])
LO = 0.1
HI = 0.9
pat = [[[LO,LO],[LO]],
       [[LO,HI],[HI]],
       [[HI,LO],[HI]],
       [[HI,HI],[LO]]]
import datetime
t0 = datetime.datetime.now()
print("Please wait...training...")
nn.train(pat,eta=10.0, N = 200,verbose=False,
         method='gd')
t1 = datetime.datetime.now()
print("train: Elapsed time:", (t1-t0).total_seconds()*1000, "ms")
for tup in pat:
    xi,yi = tup
    print(tup, nn.predict(xi),yi)

nn = bpnn.NN([2,5,1])
LO = 0.1
HI = 0.9
pat = [[[LO,LO],[LO]],
       [[LO,HI],[HI]],
       [[HI,LO],[HI]],
       [[HI,HI],[LO]]]
import datetime
t0 = datetime.datetime.now()
print("Please wait...training...")
nn.train(pat,eta=10.0, N = 200,verbose=False,
         method='nm')
t1 = datetime.datetime.now()
print("train: Elapsed time:", (t1-t0).total_seconds()*1000, "ms")
for tup in pat:
    xi,yi = tup
    print(tup, nn.predict(xi),yi)
