import numpy as np
import graph_s as graph
import a_star_digraph as asd
from copy import deepcopy

import vswitch as vs

class DuoSwitch:
    def __init__(self,
                 hdr,
                 n_i,xi,xi_sz,
                 n_o,xo,xo_sz,
                 n_c,xc,xc_sz,
                 ):
        self.hdr = hdr
        self.n_i = n_i
        self.xi = xi
        self.xi_sz = xi_sz
        self.n_o = n_o
        self.xo = xo
        self.xo_sz = xo_sz
        self.n_c = n_c
        self.xc = list(map(lambda i: self.hdr+'.'+xc[i],
                           range(self.n_c)))
        self.xc_sz = xc_sz
        self.net1 = vs.vCrossBarSwitch(\
            f'{hdr}.sw0',
            n_i = self.n_i,
            xi = self.xi,
            xi_sz = self.xi_sz,
            n_o = self.n_c,
            xo = self.xc,
            xo_sz = self.xc_sz)
        self.net2 = vs.vCrossBarSwitch(\
            f'{hdr}.sw1',
            n_i = self.n_c,
            xi = self.xc,
            xi_sz = self.xc_sz,
            n_o = self.n_o,
            xo = self.xo,
            xo_sz = self.xo_sz)
        self.nets = [self.net1,self.net2]
        self.E = [] # edge list
        self.V = [] # vertex list
        self.W = [] # wire list
        self.S = [] # switch list
        self.cons = [] # (a,b,c) tuples for assign
        return
    def get_net(self,n):
        net = None
        for i in range(len(self.nets)):
            try:
                p = self.nets[i].name_to_port(n)
                net = self.nets[i]
            except:
                continue
        return net
    def get_graph(self):
        L = []
        for i in range(len(self.nets)):
            net = self.nets[i]
            L_i = net.get_switches() + net.get_wires()
            L = L + L_i
        V = []
        E = []
        for tup in L:
            u,v = tup
            if u not in V:
                V.append(u)
            if v not in V:
                V.append(v)
            if tup not in E:
                E.append(tup)
        G = {}
        G['V'] = V
        G['E'] = E
        G2 = graph.PseudoToGraph(G)
        return G2
    def get_path_n(self,na,nb):
        #print(f"get_path(a={a},b={b})")
        G = self.get_graph()
        #print(f"G = {G}")
        def cost(start,goal):
            return 1
        nm_start = nb
        #print(f"nm_start = {nm_start}")
        nm_goal = na
        #print(f"nm_goal = {nm_goal}")
        try:
            start = G['names'].index(nm_start)
            goal = G['names'].index(nm_goal)
            #print(f"start = {start}")
            #print(f"goal = {goal}")
            H = (G['V'],G['E'])
            #print(f"H = {H}")
            path = asd.A_star_digraph(H,
                        start,goal,cost)
            #print(f"path = {path}")
            path2 = list(map(lambda v: G['names'][v],
                         path))
            return path2
        except:
            print(f"Error: could not find path")
            return []
    def get_path(self,a,b):
        na = self.xi[a]
        nb = self.xo[b]
        path = self.get_path_n(na,nb)
        return path
    def assign(self,a,b,c):
        tup = (a,b,c)
        if tup in self.cons:
            return
        idx = 0
        x1 = self.nets[idx].to_addr(a=a,t=0,sz=1)
        y1 = self.nets[idx].to_addr(a=c,t=1,sz=1)
        self.nets[idx].link(x1,y1)
        idx = 1
        x2 = self.nets[idx].to_addr(a=c,t=0,sz=1)
        y2 = self.nets[idx].to_addr(a=1,t=1,sz=1)
        self.nets[idx].link(x2,y2)
        self.cons.append(tup)
        return
    def deassign(self,a,b,c):
        tup = (a,b,c)
        if tup not in self.cons:
            return
        idx = 0
        x1 = self.nets[idx].to_addr(a=a,t=0,sz=1)
        y1 = self.nets[idx].to_addr(a=c,t=1,sz=1)
        self.nets[idx].unlink(x1,y1)
        idx = 1
        x2 = self.nets[idx].to_addr(a=c,t=0,sz=1)
        y2 = self.nets[idx].to_addr(a=1,t=1,sz=1)
        self.nets[idx].unlink(x2,y2)
        self.cons.remove(tup)
        return
    def link(self,a,b):
        print(f"link(a,b) - not implemented yet")
        return
    def tracert_path(self,path):
        #print(f"tracert_path: path = {path}")
        path.reverse()
        print(f"tracert:")
        for i in range(len(path)):
            n = path[i]
            net = self.get_net(n)
            if net is not None:
                try:
                    busy_n = net.name_to_port(n).busy
                    print(f" n = {n}, busy = {busy_n}")
                except:
                    print(f"Error: n = {n}")
            else:
                print(f" n = {n} (virtual port)")
        return        
    def tracert_n(self,na,nb):
        path = self.get_path_n(na,nb)
        self.tracert_path(path)
        return
    def tracert(self,a,b):
        path = self.get_path(a,b)
        self.tracert_path(path)
        return
    def send_path(self,path,val):
        print(f"send_path: path = {path}")
        print(f"sending...")
        path2 = deepcopy(path)
        path2.reverse()
        path3 = []
        for n in path2:
            if self.get_net(n) is None:
                continue
            else:
                path3.append(n)
        done = False
        for i in range(len(path3)-1):
            na = path3[i]
            anet = self.get_net(na)
            if anet is None:
                continue
            nb = path3[i+1]
            bnet = self.get_net(nb)
            if bnet is None:
                continue
            ap = anet.name_to_port(na)
            bp = bnet.name_to_port(nb)
            if not done:
                ap.setdat(val)
                done = True
            # transmit from a to b
            print(f" {na}!{nb};{val}")
            bp.setdat(ap.getdat())
            #print(f" ap.getdat() = {ap.getdat()}")
            #print(f" bp.getdat() = {bp.getdat()}")
            ap.busy = 1
            bp.busy = 1
            abusy = ap.busy
            bbusy = bp.busy
            busy = abusy & bbusy
        return
    def send(self,a,b,val,verbose=False):
        path = self.get_path(a,b)
        self.send_path(path,val)
        return
    def recv(self,b,a,verbose=False):
        nb = f'b[{b}]'
        G = self.get_graph()
        if nb in G['names']:
            v = G['names'].index(nb)
            N1 = graph.OutAdj(G,v)
            N2 = graph.InAdj(G,v) 
            N = N1
            if len(N) != 1:
                print(f"Error: recv, N = {N}")
                return
            u = N[0]
            nu = G['names'][u]
            p = self.get_net(nu).name_to_port(nu)
            print(f" {nb}?{nu}")
            val = p.getdat()
            print(f"  val = {val}")
            return val
        return None
    def txrx(self,a,b,data,verbose=True):
        print(f"="*20)
        print(f"  txrx: a = {a}, b = {b}")
        print(f"     data = {data}")
        data2 = []
        for x in data:
            self.send(a,b,x,verbose)
            y = self.recv(b,a,verbose)
            if y is not None:
                data2.append(chr(y))
        msg2 = ''.join(data2)
        print(f"  Recv msg2 = '{msg2}'")
        print(f"="*20)
        return
