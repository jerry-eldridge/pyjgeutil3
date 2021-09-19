import os
import fnmatch
import os.path
from nltk.tokenize import wordpunct_tokenize
import pickle as pickle
from math import log,sqrt
import random
from nltk import FreqDist
from datetime import datetime
import time
import re
import sqlite3

def Date2(seconds):
    return datetime.utcfromtimestamp(seconds).strftime('%b %m, %Y')

def Seconds(year,month,day):
    sec = (datetime(year,month,day)-datetime(1970,1,1)).total_seconds()
    return sec

def DirList(fol):
    """
    Directory listing for a folder
    """
    L = []
    for root, dire, files in os.walk(fol):
        for fn in fnmatch.filter(files, "*.txt"):
            try:
                filename = root + '\\' + fn
                L.append(filename)
            except:
                continue
    return L

def LookUp(L, fn):
    """
    Return index of filename fn in filelist L. If not present,
    add it, return possibly updated L and index i.
    """
    for i in range(len(L)):
        if L[i] == fn:
            return L,i
    i = len(L)
    L.append(fn)
    return L,i

def Save(index, index_pickle, L, filelst_pickle):
    """
    Save index and filelist L to pickle files
    """
    print("There are ", len(index), " in index")
    pickle.dump(index,open(index_pickle,"wb") )
    pickle.dump(L,open(filelst_pickle,"wb") )
    return

def Load(index_pickle, filelst_pickle):
    """
    Load pickle files for index and filelist L and return
    index and filelist L
    """
    if os.path.isfile(index_pickle):
        index = pickle.load(open(index_pickle,"rb"))
        L = pickle.load(open(filelst_pickle,"rb"))
        return index, L
    index = {}
    L = []
    return index,L

index_pickle = r'C:\_JGE_VSM\Z_Pickles\index.p'
filelst_pickle = r'C:\_JGE_VSM\Z_Pickles\filelst.p'
index,L = Load(index_pickle, filelst_pickle)

try:
    import define_corpora
    corpora = define_corpora.corpora
except:
    print("Setting corpora to None. You need to define.")
    corpora = None
    print("Create a list of folders containing text .txt files")
    print("to use as the corpora")
    print("""
#Example
corpora = [
    r"C:\_JGE_VSM\corpus1"
    r"C:\_JGE_VSM\corpus2"
    ]
""")

def IndexCorpora(corpora,index,L):
    """
    Index entire corpora of text files located in a folder tree.
    This is relatively quick adding about 80,000
    words for example in a minute or so to index and filenames
    to L.
    """
    for corpus in corpora:
        L0 = DirList(corpus)
        for fn in L0:
            index,L,i = Update(index,L, fn)
            print("|index| = ", len(index), " File ", fn, "indexed.")
        Save(index,index_pickle, L, filelst_pickle)
    return index,L

def Update(index, L, fn):
    """
    Update index and L with filename fn
    """
    L,i = LookUp(L, fn)
    f = open(L[i],'rb')
    btext = f.read()
    text = btext.decode('iso-8859-16')
    f.close()
    tokens = wordpunct_tokenize(text)
    for tok in tokens:
        tok = tok.lower() # make word lowercase
        try:
            index[tok].add(i)
        except:
            index[tok] = set([i])
    return index, L, i

def Docs(word, index, L):
    """
    List of filenames associated with a word
    """
    F = [L[i] for i in list(index[word])]
    return F

def tf(t,d):
    """
    term frequency for term t in document d
    """
    t = t.lower()
    tokens = [word.lower() for word in wordpunct_tokenize(d)]
    return tokens.count(t)

def idf(t, index, L):
    """
    independent document frequency for term t
    """
    t = t.lower()
    try:
        n = len(index[t])
    except:
        n = 1.0
    return log(1.0*len(L)/n)

def weight(t,d, index, L):
    """
    term weight (slow to compute). It would be
    difficult to compute 80,000 possible terms t
    to create a feature vector. For term t in document d.
    Using index and filelist L.
    """
    t = t.lower()
    return tf(t,d)*idf(t,index,L)

