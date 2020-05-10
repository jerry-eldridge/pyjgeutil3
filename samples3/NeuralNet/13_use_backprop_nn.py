import backprop_nn as bpnn

from math import pi,cos,sin

L = 0.1
H = 0.9

import datetime

def label(y):
    import numpy as np
    i = np.argmax(np.array(y))
    if T[0]==1:
        return ["0","1","2"][i]
    if T[0]==2:
        return ["0","1"][i]

def f(x):
    return label(nn1.predict(x))

#T = [1,False]
T = [2,False]

if T[0]==1:
    L = 0.1
    H = 0.9
    pat = [
        [[L,H,H,L],[H,L,L]], # red
        [[L,H,L,H],[L,H,L]], # green
        [[H,L,L,H],[L,L,H]]  # blue
        ]
if T[0]==2:
    L = .1
    H = .9
    pata = [
        [[L,L],[H,L]], # 0
        [[L,H],[L,H]], # 1
        [[H,L],[L,H]], # 1
        [[H,H],[H,L]],  # 0
        ]
    L = .3
    H = .7
    patb = [
        [[L,L],[H,L]], # 0
        [[L,H],[L,H]], # 1
        [[H,L],[L,H]], # 1
        [[H,H],[H,L]],  # 0
        ]
    L = 0
    H = 1
    pat = pata + patb
    
pat2 = []
def g(x):
    y = x + random.uniform(-.05,.05)
    return y
import random
for i in range(5):
    for tup in pat:
        xi,yi = tup
        xi = list(map(g,xi))
        yi = list(map(g,yi))
        tup = [xi,yi]
        pat2.append(tup)

if T[0]==1:
    fn_model = "my_nn_1.txt" # file to read and write
if T[0]==2:
    fn_model = "my_nn_2.txt"
nn1 = bpnn.NN([])
t0 = datetime.datetime.now()
print("Please wait...training...")
flag = T[1]
if flag:
    if T[0]==1:
        nn1 = bpnn.NN([4,6,3],
                      A=["sigmoid","sigmoid"])
    if T[0]==2:
        nn1 = bpnn.NN([2,5,2],
                      A=["sigmoid","sigmoid"])
    print(nn1.S)
    nn1.train(pat2,eps=1e-4,eta=30.0, N = 100,verbose=False,
              verbose2=False,method='gd')
    nn1.save(fn_model)
else:
    nn1 = nn1.load(fn_model)
    print(nn1.S)
t1 = datetime.datetime.now()
print("train: Elapsed time:", (t1-t0).total_seconds()*1000, "ms")
for tup in pat:
    xi,yi = tup
    print(tup, f(xi),label(yi))

if 1 and (T[0] == 1):
    import sys
    sys.path.insert(0,r"C:\_PythonJGE\Utility3")
    import mapto
    import graphics_cv as racg

    from math import fmod
    
    w = 500
    h = 500
    
    pat = [
        [[L,H,H,L],[H,L,L]], # red
        [[L,H,L,H],[L,H,L]], # green
        [[H,L,L,H],[L,L,H]]  # blue
        ]

    gr = racg.Graphics(w=w,h=h)
    gr.Clear()
    def D(gr,f):
        x1 = random.uniform(0,1)
        y1 = random.uniform(0,1)
        x2 = random.uniform(0,1)
        y2 = random.uniform(0,1)
        l = f([x1,y1,x2,y2])
        if l == '0':
            color = [255,0,0]
        elif l == '1':
            color = [0,255,0]
        elif l == '2':
            color = [0,0,255]
        else:
            color = [0,0,0]
        C = [w*x1,h*y1]
        r = 30*x1
        theta = 2*pi*y1
        u = r*cos(theta) + C[0]
        v = r*sin(theta) + C[1]
        A = [u,v]
        r = 30*x2
        theta = 2*pi*y2
        u = r*cos(theta) + C[0]
        v = r*sin(theta) + C[1]
        B = [u,v]
        
        gr.Line(C,A,color)
        gr.Line(A,B,color)
        return

    for i in range(1000):
        D(gr,f)
    gr.Show("result",-1)
    #gr.Save()
    gr.Close()

if 1 and (T[0] == 2):
    import sys
    sys.path.insert(0,r"C:\_PythonJGE\Utility3")
    import mapto
    import graphics_cv as racg

    w = 600
    h = 600
    
    gr = racg.Graphics(w=w,h=h)
    gr.Clear()
    def D(gr,f):
        x1 = random.uniform(0,1)
        y1 = random.uniform(0,1)
        l = f([x1,y1])
        if l == '0':
            color = [255,0,0]
        else:
            color = [0,0,255]
        C = [w*x1,h*y1]
        r = 30*x1
        theta = 2*pi*y1
        u = r*cos(theta) + C[0]
        v = r*sin(theta) + C[1]
        A = [u,v]
        gr.Line(C,A,color)
        return

    for i in range(1000):
        D(gr,f)
    gr.Show("result",-1)
    #gr.Save()
    gr.Close()
