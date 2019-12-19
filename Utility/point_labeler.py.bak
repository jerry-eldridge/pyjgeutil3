from copy import deepcopy
import numpy as np

def pnorm(A,p):
    """
    The regular l**p norm of vector A (distance formula).
    """
    try:
        N = A.shape[0]
    except:
        N = len(A)
    S = 0
    for i in range(N):
        S += abs(A[i])**p
    return S**(1.0/p)
def norm(A):
    """
    The regular l**2 norm of vector A (distance formula).
    """
    return pnorm(A,2)
def metric(A,B):
    """
    Distance metric between vectors A and B
    Eg,
    A = [1,2,0]
    B = [10,20,20]
    """
    C = np.array(A)- np.array(B)
    return norm(list(C))

class PointLabeler:
    def __init__(self,pts,display_commands=False):
        self.pts = deepcopy(pts)
        self.display_commands = display_commands
        self.labels = []
        self.epsilon = 1 # spatial resolution
        return
    def Clear(self):
        self.pts = []
        self.labels = []
    def NearestNeighbor(self,pt):
        """
        Use Brute Force to obtain NearestNeighbor
        """
        oo = 1e8
        d = oo
        j = 0
        for i in range(len(self.pts)):
            dd = metric(pt,self.pts[i])
            if dd < d:
                j = i
                d = dd
        return d,j
    def Label(self,pt):
        d,i = self.NearestNeighbor(pt)
        label = 'P%02d' % i
        if self.display_commands:
            s = "Label(%s) = '%s'" % (str(pt),label)
            print s
        return label
    def Point(self,label):
        for i in range(len(self.labels)):
            if self.labels[i] == label:
                return self.pts[i]
        return [-999,-999]
    def Add(self,pt,label=None):
        d,i = self.NearestNeighbor(pt)
        if d >= self.epsilon:
            self.pts.append(pt)
            if label is None:
                label = self.Label(pt)
            self.labels.append(label)
            return label
        else:
            return self.labels[i]
    def Print(self):
        s = "Point Labels:\n"
        for i in range(len(self.pts)):
            s += "%d,%s,%s\n" % (i, self.labels[i],str(self.pts[i]))
        return s
