import abstract_types as adt
import random

seed0 = 12345
random.seed(seed0)

def demo(N):
    sSigma = "abcd"
    tSigma = ["ns","sn"]
    start = adt.mydipole("","ns")
    word = start
    for i in range(N):
        s = random.choice(list(sSigma))
        t = random.choice(tSigma)
        ch = adt.mydipole(s,t)        
        word = word + ch
    print(f"word = {word}")
    return

M = 10
for i in range(M):
    demo(N=20)
    print()

def demo2(sent):
    start = adt.mydipole("","ns")
    sent2 = start
    for i in range(len(sent)):
        s = sent[i]
        if s == ' ':
            s = ''
            t = "sn"
        else:
            t = "ns"
        ch = adt.mydipole(s,t)
        sent2 = sent2 + ch
    print(f"sent2 = {sent2}")
    return

sent = "happy birthday to you"
print(f"sent = '{sent}'")
demo2(sent)
print()
adi = adt.myint
adp = adt.mydipole
a = adp('a','sn')
b = adp('b', 'ns')
for s in [a,b,a+a,a+b,b+a,b+b,a+a+a,a+a+b,a+b+a,
          a+b+b,b+a+a,b+a+b,b+b+a,b+b+b]:
    print(f"s = {s+s}")
