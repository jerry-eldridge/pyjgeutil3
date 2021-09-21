import BST as bst

import numpy as np

import random

random.seed(1237987234)

dist = lambda A,B: np.linalg.norm(np.array(A)-np.array(B))

def BST_LT(A,B):
    flag1 = A[1] > B[1]
    flag2 = A[1] == B[1] and A[0] < B[0]
    flag = flag1 or flag2
    return flag

def BST_EQ(A,B):
    epsilon = 1e-8
    flag = dist(A,B) < epsilon
    return flag

def BST_NULL():
    key = [0,0]
    value = None
    x = (key,value)
    return x

bst.BST_LT = BST_LT
bst.BST_EQ = BST_EQ
bst.BST_NULL = BST_NULL

T = bst.BST(key=[0,0],value=None)
N = 5
L = []
for i in range(N):
    xx = int(round(random.uniform(0,100)))
    yy = int(round(random.uniform(0,100)))
    key = [xx,yy]
    value = int(round(random.uniform(0,10)))
    x = (key,value)
    L.append(x)
T = T.build(L)
print("T=",T)
M = T.traverse()
print("T.traverse()=",M)
T.delete([65,15])
M = T.traverse()
print("T.traverse()=",M)
T.clear()
M = T.traverse()
print("T.traverse()=",M)
