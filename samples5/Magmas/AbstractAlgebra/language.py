class Dipole:
    def __init__(self,symbol, t):
        self.t = t
        self.s = symbol
        self.sep = ' '
    def __add__(self, y):
        tup = [self.t[-1],y.t[0]]
        if tup[0] == 's' and tup[1] == 'n':
            t = self.t[0] + y.t[-1]
            s = self.s + y.s
            return Dipole(s,t)
        if tup[0] == 'n' and tup[1] == 's':
            t = self.t[0] + y.t[-1]
            s = self.s + y.s
            return Dipole(s,t)
        if tup[0] == 's' and tup[1] == 's':
            t = self.t[0] + y.t[-1]
            s = self.s + self.sep + y.s
            return Dipole(s,t)
        if tup[0] == 'n' and tup[1] == 'n':
            t = self.t[0] + y.t[-1]
            s = self.s + self.sep + y.s
            return Dipole(s,t)
    def __str__(self):
        s = f"'{self.s}':{self.t}"
        return s
    def __repr__(self):
        return str(s)
