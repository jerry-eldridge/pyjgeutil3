import actions as act

from copy import deepcopy
from functools import reduce

M = 'B'
act.Cat3.op_name = 'x'
act.Cat3.e = 'e'
act.Cat3.v = '-'

act.Cat3.cc = 'c'
act.Cat3.aa = 'a'

def C(s):
    x = act.Cat3(M,s)
    return x

inv = act.inv
compose = act.compose
o = act.Cat3(M,'').one() # variable, do not change
c = C(act.Cat3.cc)
a = C(act.Cat3.aa)
e = C(act.Cat3.e) # identity, do not change
alphabet = [o,c,e]
# find instance of word
def does_pentagonal_diagram_commute():
    print(f"="*30)
    print("Pentagonal Diagram:")
    w1 = c * (c * a)
    prog1 = ['a','mx1','v']
    w1 = act.run_program(w1, '\n'.join(prog1))
    print(f"   w1 = {w1.pretty()}")
    w2 = c * (c * a)
    prog2 = ['1xv','v']
    w2 = act.run_program(w2, '\n'.join(prog2))
    print(f"   w2 = {w2.pretty()}")
    if w1 == w2:
        LHS1 = ' o '.join(list(reversed(prog1)))
        RHS1 = ' o '.join(list(reversed(prog2)))
        print(f"   {LHS1} == {RHS1}")
        print(f"   Pentagonal diagram commutes")
    print("="*30)
    return

def does_triangle_diagram_commute():
    print("="*30)
    print("Triangle Diagram:")
    w1 = e * a
    prog1 = ['ex1','v']
    w1 = act.run_program(w1, '\n'.join(prog1))
    print(f"   w1 = {w1.pretty()}")
    w2 = e * a
    prog2 = ['l']
    w2 = act.run_program(w2, '\n'.join(prog2))
    print(f"   w2 = {w2.pretty()}")
    
    if w1 == w2:
        LHS1 = ' o '.join(list(reversed(prog1)))
        RHS1 = ' o '.join(list(reversed(prog2)))
        print(f"   {LHS1} == {RHS1}")
        print(f"   Triangle diagram commutes")
    else:
        print(f"   Triangle diagram does not commute")
    print("="*30)
    return

does_pentagonal_diagram_commute()
does_triangle_diagram_commute()
