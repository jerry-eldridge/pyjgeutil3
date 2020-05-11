import backprop_nn as bpnn

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

#T = [1,True]
T = [2,True]

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

if 0 and (T[0] == 1):
    import sys
    sys.path.insert(0,r"C:\_PythonJGE\Utility3")
    import mapto
    import graphics_cv as racg

    from math import fmod
    
    w = 50 # 400
    h = 50 # 400
    
    pat = [
        [[L,H,H,L],[H,L,L]], # red
        [[L,H,L,H],[L,H,L]], # green
        [[H,L,L,H],[L,L,H]]  # blue
        ]

    gr = racg.Graphics(w=w,h=h)
    gr.Clear()
    def D(gr,f):
        for j in range(h):
            for i in range(w):
                x = mapto.MapTo(0,0,w-1,1, i)
                y = mapto.MapTo(0,0,h-1,1, j)
                u2 = fmod(2*x,1)
                v2 = fmod(2*y,1)
                u1 = fmod(4*x,1)
                v1 = fmod(4*y,1)
                l = f([u2,v2,u1,v1])
                if l == '0':
                    color = [255,0,0]
                elif l == '1':
                    color = [0,255,0]
                elif l == '2':
                    color = [0,0,255]
                else:
                    color = [0,0,0]
                gr.canvas[j,i,:] = color
        return    
    D(gr,f)
    gr.Show("result",-1)
    #gr.Save()
    gr.Close()

if 1 and (T[0] == 2):
    import sys
    sys.path.insert(0,r"C:\_PythonJGE\Utility3")
    import mapto
    import graphics_cv as racg
    
    w = 50 # 400
    h = 50 # 400
    
    gr = racg.Graphics(w=w,h=h)
    gr.Clear()
    def D(gr,f):
        for j in range(h):
            for i in range(w):
                x = mapto.MapTo(0,0,w-1,1, i)
                y = mapto.MapTo(0,0,h-1,1, j)
                l = f([x,y])
                if l == '0':
                    color = [255,0,0]
                else:
                    color = [0,0,255]
                gr.canvas[j,i,:] = color
        return    
    D(gr,f)
    gr.Show("result",-1)
    #gr.Save()
    gr.Close()