def similarity(d,q,vocab,index,L):
    """
    The similarity between document d and query q which
    is typically much shorter. The document the contents
    of the filename for it. Given a vocabulary of words
    vocab making up coordinates in a feature vector.
    The feature vector not computed but only dimensions
    or words in q are checked as the weight for term in q
    would be zero if word not in q. Index and filelist L.
    """
    tokens = [word.lower() for word in wordpunct_tokenize(q)]
    s = 0
    s2 = 0
    for t in set(tokens):
        s = s + weight(t,d,index,L)*weight(t,q,index,L)
        s2 = s2 + weight(t,q,index,L)**2
    tokens = [word.lower() for word in wordpunct_tokenize(d)]
    s3 = 1
##    s3 = 0
##    for t in set(tokens):
##        s3 = s3 + weight(t,d,index,L)**2
    cossim = s/(sqrt(s3)*sqrt(s2))
    return cossim

def Search(q, index, L, k):
    """
    Given index and filelist L, retrieve the closest k documents
    to a query q.
    """
    tokens = [word.lower() for word in wordpunct_tokenize(q)]
    tokens2 = []
    for t in tokens:
        if t in vocab:
            tokens2.append(t)
    tokens = tokens2
    lst = []
    for t in tokens:
        lst = lst + Docs(t, index, L)
    lst = list(set(lst))
    sims = []
    for fn in lst:
        sim = similarity(open(fn,"r").read(),q,index,L,vocab)
        sims.append([fn,sim])
    sims = sorted(sims, key = lambda lst: lst[1])
    sims.reverse()
    k = min(k,len(sims))
    print()
    print(""">>>Search("%s", index, L, %d)""" % (q,k))
    print()
    for i in range(k):
        print(sims[i])
    print()
    for i in range(k):
        tup = sims[i]
        f = open(tup[0],'r')
        (mode, ino, dev, nlink, uid, gid, size, atime, mtime, ctime) = os.stat(tup[0])
        print()
        print("PY"*40)
        print("PY Filename: "+tup[0])
        print("PY last modified: %s" % time.ctime(mtime))
        print("PY created: %s" % time.ctime(ctime))
        print("PY"*40)
        text = f.read()
        f.close()
        print()
        print(text)
    print()
    return

def WordCount(corpora):
    count = 0
    for corpus in corpora:
        L0 = DirList(corpus)
        for fn in L0:
            f = open(fn,'rb')
            btext = f.read()
            text = btext.decode('iso-8859-16')
            f.close()
            tokens = wordpunct_tokenize(text)
            count = count + len(tokens)
    return count

def OpusNumber(i,s):
    val = 'FS. %d' % i
    s = '.*'+s+'.*'
    for tup in opusL:
        try:
            opusno,secs,subj,comment = tup
            secs = int(secs)
            subj = subj.replace('.*','')
            m = re.match(s,subj)
            if not (m is None):
                val = 'Op. %d, %s.' % (opusno,Date2(secs))
                break
        except:
            continue
    return val

def cite(i):
    fn = L[i]
    author = 'Eldridge, J. G.'
    toks = fn.split('\\')
    fn = toks[-1]
    s0 = fn[:-4]
    s = author+', "'+s0+'", Unpublished personal communications. ' + OpusNumber(i,s0)
    return s

vocab = list(index.keys())

opus_pickle = "C:\_JGE_VSM\Z_Pickles\opus_numbers.p"
if os.path.isfile(opus_pickle):
    opusL = pickle.load(open(opus_pickle,"rb"))
else:
    opusL = []

def CreateBiblio(fn_biblio):
    print("Writing to ",fn_biblio)
    f = open(fn_biblio,'w')
    n = len(L)
    print("On rare occasions some reference links may be by another author")
    for i in range(n):
        fsno = i
        subj = L[i][:-4]
        opusno = OpusNumber(i,subj)
        s = "[%d] %s" % (i+1,cite(i))
        print(s)
        f.write(s+'\n')
    print("On rare occasions some reference links may be by another author")
    f.close()
    return

