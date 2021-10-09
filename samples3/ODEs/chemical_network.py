import enzyme_reaction as enz

import matplotlib.pyplot as plt

def SimGraph(G,KF,KR,KCAT,S,E,ES,dt,tmax,ds):
    t = 0
    u = 0
    L = []
    TL = []
    Z = [None]*len(S)

    ei = 0 # choose first reaction to start

    TS = []
    for i in range(len(S)):
        Ti = []
        TS.append(Ti)

    LS = []
    for i in range(len(S)):
        Li = []
        LS.append(Li)

    while t < tmax:
        e = G['E'][ei]
        u,v = e
        Z[u] = enz.EnzymeR(kf=KF[u],kr=KR[u],kcat=KCAT[u],
                     E=E[u],S=S[u],ES=ES[u],P=S[v],dt=dt)
        T,Y = Z[u].sim(tmin=t,tmax=t+ds,name="RK4")
        s = t
        for tup in Y:
            LS[u].append(tup[1])
            TS[u].append(s)
            LS[v].append(tup[3])
            TS[v].append(s)
            s = s + dt
        E[u] = Y[-1][0]
        S[u] = Y[-1][1]
        ES[u] = Y[-1][2]
        S[v] = Y[-1][3]
        t = t + ds
        ei = (ei+1)%len(G['E'])
    return LS,TS

def PlotSim(labels,LS,TS,tmax):
    assert(len(LS)==len(labels))
    color = ['b']*len(labels)
    N = len(labels)
    f, ax = plt.subplots(N)
    for j in range(len(labels)):
        Lj = list(map(lambda tup: tup[j], LS))
        ax[j].set_xlim(0,tmax)
        ax[j].plot(TS[j],LS[j],color[j])
        #ax[j].scatter(TS[j],LS[j])
    for j in range(len(ax)):
        ax[j].set(xlabel='t',ylabel=labels[j])
    plt.show()
    return
