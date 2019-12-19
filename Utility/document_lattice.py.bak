from LCS import LongestCommonSubsequence as LCS

def GetText(fn):
    f = open(fn,'r')
    text = f.read()
    f.close()
    return text

def AddLines(L,text):
    L2 = text.split('\n')
    for line in L2:
        if line not in L:
            L.append(line)
    return L

def Lookup(L,s):
    i = 0
    for line in L:
        if line == s:
            return i
        i += 1
    return -1

def Sequence(L,text):
    L = AddLines(L,text)
    L2 = text.split('\n')
    seq = []
    for line in L2:
        i = Lookup(L,line)
        seq.append(i)
    return L, seq

def ToText(L, seq):
    text = ""
    count = 0
    for i in seq:
        text += L[i]
        if count < len(seq)-1:
            text += "\n"
        count += 1
    return text

def ToSeq(L):
    seq = []
    for line in L:
        i = Lookup(L,line)
        seq.append(i)
    return seq

def Join(tx1,tx2):
    L = []
    L,seq1 = Sequence(L,tx1)
    L,seq2 = Sequence(L,tx2)
    seq4 = ToSeq(L)
    tx4 = ToText(L,seq4)
    return tx4

def Meet(tx1,tx2):
    L = []
    L,seq1 = Sequence(L,tx1)
    L,seq2 = Sequence(L,tx2)
    seq3 = LCS(seq1,seq2)
    tx3 = ToText(L,seq3)
    return tx3
