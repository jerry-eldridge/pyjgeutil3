import indexer as idxr

def Index():
    idxr.index,idxr.L = idxr.IndexCorpora(idxr.corpora,idxr.index,idxr.L)
    K = 50000
    #vocab = map(lambda i: index.keys()[i],random.sample(range(len(index.keys())), K))
    idxr.vocab = list(idxr.index.keys())

    #Search("function type curry polynomial", index, L, 10)

    print("word count: ",idxr.WordCount(idxr.corpora))

    n = 0
    for corpus in idxr.corpora:
        L0 = idxr.DirList(corpus)
        n += len(L0)
    print("number of documents: ",n)
    print("vocabulary count: ", len(list(idxr.index.keys())))
    return

Index()


