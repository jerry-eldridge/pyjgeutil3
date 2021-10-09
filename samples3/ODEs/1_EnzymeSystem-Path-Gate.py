import chemical_network as xn

import matplotlib.pyplot as plt

dt = 0.5
tmax = 500
ds = 5.0
    
KF = [.2,.3,.4,.34]
KR = [.1,.2,.3,.24]
KCAT = [.4,.5,.6,.2]
S = [10, 0, 3, 0]
E = [10,10,.1,10]
ES = [0,0,0,0]
    
G = {}
G['V'] = range(4)
G['E'] = [(0,1),(1,2),(2,3)]
    
TS,LS = xn.SimGraph(G,KF,KR,KCAT,S,E,ES,dt,tmax,ds)

labels = ['S0','S1','S2','S3']
xn.PlotSim(labels,TS,LS,tmax)
