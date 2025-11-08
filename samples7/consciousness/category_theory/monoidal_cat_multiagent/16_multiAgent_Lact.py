import actions as act
import agent as agn

from copy import deepcopy
from functools import reduce
import random

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
    if F(b2) == b and tag2 == tag:
        word2,cmd2 = message2
        P[b].program.append(cmd2)
        P[b].word = word2
        P[b].run_step()
        P[b].program = []
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
        P[F(a1)].word = msg
    return

def run_comm_prog(instruction_set, comm_prog):
    for cmd in comm_prog:
        for x in P:
            print(x)
        print()
        print(cmd)
        toks = cmd.split(";")
        for instruction in instruction_set:
            cc,ff = instruction
            if cc in list(toks[0]):
                a,b = toks[0].split(cc)
                tag = toks[1]
                ff(a,b,tag)
    for x in P:
        print(x)
    print()
    return

def batch_job(n,m,tag):
    prog = [
        f"{n}!{m};{tag}",
        f"{m}?{n};{tag}",
        f"{n}={m};{tag}",
        f"{n}<{m};{tag}",
        ]
    return prog

instruction_set = [
    ("!",send),
    ("?",recv),
    ("=",run),
    ("<",gather)
    ]
cmd_list = [instruction_set[i][0] \
    for i in range(len(instruction_set))]
print(f"Communication instruction_set = {cmd_list}")

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

agent_instruction_set = act.instruction_set
a_cmd_list = [act.instruction_set[i][0] \
       for i in range(len(act.instruction_set))]
print(f"Agent instruction_set = {a_cmd_list}")

A = agn.Agent

BOSS = "BOSS"
WORKER1 = "WORKER1"
WORKER2 = "WORKER2"
P = [A(BOSS,e,[]),
     A(WORKER1,e,[]),
     A(WORKER2,e,[])]
F = lambda name: find(P,name)
print(f"="*30)
P[F(BOSS)].word = c * (c * a)
P[F(BOSS)].program = ['a','mx1','v']

comm_prog = []
a = BOSS
for i in range(len(P[F(a)].program)):
    b = random.choice([WORKER1,WORKER2])
    job_i = batch_job(a,b,"EXE")
    comm_prog = comm_prog + job_i

run_comm_prog(instruction_set, comm_prog)
