import actions as act
import agent as agn
import shared_memory as shm
import semaphore as sem

from copy import deepcopy
from functools import reduce
import random

def find(P,name):
    for i in range(len(P)):
        if P[i].name == name:
            return i
    return None

F = lambda name: find(P,name)

def send(n,m,tag):
    global P
    a = find(P,n)
    b = find(P,m)
    word = P[a].word
    if len(P[a].program) == 0:
        return False
    cmd = P[a].program.pop(0)
    message = [word,cmd]
    flag = P[a].send(P[b],tag,message)
    if not flag:
        return flag
    P[a].word = e
    return True
def run(n,m,tag):
    global P
    a = find(P,n)
    b = find(P,m)
    if len(P[b].inbox) > 0:
        b2,tag2,message2 = P[b].inbox.pop(0)
    else:
        return False
    if F(b2) == b and tag2 == tag:
        word2,cmd2 = message2
        P[b].program.append(cmd2)
        P[b].word = word2
        P[b].run_step()
        P[b].program = []
    return True

def recv(n,m,tag):
    global P
    a = find(P,n)
    b = find(P,m)
    flag = P[a].receive(P[b], tag)
    return flag

def gather(n,m,tag):
    global P
    a = find(P,n)
    b = find(P,m)
    message = P[b].word
    P[b].word = e
    P[b].send(P[a],tag,message)
    flag = P[a].receive(P[b], tag)
    if not flag:
        return False
    if len(P[a].inbox) > 0:
        a1,tag1,msg = P[a].inbox.pop(0)
        if tag1 == tag:
            P[F(a1)].word = msg
    else:
        return False
    return True

def store(n,m,tag):
    global P,mem,S
    a = find(P,n)
    b = find(P,m)
    message = P[a].word
    # check semaphore region before storing
    if S[b].is_accessible():
        mem.L[b] = message
        return True
    return False
def load(n,m,tag):
    global P,mem,S
    a = find(P,n)
    b = find(P,m)
    # can read from semaphore region when loading
    message = mem.L[a]
    P[b].word = message
    return True

def print_x(n,m,tag):
    global P,mem
    for x in P:
        print(f"x = {x}")
    print()
    return True

def print_y(n,m,tag):
    global P,mem
    for y in mem.L:
        print(f"y = {y}")
    print()
    return True

def lock(n,m,tag):
    global P,mem,S
    a = find(P,n)
    b = find(P,m)
    S[a].lock()
    return True

def unlock(n,m,tag):
    global P,mem,S
    a = find(P,n)
    b = find(P,m)
    S[a].unlock()
    return True

def run_comm_prog(instruction_set, comm_prog,\
                verbose=True):
    global P,mem
    ready = {}
    for cmd in comm_prog:
        toks = cmd.split(";")
        for instruction in instruction_set:
            cc,ff = instruction
            if cc in list(toks[0]):
                a,b = toks[0].split(cc)
                tag = toks[1]
                try:
                    ready[a].append([cmd,ff,a,b,tag])
                except:
                    ready[a] = [[cmd,ff,a,b,tag]]
    K = list(ready.keys())
    for key in K:
        V = [tup[0] for tup in ready[key]] 
        #print(key, V)
    L = reduce(lambda s,v: s + ready[v],\
                   K,[])
    last_L_len = -1
    count = 1
    ccount = 0
    maxccount = 100
    while True and ccount < maxccount:
        if len(L) == 0:
            break  
        for a in K:
            if len(ready[a]) > 0:
                cmd,ff2,a2,b2,tag2 = ready[a][0]
                ready[a] = ready[a][1:]
                flag = ff2(a2,b2,tag2)
                if not flag:
                    ccount = ccount + 1
                    ready[a] = [[cmd,ff2,a2,b2,tag2]] + \
                            ready[a]
                    continue
                else:
                    if verbose:
                        print(f"{count}::{cmd}")
                    count = count + 1
        L2 = reduce(lambda s,v: s + ready[v],\
                   K,[])
        last_L_len = len(L)
        L = deepcopy(L2)
    for a in K:
        if verbose:
            print(f"{a} :: {ready[a]}")
    for x in P:
        if verbose:
            print(x)
    if verbose:
        print()
    if ccount == maxccount:
        print(f"ERROR: maxcount exceeded due to parallel nature")
    return

def batch_job(n,m,tag):
    prog = [
        f"{n}({n};load",
        f"{n}#{n};lock",
        f"{n}!{m};{tag}",
        f"{m}?{n};{tag}",
        f"{n}${n};unlock",
        f"{m}#{m};lock",
        f"{n}={m};{tag}",
        f"{n}<{m};{tag}",
        f"{n}){n};store",
        f"{m}${m};unlock",
        f"{n}#{n};lock",
        f"{n}${n};unlock",
        ]
    return prog

instruction_set = [
    ("!",send),
    ("?",recv),
    ("=",run),
    ("<",gather),
    (")",store),
    ("(",load),
    ("*",print_x),
    ("&",print_y),
    ("#",lock),
    ("$",unlock),
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

count = 0
N = 1
for i in range(N):
    BOSS = "BOSS"
    WORKER1 = "WORKER1"
    WORKER2 = "WORKER2"
    P = [A(BOSS,e,[]),
         A(WORKER1,e,[]),
         A(WORKER2,e,[])]

    mem = shm.SharedMemory([e for i in range(len(P))])
    S = [sem.Semaphore() for i in range(len(P))]
    mem.L[F(BOSS)] = c * (c * (c * a))
    P[F(BOSS)].program = ['a','mx1','1xv','v']

    comm_prog = []
    aa = BOSS
    for i in range(len(P[F(aa)].program)):
        bb = random.choice([WORKER1,WORKER2])
        job_i = batch_job(aa,bb,"EXE")
        comm_prog = comm_prog + job_i
    job_head = [
        f"{aa}*{aa};print_x",
        f"{aa}&{aa};print_y",
        ]
    job_tail = [
        f"{aa}*{aa};print_x",
        f"{aa}&{aa};print_y",
        ]
    comm_prog = job_head + comm_prog + job_tail

    run_comm_prog(instruction_set, comm_prog,\
            verbose=True)
    if P[F(aa)].word == a:
        count = count + 1
print(f"Accuracy = {100*count/N:0.3f}")


