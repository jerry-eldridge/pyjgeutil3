
# [1] MacLane, Saunders, Categories for the Working
# Mathematician (GTM 5) 2nd Ed, Springer, 1998
# [2] Microsoft Copilot, a large language model

from copy import deepcopy
import re
    
# https://en.wikipedia.org/wiki/Bubble_sort
# each time a transposition (a swap) is done.
def BubbleSort(L,compare): 
    n = len(L)
    M = deepcopy(L)
    prog = []
    while True:
        swapped = False
        for i in range(1,n):
            if compare(M[i-1],M[i]):
                tmp = M[i-1]
                M[i-1] = M[i]
                M[i] = tmp
                pi = [i-1,i]
                prog.append(pi)
                swapped = True
        if not swapped:
            break
    return prog, M

##############################################
# [1] Microsoft Copilot, a large language model
#
def inv(pi):
    L = list(zip(range(len(pi)), pi))
    L.sort(key=lambda tup: tup[1])
    pi_inv = [tup[0] for tup in L]
    return pi_inv
def compose(pi,sigma):
    tau = [sigma[pi[i]] for i in range(len(pi))]
    return tau
#
########################################

class Cat3:
    op_name = '\u2610'#'\u2297' #'BOX'# '\u2610'
    e = 'e0' # identity object
    v = '-' # variable object
    cc = 'cc'
    aa = 'aa'
    def __init__(self, c, s):
        self.c = c
        self.s = s
    def pretty(self, depth=0):
        if isinstance(self.s, str):
            return f"{self.s}"
        elif isinstance(self.s, list):
            left = self.s[0].pretty(depth + 1)
            right = self.s[1].pretty(depth + 1)
            return f"("+\
                   f"{left} {self.op_name} {right})"
    def __eq__(self, y):
        return str(self) == str(y)
    # identity object
    def zero(self):
        return Cat3(self.c,self.e)
    # functor variable object
    def one(self):
        return Cat3(self.c,self.v)
    # eta : e -> c
    def eta(self):
        if self.objs() >= 1:
            try:
                a = self.s
                if type(a) == str:
                    a = Cat3(self.c,a)
                if a == self.zero():
                    return Cat3(self.c,self.cc)
                else:
                    return self
            except:
                return self
        return self
    # (1,eta) 
    def one_times_eta(self):
        if self.objs() >= 2:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat3:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat3(self.c,a)
                    if type(b) == str:
                        b = Cat3(self.c,b)
                    b2 = b.eta()
                    return a * b2
            except:
                return self
        return self
    # (eta, 1)
    def eta_times_one(self):
        if self.objs() >= 2:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat3:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat3(self.c,a)
                    if type(b) == str:
                        b = Cat3(self.c,b)
                    a2 = a.eta()
                    return a2 * b
            except:
                return self
        return self
    # a BOX b => a * b
    def mu(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                if a.s == b.s:
                    return Cat3(self.c,a.s)
            except:
                return self
        return self
    def one_times_mu(self):
        if self.objs() >= 2:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat3:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat3(self.c,a)
                    if type(b) == str:
                        b = Cat3(self.c,b)
                    b2 = b.mu()
                    return a * b2
            except:
                return self
        return self
    # (mu, 1)
    def mu_times_one(self):
        if self.objs() >= 2:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat3:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat3(self.c,a)
                    if type(b) == str:
                        b = Cat3(self.c,b)
                    a2 = a.mu()
                    return a2 * b
            except:
                return self
        return self
    def __mul__(self, y):
        if self.c == y.c:
            return Cat3(self.c, [self,y])
        #return Cat3(self.c,[self,y])
    # (a * b) * c => a * (b * c)
    def alpha_inv(self):
        if self.objs() >= 3:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat3:
                    return self
                elif type(self.s) == list:
                    if type(self.s[0].s) == str:
                        return self
                    elif type(self.s[0].s) == Cat3:
                        return self
                    elif type(self.s[0].s) == list:
                        a = self.s[0].s[0]
                        b = self.s[0].s[1]
                    else:
                        return self
                    
                else:
                    return self
                c = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                if type(c) == str:
                    c = Cat3(self.c,c)
                return a*(b*c)
            except:
                return self
        return self
    # a * (b * c) => (a * b) * c
    def alpha(self):
        if self.objs() >= 3:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat3:
                    return self
                elif type(self.s) == list:
                    if type(self.s[1].s) == str:
                        return self
                    elif type(self.s[1].s) == Cat3:
                        return self
                    elif type(self.s[1].s) == list:
                        b = self.s[1].s[0]
                        c = self.s[1].s[1]
                    else:
                        return self
                    
                else:
                    return self
                a = self.s[0]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                if type(c) == str:
                    c = Cat3(self.c,c)
                return (a*b)*c
            except:
                return self
        return self
    # (1,alpha_inv)
    def one_times_alpha_inv(self):
        if self.objs() >= 2:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat3:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat3(self.c,a)
                    if type(b) == str:
                        b = Cat3(self.c,b)
                    b2 = b.alpha_inv()
                    return a * b2
            except:
                return self
        return self
    # (alpha_inv, 1)
    def alpha_inv_times_one(self):
        if self.objs() >= 2:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat3:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat3(self.c,a)
                    if type(b) == str:
                        b = Cat3(self.c,b)
                    a2 = a.alpha_inv()
                    return a2 * b
            except:
                return self
        return self
    # (alpha, 1)
    def alpha_times_one(self):
        if self.objs() >= 2:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat3:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat3(self.c,a)
                    if type(b) == str:
                        b = Cat3(self.c,b)
                    a2 = a.alpha()
                    return a2 * b
            except:
                return self
        return self
    # (1,alpha)
    def one_times_alpha(self):
        if self.objs() >= 2:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat3:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) != Cat3:
                        a = Cat3(self.c,a)
                    if type(b) != Cat3:
                        b = Cat3(self.c,b)
                    b2 = b.alpha()
                    return a * b2
            except:
                return self
        return self
    # a * e => a
    def rho(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                if b == b.zero():
                    return a
                return self
            except:
                return self
        return self
    # (1,rho)
    def one_rho(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                b2 = b.rho()
                return a * b2
            except:
                return self
        return self
    # (rho, 1)
    def rho_one(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                a2 = a.rho()
                return a2 * b
            except:
                return self
        return self
    # e * a => a
    def lam(self):
        if self.objs() >= 2:
            try:
                if type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat3(self.c,a)
                    if type(b) == str:
                        b = Cat3(self.c,b)
                    if a == self.zero():
                        return b
                    return self
                else:
                    return self
            except:
                return self
        return self
    def lam_one(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                a2 = a.lam()
                return a2 * b
            except:
                return self
        return self
    def one_lam(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                b2 = b.lam()
                return a * b2
            except:
                return self
        return self
    # a * b => b * a
    def gamma(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                return b * a
            except:
                return self
        return self
    # (1,gamma)
    def one_gamma(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                b2 = b.gamma()
                return a * b2
            except:
                return self
        return self
    # (gamma,1)
    def gamma_one(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                a2 = a.gamma()
                return a2 * b
            except:
                return self
        return self
    # b * a => a * b
    def gamma_inv(self):
        if self.objs() >= 2:
            try:
                b = self.s[0]
                a = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                return a * b
            except:
                return self
        return self
    # (1,gamma_inv)
    def one_gamma_inv(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                b2 = b.gamma_inv()
                return a * b2
            except:
                return self
        return self
    # (gamma_inv,1)
    def gamma_inv_one(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                a2 = a.gamma_inv()
                return a2 * b
            except:
                return self
        return self
    # length of word w
    def __len__(self):
        if type(self.s) == str:
            if self.s == self.e:
                return 0
            else:
                return 1
        elif type(self.s) == list:
            v1 = self.s[0]
            if type(v1) == str:
                if v1 == self.e:
                    a = 0
                else:
                    a = 1
            else:
                a = len(v1)
            v2 = self.s[1]
            if type(v2) == str:
                if v2 == self.e:
                    b = 0
                else:
                    b = 1
            else:
                b = len(v2)
            return a + b
        else:
            return 0
    def objs(self):
        if type(self.s) == str:
            if self.s == self.e:
                return 1
            else:
                return 1
        elif type(self.s) == list:
            v1 = self.s[0]
            if type(v1) == str:
                if v1 == self.e:
                    a = 1
                else:
                    a = 1
            else:
                a = v1.objs()
            v2 = self.s[1]
            if type(v2) == str:
                if v2 == self.e:
                    b = 1
                else:
                    b = 1
            else:
                b = v2.objs()
            return a + b
        else:
            return 0
    # fill functor '-' with values
    def fill(self, L):
        assert(len(L) == len(self))
        if type(self.s) == str:
            if self.s == self.v:
                return L[0]
            else:
                return self.s
        elif type(self.s) == list:
            v1 = self.s[0]
            n = len(v1)
            M = L[:n]
            a = v1.fill(M)
            v2 = self.s[1]
            M = L[n:]
            b = v2.fill(M)
            return Cat3(self.c,[a,b])
    # string version of word
    def __str__(self):
        if type(self.s) == str:
            return self.s
        elif type(self.s) == list:
            s = '('+str(self.s[0])+')' + \
                self.op_name + '('+str(self.s[1])+')'
            return s
    # representation of word
    def __repr__(self):
        return str(self)
    # Lact - Left Action,
    # nu : cc x aa -> aa
    def nu(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                cc = Cat3(self.c,self.cc)
                aa = Cat3(self.c,self.aa)
                if a == cc and \
                   b == aa:
                    return aa
                else:
                    return self
            except:
                return self
        return self
    # (nu,1)
    def one_nu(self):
        if self.objs() >= 2:
            try:
                a = self.s[0]
                b = self.s[1]
                if type(a) == str:
                    a = Cat3(self.c,a)
                if type(b) == str:
                    b = Cat3(self.c,b)
                b2 = b.nu()
                return a*b2
            except:
                return self
        return self

instruction_set = [
        ('e',lambda w: w.eta()),
        ('1xai',lambda w: w.one_times_alpha_inv()),
        ('aix1',lambda w: w.alpha_inv_times_one()),
        ('a',lambda w: w.alpha()),
        ('1xa',lambda w: w.one_times_alpha()),
        ('ax1',lambda w: w.alpha_times_one()),
        ('r',lambda w: w.rho()),
        ('l',lambda w: w.lam()),
        ('rx1',lambda w: w.rho_one()),
        ('lx1',lambda w: w.lam_one()),
        ('1xr',lambda w: w.one_rho()),
        ('1xl',lambda w: w.one_lam()),
        ('g',lambda w: w.gamma()),
        ('1xg',lambda w: w.one_gamma()),
        ('gx1',lambda w: w.gamma_one()),
        ('m',lambda w: w.mu()),
        ('mx1',lambda w: w.mu_times_one()),
        ('1xm',lambda w: w.one_times_mu()),
        ('ai',lambda w: w.alpha_inv),
        ('ex1',lambda w: w.eta_times_one()),
        ('1xe',lambda w: w.one_times_eta()),
        ('v',lambda w: w.nu()),
        ('1xv',lambda w: w.one_nu()),
    ]

def run_program(word, prog):
    w = word
    lines = prog.split('\n')
    #print(f"ob: {w.pretty()}")
    for line in lines:
        if len(line) == 0:
            continue
        cmd = line.strip()
        w2 = Cat3('c','None')
        for instruction in instruction_set:
            cc,ff = instruction
            if cmd == cc:
                w2 = ff(w)
                break
        #print(f"ob: {w2.pretty()}, mor: {cmd}")
        w = w2
    return w

def run_shell(word,alphabet):
    a,b,c,d,e = alphabet
    prog = []
    w = word
    print(word.pretty())
    while True:
        w2 = w
        cmd = input("cmd> ")
        cmd = cmd.strip()
        if cmd == 'q':
            break
        prog.append(cmd)
        cmd = line.strip()
        w2 = Cat3('c','None')
        if cmd == 'w':
            w2 = input("mor: ")
            pattern = "[a-de](\\*[a-de])*"
            if re.match(pattern,w2):
                w2 = eval(w2)
            else:
                print(f"Error")
                continue
        for instruction in instruction_set:
            cc,ff = instruction
            if cmd == cc:
                w2 = ff(w)
                break
        print(f"ob: {w2.pretty()},\n mor: {cmd}")
        w = w2
    return prog,w
