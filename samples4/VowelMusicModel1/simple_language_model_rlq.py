from scipy.stats import rv_discrete
from nltk.tokenize import word_tokenize
import numpy as np

# uses scipy and ntlk and numpy

def ngrams(toks,N=1):
    d = {}
    for i in range(len(toks)-N):
        words = toks[i:i+N]
        words = tuple(words)
        try:
            d[words] = d[words] + 1
        except:
            d[words] = 1
    return d

def prob(d,N=1):
    m = {}
    K = list(d.keys())
    for key in K:
        key2 = key[:-1]
        val1 = key[-1]
        val2 = d[key]
        val = (val1,val2)
        try:
            m[key2].append(val)
        except:
            m[key2] = [val]
    K2 = list(m.keys())
    m2 = {}
    for key in K2:
        L = m[key]
        W = list(map(lambda tup: tup[0],L))
        F = list(map(lambda tup: tup[1],L))
        F = np.array(F)
        F = F / np.sum(F)
        F2 = list(F)
        L2 = list(zip(W,F2))
        m2[key] = L2
    return m2

def sample(w,m,N,nwords):
    v = w[-(N-1):]
    #print(f"v = {v}")
    K = list(m.keys())
    #print(f"K[:5] = {K[:5]}")
    s = ' '.join(list(v))
    for i in range(nwords):
        if v not in K:
            break
        L = m[v]
        #print(f"L={L}")
        W = list(map(lambda tup: tup[0],L))
        xk = list(range(len(W)))
        pk = list(map(lambda tup: tup[1],L))
        rv = rv_discrete(name='custm',values=(xk,pk))
        val = rv.rvs(size=1)
        L2 = [W[i] for i in val]
        v = list(v) + L2
        v = tuple(v[-(N-1):])
        #print(f"v = {v}")
        t = ' '.join(L2)
        #print(f"t = {t}")
        s = s + ' ' + t
    return s

def Tokenize(s):
    s = s.lower()
    toks = word_tokenize(s)
    toks = [val for val in toks if val not in ['.']]
    return toks

class SimpleLanguageModel:
    def __init__(self,N=2):
        self.N = N
        self.m = {}
        return
    def train(self,data):
        N = self.N
        s = data
        toks = Tokenize(s)
        d = ngrams(toks, N)
        m = prob(d,N)
        self.m = m
        return
    def predict(self,stem,nwords=5):
        N = self.N
        q = tuple(Tokenize(stem)[-N:])
        assert(len(q) == N)
        s2 = sample(q,self.m,N,nwords)
        s3 = ' '.join(list(q)[0:2:(N-1)]) 
        s4 = s3 + ' ' + s2
        return s4        

