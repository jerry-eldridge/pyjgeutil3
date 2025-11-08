import actions as act
import agent as agn

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

A = agn.Agent

P = [A(0,e,[]),
     A(1,e,[]),
     A(2,e,[])]

def find(P,name):
    for i in range(len(P)):
        if P[i].name == name:
            return i
    return None

def send(n,m,tag):
    global P
    a = find(P,n)
    b = find(P,m)
    word = P[a].word
    cmd = P[a].program.pop(0)
    message = [word,cmd]
    P[a].send(P[b],tag,message)
    P[a].word = e
    return
def run(n,m,tag):
    global P
    a = find(P,n)
    b = find(P,m)
    b2,tag2,message2 = P[b].inbox.pop(0)
    if b2 == b and tag2 == tag:
        word2,cmd2 = message2
        P[b].program.append(cmd2)
        P[b].word = word2
        P[b].run_step()
    return

def recv(n,m,tag):
    global P
    a = find(P,n)
    b = find(P,m)
    P[a].receive(P[b], tag)
    return

def gather(n,m,tag):
    global P
    a = find(P,n)
    b = find(P,m)
    message = P[b].word
    P[b].word = e
    P[b].send(P[a],tag,message)
    P[a].receive(P[b], tag)
    a1,tag1,msg = P[a].inbox.pop(0)
    if tag1 == tag:
        P[a1].word = msg
    return

print(f"="*30)
P[0].word = c * (c * a)
P[0].program = ['a','mx1','v']

def run_comm_prog(comm_prog):
    for cmd in comm_prog:
        for x in P:
            print(x)
        print()
        print(cmd)
        toks = cmd.split(";")
        if "!" in list(toks[0]):
            a,b = toks[0].split('!')
            a = int(a)
            b = int(b)
            tag = toks[1]
            send(a,b,tag)
        elif "?" in list(toks[0]):
            a,b = toks[0].split('?')
            a = int(a)
            b = int(b)
            tag = toks[1]
            recv(a,b,tag)
        elif "=" in list(toks[0]):
            a,b = toks[0].split('=')
            a = int(a)
            b = int(b)
            tag = toks[1]
            run(a,b,tag)
        elif "<" in list(toks[0]):
            a,b = toks[0].split('<')
            a = int(a)
            b = int(b)
            tag = toks[1]
            gather(a,b,tag)
    for x in P:
        print(x)
    print()
    return

comm_prog = [
    "0!1;EXE",
    "1?0;EXE",
    "0=1;EXE",
    "0<1;EXE",
    ]

run_comm_prog(comm_prog)
