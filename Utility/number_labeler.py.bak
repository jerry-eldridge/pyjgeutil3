from copy import deepcopy

def norm(A):
    """
    The regular l**2 norm of number A (distance formula).
    """
    return abs(A)
def metric(A,B):
    """
    Distance metric between numbers A and B
    """
    C = A - B
    return norm(C)

class NumberLabeler:
    def __init__(self,pts,display_commands=False):
        self.pts = deepcopy(pts)
        self.display_commands = display_commands
        self.labels = []
        self.number_labels = []
        self.epsilon = 1e-5 # spatial resolution
        return
    def Clear(self):
        self.pts = []
        self.labels = []
        self.number_labels = []
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
        label = 'AE%03d' % i
        number_label = 'AE%03d' % i
        if self.display_commands:
            s = "Label(%s) = '%s', '%s'" % (str(pt),label,number_label)
            print s
        return label,number_label
    def Point(self,label):
        for i in range(len(self.labels)):
            if self.labels[i] == label:
                return self.pts[i]
        return -999
    def PointNumber(self,number_label):
        for i in range(len(self.number_labels)):
            if self.number_labels[i] == number_label:
                return self.pts[i]
        return -999
    def Add(self,pt,number_label=None):
        d,i = self.NearestNeighbor(pt)
        if d >= self.epsilon:
            self.pts.append(pt)
            label,number_label0 = self.Label(pt)
            self.labels.append(label)
            if number_label is None:
                self.number_labels.append(number_label0)
            else:
                self.number_labels.append(number_label)            
            return label
        else:
            return self.labels[i]
    def Print(self):
        s = "Point Labels:\n"
        for i in range(len(self.pts)):
            s += "%d,%s,%s,%s\n" % (i, self.labels[i],str(self.number_labels[i]),str(self.pts[i]))
        return s
