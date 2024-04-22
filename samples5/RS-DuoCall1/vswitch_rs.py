import numpy as np
import graph_s as graph
import a_star_digraph as asd
from copy import deepcopy

# implement (verilog) bits and switch module
class vArray:
    def __init__(self, n):
        self.sz = n
        self.dat = [0]*self.sz
    def getsz(self):
        return self.sz
    def getdat(self):
        return deepcopy(self.dat)
    def setdat(self,val):
        self.dat = val
        return
    def setzero(self):
        self.dat = [0]*self.sz()
        return
class vPort:
    def __init__(self,hdr, a, t, sz, verbose=False):
        self.hdr = hdr
        self.a = a
        self.t = t
        self.busy = 0
        self.sz = sz
        self.I = vArray(sz)
        self.V = vArray(sz)
        self.m = ['i','o','io']
        if verbose:
            print(f"Created port {str(self)}")
    def get_label(self):
        n = f"{self.hdr}.{self.m[self.t]}.{self.a}"
        return n
    def get_I(self):
        return self.I.getdat()
    def set_I(self,val):
        self.I.setdat(val)
    def get_V(self):
        return self.V.getdat()
    def set_V(self,val):
        self.V.setdat(val)
    def __str__(self):
        return self.get_label()
    def __repr__(self):
        return str(self)

class vEdge:
    def __init__(self, port1, port2, verbose=False):
        self.port1 = port1
        self.port2 = port2
        if verbose:
            print(f"Created Edge {str(self)}")
    def label(self):
        n = (str(self.port1),str(self.port2))
        return n
    def __str__(self):
        s = str(self.label())
        return s
    def __repr__(self):
        return str(self)

