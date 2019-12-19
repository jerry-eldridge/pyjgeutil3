import numpy as np
import random
import math

# bpnn_np.py (Jerry Eldridge) - a reworked version
# using numpy arrays of what backpropagation does
# in bpnn.py minus momentum and etc.

# For general outline of backpropagation neural
# network see bpnn.py:
# # Neil Schemenauer <nas@arctrix.com>
# http://arctrix.com/nas/python/bpnn.py
# The below class follows outline of bpnn.py of the
# backpropagation part but uses numpy and
# reworked.
class BPNN:
    def __init__(self,ni,nh,no):
        # weight matrices
        self.ni = ni
        self.nh = nh
        self.no = no
        self.Wi = np.ones((nh,ni))*.8
        self.Wh = np.ones((no,nh))*.8
        for j in range(ni):
            for i in range(nh):
                self.Wi[i,j] = random.uniform(-1,1)
        for j in range(nh):
            for i in range(no):
                self.Wh[i,j] = random.uniform(-1,1)
        
        # neuron activations
        self.ai = np.ones((ni))*.8
        self.ah = np.ones((nh))*.8
        self.ao = np.ones((no))*.8
        # activation functions
        self.g = np.tanh
        self.dg = lambda x: 1.0 - x**2 # dg(g(x)) = dg/dx
        return
    def update(self,ai):
        self.ai = ai
        self.ah = self.g(np.dot(self.Wi,self.ai))
        self.ao = self.g(np.dot(self.Wh,self.ah))
        return
    def backprop(self,xi,yi,eta=0.5):
        ai = np.array(xi)
        self.update(ai)
        yo = np.array(yi)
        err = yo - self.ao
        do = self.dg(self.ao)*err
        err = np.dot(do,self.Wh)
        dh = self.dg(self.ah)*err
        dWh = np.einsum('i,j->ij',do, self.ah)
        dWi = np.einsum('i,j->ij',dh, self.ai)
        self.Wh += eta*dWh
        self.Wi += eta*dWi
        err = sum(0.5*(yo-self.ao)**2.0)
        return err
    def train(self,pat,iters=2000, eta=0.5, eps = 1e-8):
        N = len(pat)
        err_last = 0
        for i in range(iters):
            err = 0
            for k in range(N):
                xi = pat[k][0]
                yi = pat[k][1]
                err += self.backprop(xi,yi,eta=eta)
            err = math.sqrt(err)
##            print "err=",err
##            print "Wi=\n",nn.Wi
##            print "Wh=\n",nn.Wh
            if abs(err) < eps:
                break
            if abs(err-err_last) < min(eps,1e-5):
                break
            err_last = err
        return
    def H(self,x):
        if x > (HI+LO)/2.0:
            return HI
        else:
            return LO
    def predict(self,xi):
        ai = np.array(xi)
        self.update(ai)
        return map(self.H,list(self.ao))

def demo(pat,ni,nh,no):
    print "Building Back-propagation Neural Network, ni, nh, no = ", ni,nh,no
    nn = BPNN(ni,nh,no)
    nn.train(pat,iters=500,eta=0.7,eps=1e-5)
    for tup in pat:
        print "train=",tup, "predict=",nn.predict(tup[0])
    print "Wi = \n",nn.Wi
    print "Wh = \n",nn.Wh
    return nn
    
HI = .9
LO = .1
