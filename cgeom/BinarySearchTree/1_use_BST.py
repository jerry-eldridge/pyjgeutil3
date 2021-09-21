import BST as bst

T = bst.BST(key=0,value=65)
T.C[0] = bst.BST(key=1,value=50)
T.C[0].C[1] = bst.BST(key=2,value=60)
T.C[1] = bst.BST(key=3,value=70)
print("T=",T)
min_val = -10000
max_val = 10000
print("T.is_BST(min_val,max_val) = ", T.is_BST(min_val,max_val))
print("Lp = ",T.traverse())
print()

import random
N = 5
L = []
for i in range(N):
    key = int(round(random.uniform(0,100)))
    value = int(round(random.uniform(0,10)))
    x = (key,value)
    L.append(x)
print("L=",L)
T2 = bst.BST()
T2 = T2.build(L)
print("T2 = ", T2)
min_val = -10000
max_val = 10000
print("T2.is_BST(min_val,max_val) = ", T2.is_BST(min_val,max_val))
print("Lp = ",T2.traverse())
T2.clear()
print("T2.clear()")
print("T2 = ", T2)
print("T2.is_BST(min_val,max_val) = ", T2.is_BST(min_val,max_val))
print(T2.traverse())
