import sys
sys.path.insert(0,r"C:\_JGE_VSM")
import indexer as idxr

def Query(query,k=10):
    idxr.Search(query, idxr.index, idxr.L, k)
    return

Query("physics",k=3)
