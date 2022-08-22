from math import log
from copy import deepcopy

#################################################
# butterfly.py
#
def PseudoToGraph(G):
    V = list(range(len(G['V'])))
    d = {}
    i = 0
    for i in V:
        v = G['V'][i]
        d[v] = i
    E = []
    for e in G['E']:
        u,v = e
        f = [d[u],d[v]]
        E.append(f)
    G2 = {}
    G2['V'] = V
    G2['E'] = E
    G2['O'] = deepcopy(G['V'])
    return G2

def InAdj(doc,i):
    ii = doc['V'].index(i)
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[ii]
    for e in E:
        v,w = e
        if (u == w):
            adj.append(v)
    return adj

def OutAdj(doc,i):
    ii = doc['V'].index(i)
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[ii]
    for e in E:
        v,w = e
        if (u == v):
            adj.append(w)
    return adj

def Base(i,base, bits):
    L = []
    j = 0
    n = 0
    ii = i
    for j in range(bits):
        a = ii%base
        ii = int(ii/base)
        n = n + a*base**j
        L.append(a)
    L.reverse()
    return L

def Number(L,base):
    n = 0
    k = len(L)-1
    for i in range(len(L)):
        n = n + L[k-i]*base**i
    return n

def S(i,j,p,base,c):
    x = Base(j,base,int(round(log(p)/log(base))))
    x[i] = (x[i]+c)%base
    v = Number(x,base)
    return v,x

# [1] https://en.wikipedia.org/wiki/Butterfly_network
def Butterfly(stages,radix=2):
    p = radix**(stages-1)
    
    base = radix
    N2 = p
    N1 = int(log(p)/log(base))
    n = (N1+1)*N2
    G = {}

    G['V'] = []
    for i in range(N1+1):
        for j in range(N2):
            u = (i,j)
            G['V'].append(u)

    G['E'] = []
    for i in range(N1):
        for j in range(N2):
            u = (i,j)
            v = ((i+1)%(N1+1),j)
            e1 = [u,v]
            G['E'].append(e1)            
            for c in range(1,base):
                m,x = S(i,j,p,base,c)
                w = ((i+1)%(N1+1),m)
                e2 = [u,w]
                G['E'].append(e2)
    return G

stages0 = 5
radix0 = 2
G1 = Butterfly(stages=stages0,radix=radix0)
print("Number of processors |V(G)| =",len(G1['V']))
#G1 = MakeUndirected(G1)
G1b = PseudoToGraph(G1)

f_save = "butterfly_net_1.v"
f = open(f_save,'w')
s = """module ButterflyNet(packeti, packeto);
    input [15:0][39:0] packeti;
    output [15:0][39:0] packeto;
    reg [79:0] channel;
    reg [79:0][39:0] packetii;
    reg [79:0][39:0] packetjja;
    reg [79:0][39:0] packetjjb;
    
"""
f.write(s)
for k in range(len(G1['V'])):
    u = G1['V'][k]
    if u[0] == 0:
        s = '    assign packetii[%d] = packeti[%d];\n' % (k,u[1])
        f.write(s)
f.write('\n')
for i in range(len(G1['V'])):
    u = G1['V'][i]
    N = OutAdj(G1,u)
    if len(N) == 0:
        continue
    vv = N[0]
    ww = N[1]
    j1 = G1['V'].index(vv)
    j2 = G1['V'].index(ww)
    s = '    ButterflyNodeD bnd%03d(packetii[%d], channel[%d]);\n' % (i,i,i)
    f.write(s)
f.write('\n')
for i in range(len(G1['V'])):
    u = G1['V'][i]
    if u[0] in [4]:
        continue
    N = OutAdj(G1,u)
    vv = N[0]
    ww = N[1]
    j1 = G1['V'].index(vv)
    j2 = G1['V'].index(ww)
    s = '    switch sw%03d(packetii[%d],channel[%d], {packetjja[%d],packetjjb[%d]});\n' % (i,i,i,j1,j2)
    f.write(s)
f.write('\n')
for j in range(len(G1['V'])):
    v = G1['V'][j]
    if v[0] in [0]:
        continue
    N = InAdj(G1,v)
    uu1 = N[0]
    uu2 = N[1]
    i1 = G1['V'].index(uu1)
    i2 = G1['V'].index(uu2)
    s = '    assign packetii[%d] = (packetjja[%d]|packetjjb[%d]);\n' % (j,j,j)
    f.write(s)
f.write('\n')
for k in range(len(G1['V'])):
    u = G1['V'][k]
    if u[0] == 4:
        s = '    assign packeto[%d] = packetii[%d];\n' % (u[1],k)
        f.write(s)
f.write('\n')
f.write("endmodule\n")
f.close()