class vCrossBarSwitch:
    def __init__(self,
                 hdr,
                 n_i,xi,xi_sz,
                 n_o,xo,xo_sz,
                 n_io=0,xio=[],xio_sz=[],
                 ):
        self.hdr = hdr # header (name) of module
        self.n_i = n_i # number of inputs
        self.xi_sz = xi_sz # size of each input data
        self.xi = xi # names of each input
        self.n_o = n_o # number of outputs
        self.xo_sz = xo_sz # size of each output
        self.xo = xo # names of each output
        self.n_io = n_io # number of inputs/outputs
        self.xio_sz = xio_sz # sizes of inputs/outputs
        self.xio = xio # names of each input/output
        self.P = {} # port dictionary
        self.E = [] # edge list
        self.V = [] # vertex list
        self.W = [] # wire list
        self.S = [] # switch list
        self.g_S = {} # conductance g list for S
        self.g_W = {} # conductance g list for W
        self._g = {} # conductance g list
        self.build()
    def get_wires(self):
        W = deepcopy(self.W)
        return W
    def get_switches(self):
        S = deepcopy(self.S)
        return S
    def get_g_W(self):
        dg = self.g_W
        return dg
    def get_g_S(self):
        dg = self.g_S
        return dg
    def get_g(self):
        KW = list(self.g_W.keys())
        KS = list(self.g_S.keys())
        K = list(set(KW) | set(KS))
        for key in K:
            if key in KW:
                self._g[key] = self.g_W[key]
            if key in KS:
                self._g[key] = self.g_S[key]
        return self._g
    def get_graph(self):
        L = self.get_switches() + self.get_wires()
        d_g = self.get_g()
        g = [d_g[tup] for tup in L]
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
        G['g'] = g
        G2 = graph.PseudoToGraph(G)
        return G2
    def to_addr(self,a,t,sz):
        x = (a,t,sz)
        return x
    def get_label(self,addr):
        a,t,sz = addr
        m = ['i','o','io']
        n = f'{self.hdr}.{m[t]}.{a}'
        return n
    def name_to_addr(self,n):
        toks = n.split('.')
        toks.reverse()
        a = int(toks[0])
        s = toks[1]
        m = ['i','o','io']
        addr = None
        if s in m:
            t = m.index(s)
            if t == 0:
                sz = self.xi_sz[a]
                addr = (a,t,sz)
            if t == 1:
                sz = self.xo_sz[a]
                addr = (a,t,sz)
            if t == 2:
                sz = self.xio_sz[a]
                addr = (a,t,sz)
        return addr        
    def build_wires(self,verbose=True):
        t = 0
        g = 1
        for a in range(self.n_i):
            w1 = self.xi[a]
            sz = self.xi_sz[a]
            addr = (a,t,sz)
            w2 = self.get_label(addr)
            self.add_wire(w1,w2,g)
        t = 1
        g = 1
        for a in range(self.n_o):
            w2 = self.xo[a]
            sz = self.xo_sz[a]
            addr = (a,t,sz)
            w1 = self.get_label(addr)
            self.add_wire(w1,w2,g)
        t = 2
        g = 1
        for a in range(self.n_io):
            w1 = self.xio[a]
            sz = self.xio_sz[a]
            addr = (a,t,sz)
            w2 = self.get_label(addr)
            self.add_wire(w1,w2,g)
            self.add_wire(w2,w1,g)            
        return
    def build_port(self,addr,verbose=False):
        a,t,sz = addr
        p = vPort(self.hdr,a,t,sz,verbose)
        n = p.get_label()
        self.P[n] = p
        self.V.append(n)
        return
    def build_ports(self):
        # build input ports
        t = 0 # input port type
        for a in range(self.n_i):
            sz = self.xi_sz[a]
            addr = (a,t,sz)
            self.build_port(addr)

        # build output ports
        t = 1 # output port type
        for a in range(self.n_o):
            sz = self.xo_sz[a]
            addr = (a,t,sz)
            self.build_port(addr)

        # build input/output ports
        t = 2 # input/output port type
        for a in range(self.n_io):
            sz = self.xio_sz[a]
            addr = (a,t,sz)
            self.build_port(addr)
        return
    def name_to_port(self,n):
        return self.P[n]
    def addr_to_port(self,x):
        n = self.get_label(x)
        return self.P[n]
    def build(self):
        self.build_ports()
        self.build_wires()
        return
    def get_verilog(self):
        print(f"vModule.get_verilog(): need to define.")
        return
    def add_wire(self,w1,w2, g):
        tup = (w2,w1)
        if tup not in self.W:
            print(f"adding wire {tup}")
            self.W.append(tup)
        if tup not in self.g_W.keys():
            self.g_W[tup] = g
        return tup
    def remove_wire(self,w1,w2):
        tup = (w2,w1)
        if tup in self.W:
            print(f"removing wire {tup}")
            self.W.remove(tup)
        if tup in self.g_W.keys():
            del self.g_W[tup]
    def add_switch(self,w1,w2,g):
        tup = (w2,w1)
        if tup not in self.S:
            print(f"adding switch {tup}")
            self.S.append(tup)
            p2 = self.name_to_port(tup[0])
            p1 = self.name_to_port(tup[1])
        if tup not in self.g_S.keys():
            self.g_S[tup] = g
        return tup
    def remove_switch(self,w1,w2):
        tup = (w2,w1)
        if tup in self.S:
            print(f"removing switch {tup}")
            self.S.append(tup)
            p2 = self.name_to_port(tup[0])
            p1 = self.name_to_port(tup[1])
            if tup in self.g_S:
                del self.g_S[tup]
        return tup
    def link(self,x,y,g):
        na = self.get_label(x)
        nb = self.get_label(y)
        self.add_switch(na,nb,g)
        return
    def unlink(self,x,y):
        na = self.get_label(x)
        nb = self.get_label(y)
        self.remove_switch(na,nb)
        return
    def get_path(self,a,b):
        #print(f"get_path(a={a},b={b})")
        G = self.get_graph()
        d_g = self.get_g()
        k_g = list(d_g.keys())
        #print(f"G = {G}")
        def cost(start,goal):
            tup = (start,goal)
            oo = 1e12
            epsilon = 1e-12
            # calculate resistance R and use as cost
            if tup in k_g:
                if abs(k_g[tup]) > epsilon:
                    R = 1/k_g[tup]
                else:
                    R = oo
            else:
                R = oo
            return R
        na = self.xi[a]
        nb = self.xo[b]
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



    
