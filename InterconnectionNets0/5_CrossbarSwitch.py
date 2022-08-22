import numpy as np

# [1] https://en.wikipedia.org/wiki/Crossbar_switch
#
# [2] @book{Dally04,
# author = "Dally, William James  and  Towles,
# Brian Patrick",
# title = "Principles and Practices of
# Interconnection Networks - 1st Ed",
# publisher = "Morgan Kaufmann (2004)",
# year = "2004"
# }

class CrossBarSwitch:
    def __init__(self,n,m):
        self.n = n
        self.m = m
        self.A = np.zeros((n,m),dtype=np.int8)
        return
    def set(self,out0, in0):
        assert(out0 in range(self.m))
        assert(in0 in range(self.n))
        self.A[in0,out0] = 1
        return
    def __str__(self):
        s = ''
        for j in range(self.m):
            aj = list(self.A[:,j].flatten())
            try:
                i = aj.index(1)
                v = 'out%d <- in%d\n' % (j,i)
                s = s + v
            except:
                continue
        return s
    def find_out(self, in0):
        assert(in0 in range(self.n))
        aj = list(self.A[in0:].flatten())
        I = list(filter(lambda i: aj[i]==1,
                        range(self.m)))
        return I
    def find_in(self, out0):
        assert(out0 in range(self.m))
        aj = self.A[:,out0].flatten()
        in0 = np.argmax(aj)
        return in0

S = CrossBarSwitch(8,8)
S.set(0, 1)
S.set(1, 2)
S.set(2, 1)
S.set(3, 0)
print("S=\n%s" % str(S))
S.set(1, 0)
S.set(6, 5)
print("S=\n%s" % str(S))
print("S.find_out(in0=1)=",S.find_out(in0=1))
print("S.find_in(out0=6)=",S.find_in(out0=6))

