import sys
sys.path.insert(0,r"C:\_JGE_VSM")
import a2_EnglishScore as es

def S(word):
    try:
        return set(list(es.index[word]))
    except:
        return set([])
def And(S1,S2):
    return S1.intersection(S2)
def Or(S1,S2):
    return S1.union(S2)
def Minus(S1,S2):
    return S1.difference(S2)
def Retr(i):
    txt = es.EssayText(es.L[i])
    return txt

T = And(And(S("solid"),S("state")),S("physics"))
T= And(S("iis"),S("php"))
print(T)

for i in list(T):
    print("@"*40)
    print(Retr(i))
    print("@!"*20)
    fn = es.L[i]
    score = es.EssayScore(es.D,fn)
    tup = (score,i,fn)
    print(tup)
    print("@"*40)
