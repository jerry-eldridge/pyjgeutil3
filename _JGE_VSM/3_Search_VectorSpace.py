import sys
sys.path.insert(0,r"C:\_JGE_VSM")
import indexer as idxr

def Query(query,k=10):
    idxr.Search(query, idxr.index, idxr.L, k)
    return

def Search():
    done = False
    while not done:
        print("type 'quit' to quit.")
        query = input("query> ")
        if query == "quit":
            done = True
            break
        else:
            try:
                Query(query, k = 3)
            except:
                continue
    return

Search()
#Query("physics",k=3)
