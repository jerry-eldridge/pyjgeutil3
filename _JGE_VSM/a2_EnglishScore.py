# First install nltk python library, then nltk corpora with Install()
from nltk.corpus import words
from nltk.tokenize import wordpunct_tokenize
from nltk import download

import pickle as pickle
import os
import fnmatch
import os.path
from functools import reduce

def Install():
     print("Installing ntlk corpora, select at least words and wordnet")
     print("A corpora is usually a (text) file or several files stored at")
     print("the ntlk install folder somewhere")
     download()
     return

def WordDict(words):
    D = {}
    for word in words:
        D[word] = 1
    return D
def WordScore(D,word):
    try:
        return D[word]
    except:
        D[word] = 0
        return D[word]
def TextScore(D,text):
    tokens = wordpunct_tokenize(text)
    tokens = list(map(str.lower,tokens))
    N = len(tokens)
    if N == 0:
        return 0
    score = reduce(lambda s,tok: s+WordScore(D,tok), tokens, 0)
    return 100*score/N
def Lower(word):
    try:
        return word.lower()
    except:
        return word
def Load(obj_pickle):
    """
    Load pickle file for obj and return obj
    """
    if os.path.isfile(obj_pickle):
        obj = pickle.load(open(obj_pickle,"rb"))
        return obj
    else:
        return None
    return obj
def Save(obj, obj_pickle):
    """
    Save obj to pickle files
    """
    pickle.dump(obj,open(obj_pickle,"wb") )
    return

def EssayText(fn):
    try:
         f = open(fn,'r')
         text = f.read()
         f.close()
    except:
         return "Error"
    return text
def EssayScore(D,fn):
    text = EssayText(fn)
    return TextScore(D,text)

index_pickle = r'C:\_JGE_VSM\Z_Pickles\index.p'
filelst_pickle = r'C:\_JGE_VSM\Z_Pickles\filelst.p'
essayscore_pickle = r'C:\_JGE_VSM\Z_Pickles\essayscore.p'

index = Load(index_pickle)
L = Load(filelst_pickle)

words = words.words()
words = list(map(Lower,words))
words = words + list('.;,!?\"\'-\n')
D = WordDict(words)

L2 = Load(essayscore_pickle)
if L2 is None:
    L2 = []
    for i in range(len(L)):
        fn = L[i]
        score = EssayScore(D,fn)
        tup = (score,i,fn)
        L2.append(tup)
    L2.sort(key=lambda tup: tup[0])
    L2.reverse()
    Save(L2,essayscore_pickle)

ES = L2
