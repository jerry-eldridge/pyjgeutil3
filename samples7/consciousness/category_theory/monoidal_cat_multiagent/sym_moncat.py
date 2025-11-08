
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

class Cat1:
    def __init__(self, s):
        self.s = s
        self.e = 'e0' # identity object
        self.v = '-' # variable object
        self.op_name = 'BOX'# '\u2610'
    def pretty(self, depth=0):
        if isinstance(self.s, str):
            return f"{self.s}"
        elif isinstance(self.s, list):
            left = self.s[0].pretty(depth + 1)
            right = self.s[1].pretty(depth + 1)
            return f"({self.op_name} "+\
                   f"{left} {right})"
        
    def __eq__(self, y):
        return str(self) == str(y)
    # identity object
    def zero(self):
        return Cat1(self.e)
    # functor variable object
    def one(self):
        return Cat1(self.v)
    # multiplication self box y
    def __mul__(self, y):
        return Cat1([self,y])
    # (a * b) * c => a * (b * c)
    def alpha_inv(self):
        if self.objs() >= 3:
            try:
                if type(self.s) == str:
                    return self
                elif type(self.s) == Cat1:
                    return self
                elif type(self.s) == list:
                    if type(self.s[0].s) == str:
                        return self
                    elif type(self.s[0].s) == Cat1:
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
                    a = Cat1(a)
                if type(b) == str:
                    b = Cat1(b)
                if type(c) == str:
                    c = Cat1(c)
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
                elif type(self.s) == Cat1:
                    return self
                elif type(self.s) == list:
                    if type(self.s[1].s) == str:
                        return self
                    elif type(self.s[1].s) == Cat1:
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
                    a = Cat1(a)
                if type(b) == str:
                    b = Cat1(b)
                if type(c) == str:
                    c = Cat1(c)
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
                elif type(self.s) == Cat1:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat1(a)
                    if type(b) == str:
                        b = Cat1(b)
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
                elif type(self.s) == Cat1:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat1(a)
                    if type(b) == str:
                        b = Cat1(b)
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
                elif type(self.s) == Cat1:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) == str:
                        a = Cat1(a)
                    if type(b) == str:
                        b = Cat1(b)
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
                elif type(self.s) == Cat1:
                    return self
                elif type(self.s) == list:
                    a = self.s[0]
                    b = self.s[1]
                    if type(a) != Cat1:
                        a = Cat1(a)
                    if type(b) != Cat1:
                        b = Cat1(b)
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
                    a = Cat1(a)
                if type(b) == str:
                    b = Cat1(b)
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
                    a = Cat1(a)
                if type(b) == str:
                    b = Cat1(b)
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
                    a = Cat1(a)
                if type(b) == str:
                    b = Cat1(b)
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
                        a = Cat1(a)
                    if type(b) == str:
                        b = Cat1(b)
                    if a == a.zero():
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
                    a = Cat1(a)
                if type(b) == str:
                    b = Cat1(b)
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
                    a = Cat1(a)
                if type(b) == str:
                    b = Cat1(b)
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
                    a = Cat1(a)
                if type(b) == str:
                    b = Cat1(b)
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
                    a = Cat1(a)
                if type(b) == str:
                    b = Cat1(b)
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
                    a = Cat1(a)
                if type(b) == str:
                    b = Cat1(b)
                a2 = a.gamma()
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
            return Cat1([a,b])
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

def run_program(word, prog):
    w = word
    lines = prog.split('\n')
    print(f"ob: {w.pretty()}")
    for line in lines:
        if len(line) == 0:
            continue
        cmd = line.strip()
        if cmd == 'ai':
            w2 = w.alpha_inv()
        elif cmd == '1xai':
            w2 = w.one_times_alpha_inv()
        elif cmd == 'aix1':
            w2 = w.alpha_inv_times_one()
        elif cmd == 'a':
            w2 = w.alpha()
        elif cmd == '1xa':
            w2 = w.one_times_alpha()
        elif cmd == 'ax1':
            w2 = w.alpha_times_one()
        elif cmd == 'r':
            w2= w.rho()
        elif cmd == 'l':
            w2 = w.lam()
        elif cmd == 'rx1':
            w2= w.rho_one()
        elif cmd == 'lx1':
            w2 = w.lam_one()
        elif cmd == '1xr':
            w2 = w.one_rho()
        elif cmd == '1xl':
            w2 = w.one_lam()
        elif cmd == 'g':
            w2 = w.gamma()
        elif cmd == '1xg':
            w2 = w.one_gamma()
        elif cmd == 'gx1':
            w2 = w.gamma_one()
        print(f"ob: {w2.pretty()}, mor: {cmd}")
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
        if cmd == 'ai':
            w2 = w.alpha_inv()
        elif cmd == '1xai':
            w2 = w.one_times_alpha_inv()
        elif cmd == 'aix1':
            w2 = w.alpha_inv_times_one()
        elif cmd == 'a':
            w2 = w.alpha()
        elif cmd == '1xa':
            w2 = w.one_times_alpha()
        elif cmd == 'ax1':
            w2 = w.alpha_times_one()
        elif cmd == 'r':
            w2= w.rho()
        elif cmd == 'l':
            w2 = w.lam()
        elif cmd == 'rx1':
            w2= w.rho_one()
        elif cmd == 'lx1':
            w2 = w.lam_one()
        elif cmd == '1xr':
            w2 = w.one_rho()
        elif cmd == '1xl':
            w2 = w.one_lam()
        elif cmd == 'g':
            w2 = w.gamma()
        elif cmd == '1xg':
            w2 = w.one_gamma()
        elif cmd == 'gx1':
            w2 = w.gamma_one()
        elif cmd == 'w':
            w2 = input("mor: ")
            pattern = "[a-de](\\*[a-de])*"
            if re.match(pattern,w2):
                w2 = eval(w2)
            else:
                print(f"Error")
                continue
        print(f"ob: {w2.pretty()},\n mor: {cmd}")
        w = w2
    return prog,w
