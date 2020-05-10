import matrix

from math import sqrt

A = matrix.Mat([[2,4,8],[2,1,5],[-2,6,10]])
print("A=",A)
print("Using cofactor expansion for determinant:")
print("A.det()=",A.det())

A = matrix.Mat([[1,4,7],[3,0,5]])
B = matrix.Mat([[2,4,1],[1,2,3]])
print("A=",A)
print("B=",B)
print("A.shape = ",A.shape)
print("B.shape = ",B.shape)
print("M(n,m) - n x m matrices")
print("A.inner(B) = (B.adj().dot(A)).tr()")
print("A.inner(B) =",A.inner(B))
print("|A-B| = (A-B).norm_inner() =",(A-B).norm_inner())
print("d(A,B) = A.dist(B) = |A-B| =",A.dist(B))
print("abs(A) =",abs(A))
print("abs(B) =",abs(B))
C = matrix.Mat([[1,2],[3,2],[4,5]])
print("C=",C)
print("C.shape = ",C.shape)
D = A.dot(C) # not A * C in implementation!
print("D = A * C = A.dot(C) =",D)
print("4*A = ",4*A)
