import matrix
import LU

import random

def RndMat(n):
    A = matrix.Mat([[]]).zero(n,n)
    for j in range(n):
        for i in range(n):
            v = random.uniform(-1,1)
            A.s(i,j,v)
    return A

A = matrix.Mat([[1,2,3],[3,2,1],[4,2,1]])
b = matrix.Mat([[1,2,3]]).transpose()
Tol = 1e-8
x = LU.solve(A,b)
print("A = ",A)
print("b = ",b)
print("x = LUPSolve(A,b) =",x)
print("A.dot(x)=",A.dot(x))
B = LU.inv(A)
print("B = LUPInvert(A) = ",B)
print("A.dot(B) = ",A.dot(B))
print("LUPDeterminant(A) =",LU.det(A))
print("A.det() = ", A.det())
A = RndMat(9)
import datetime
print("A = RndMat(9)")
t0 = datetime.datetime.now()
print("LU.det(A) =",LU.det(A))
t1 = datetime.datetime.now()
print("Elapsed time:", (t1-t0).total_seconds()*1000, "ms")
t0 = datetime.datetime.now()
print("A.det() = ", A.det())
t1 = datetime.datetime.now()
print("Elapsed time:", (t1-t0).total_seconds()*1000, "ms")

A = RndMat(7)
print("A = RndMat(7)")
t0 = datetime.datetime.now()
B = LU.inv(A)
print("LU.inv(A):")
t1 = datetime.datetime.now()
print("Elapsed time:", (t1-t0).total_seconds()*1000, "ms")
t0 = datetime.datetime.now()
B = A.inv()
print("A.inv():")
t1 = datetime.datetime.now()
print("Elapsed time:", (t1-t0).total_seconds()*1000, "ms")

