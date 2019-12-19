from copy import deepcopy
from math import acos,pi,sqrt

class Words:
    def __init__(S):
        S.words = []
        return
    def add(S,word):
        if word not in S.words:
            S.words.append(word)
        return
    def Clear(S):
        S.words = []
W = Words()
class Term:
    def __init__(S,word,a):
        S.word = word
        S.a = 1
        return
    def __smul__(S,a):
        a2 = S.a*a
        return Word(S.word,a2)
    def Zero(S):
        return Word("",0)
    def __mul__(S,word_term):
        if S.word == word_term.word:
            a = S.a*word_term.a
            return Word(S.word,a)
        else:
            return S.Zero()     
    def __str__(S):
        return str(S.L)
class Word:
    def __init__(S,L,A=None,words=W):
        if A == None:
            A = [1]*len(L)
        L = map(lambda s: s.lower(), L)
        S.V = zip(L,A)
        S.V.sort(key = lambda tup: tup[0])
        S.words = words
        for word in L:
            S.words.add(word)
        return
    def __add__(S,word):
        L1 = map(lambda tup: tup[0],S.V)
        A1 = map(lambda tup: tup[1],S.V)
        L2 = map(lambda tup: tup[0],word.V)
        A2 = map(lambda tup: tup[1],word.V)
        L = list(set(L1) | set(L2))
        L.sort()
        A = [0]*len(L)
        for i in range(len(L1)):
            word = L1[i]
            a = L1[i]
            j = L.index(word)
            A[j] += A1[i]
        for i in range(len(L2)):
            word = L2[i]
            a = L2[i]
            j = L.index(word)
            A[j] += A2[i]
        return Word(L,A,S.words)
    def __rmul__(S,a):
        L1 = map(lambda tup: tup[0],S.V)
        A1 = map(lambda tup: a*tup[1],S.V)
        return Word(L1,A1,S.words)
    def __mul__(S,word):
        L1 = map(lambda tup: tup[0],S.V)
        A1 = map(lambda tup: tup[1],S.V)
        L2 = map(lambda tup: tup[0],word.V)
        A2 = map(lambda tup: tup[1],word.V)
        L = list(set(L1) & set(L2))
        L.sort()
        A = [1]*len(L)
        for i in range(len(L)):
            j = L1.index(L[i])
            a = A1[j]
            A[i] *= a
        for i in range(len(L)):
            j = L2.index(L[i])
            a = A2[j]
            A[i] *= a
        return sum(A)
    def __str__(S):
        s = ''
        L1 = map(lambda tup: tup[0],S.V)
        A1 = map(lambda tup: tup[1],S.V)
        for i in range(len(S.V)):
            word = L1[i]
            a = A1[i]
            t = str(a)+'*'+word
            s += t+' + '
        s = s[:-3]
        return s
# norm of inner product space of Word objects
def norm(word):
    w = sqrt(word*word)
    return w
# cosine similarity of two Word objects
def clamp(lo,hi,x):
    return min(hi,max(lo,x))
def d0(word1,word2):
    ca = word1*word2
    x = 1.0*ca/(norm(word1)*norm(word2))
    x = clamp(-1.0,1.0,x)
    theta = acos(x)
    degrees = theta*180/pi
    return degrees
# cosine similarity between two lists of strings
def d1(L1,L2):
    word1 = Word(L1)
    word2 = Word(L2)
    return d0(word1,word2)
# cosine similarity between two strings with " " separator
def d2(s1,s2):
    # create lists of words by splitting by " " character
    # first removing surrounding whitespace characters.
    s1 = s1.strip()
    s2 = s2.strip()
    L1 = s1.split(" ")
    L2 = s2.split(" ")
    return d1(L1,L2)
