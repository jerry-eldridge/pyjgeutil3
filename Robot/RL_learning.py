from math import exp
import functools

import numpy as np # Before 'pip install numpy'
import scipy.stats as ss # Before 'pip install scipy'

import time

def R_t(R,t,gamma=.9):
    t = max(0,min(len(R),t))
    T = len(R)
    S = 0
    for i in range(t):
        S = S + gamma**(t+i)*R[i]
    return S

# Value based on future rewards
class Value:
    def __init__(self,alpha=.3,gamma=.9):
        self.value = {}
        self.alpha = alpha
        self.gamma = gamma
    def set(self,s_t,val):
        self.value[s_t] = val
    def V(self,s_t):
        try:
            return self.value[s_t]
        except:
            return 0
    def update(self,s_t,R,t):
        R_val = R_t(R,t,self.gamma)
        self.set(s_t,self.V(s_t) + \
                self.alpha*(R_val - self.V(s_t)))
        return
    def __str__(self):
        return str(self.value)

def softmax(z):
    a = list(map(exp,z))
    b = sum(a)
    c = [0]*len(a)
    for i in range(len(c)):
        c[i] = a[i]/b
    return c

# choose from items based on reward
def Choose(V,N):
    global rng
    s = list(V.value.keys())
    z = list(map(lambda s_i: V.V(s_i), s))
    c = softmax(z)
    print("pk =",list(zip(s,c)))
    rv = rv_discrete(xk=s,pk=c,seed=time.time())
    M = rv.rvs(size=N)
    return M

def Build_V(seq,alpha=.3,gamma=.9):
    V = Value(alpha,gamma)
    states = []
    rewards = []
    T = []
    for i in range(len(seq)):
        tup = seq[i]
        if tup[0] not in states:
            states.append(tup[0])
            V.set(tup[0],0)
            rewards.append([0])
            T.append(i)
    for j in range(len(seq)):
        tup = seq[j]
        i = states.index(tup[0])
        rewards[i].append(tup[1])
        V.update(states[i],rewards[i],j)
    return V

def Display(seq):
    V = Build_V(seq,alpha=.3,gamma=.9)
    print(V)
    print()

    N = 1000
    print("Sampling N = ", N, "from V")

    # From the list of events, the next event is
    # transitioned to by a behavior, a_t.
    # Below M is a sampling of the next event.
    M = Choose(V,N)
    d = {}
    for m in M:
        try:
            d[m] = d[m] + 1
        except:
            d[m] = 1
    print("Sampling: ",d)
    return

class RLLearn:
    def __init__(self,alpha=.3,gamma=.9):
        self.seq = [("",-100),("",-100)]
        self.alpha = alpha
        self.gamma = gamma
        V0 = Build_V(self.seq,self.alpha,
                         self.gamma)
        self.V0 = V0
        return
    def insert(self, action, reward):
        tup = (action,reward)
        self.seq.append(tup)
    def learn(self):
        V0 = Build_V(self.seq,self.alpha,
                         self.gamma)
        self.V0 = V0
        return
    def __str__(self):
        V = self.V0.value
        s = ''
        for key in V.keys():
            t = '%s,%f\n' % (key,V[key])
            s = s + t
        return s
    def values(self):
        return self.V0.value
    def choose(self):
        V = self.V0.value
        K = list(V.keys())
        Y = list(map(lambda key: V[key], K))
        pk = list(softmax(np.array(Y)))
        xk = range(len(K))
        rv = ss.rv_discrete(name='custm',
                    values=(xk,pk))
        L = rv.rvs(size=1)
        c = L[0]
        key = K[c]
        self.K = K
        self.xk = xk
        self.pk = pk
        self.c = c
        return key
