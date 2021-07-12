import scipy.optimize as so
import numpy as np

def Create_A(m,n):
    A = np.zeros((m+n,m*n))
    for i in range(m):
        j = n*i
        A[i,j:j+n] = [1]*n
    I = np.zeros((n,n))
    for i in range(n):
        I[i,i] = 1
    for a in range(m):
        j = a*n
        j2 = (a+1)*n
        A[m:m+n,j:j2] = I
    return A

def Cost(C,X):
    cc = np.array(C,dtype=np.float32).flatten()
    xx = np.array(X,dtype=np.float32).flatten()
    cost = sum(cc*xx)
    return cost

def Optimize_x(m,n,C,X):
    x = np.array(X,dtype=np.float32).reshape(m,n)
    A_eq = Create_A(m,n)
    c = np.array(C,dtype=np.float32).flatten()
    outputs = list(np.sum(x,axis=1).flatten())
    allocations = list(np.sum(x,axis=0).flatten())
    b_eq = outputs + allocations
    res = so.linprog(c,A_eq=A_eq,b_eq=b_eq,
                     bounds=[0,None],
                     method='revised simplex',
                options={'rr':False})
    x_opt = list(res.x)
    return outputs,allocations,x_opt

m = 3 # producers
n = 4 # consumers
# cost to ship from producer i to consumer j
C = [[10,50,60,10],[40,70,10,70],[20,30,40,14]]
print("C = ",C)
# units to ship from producer i to consumer j
X = [[1,6,1,2],[5,1,3,4],[1,4,1,2]]
print("X = ",X)

outputs,allocations,X_opt = Optimize_x(m,n,C,X)
print("outputs=",outputs)
print("allocations=",allocations)
print("X_opt = ",X_opt)
print("="*30)
for i in range(m):
    for j in range(n):
        s = ' cost(producer=%d,consumer=%d) = $%.2f' % (i,j,C[i][j])
        print(s)
print("="*30)
for i in range(m):
    s = ' output(producer=%d) = %.1f' % (i,outputs[i])
    print(s)
for i in range(n):
    s = ' input(consumer=%d) = %.1f' % (i,allocations[i])
    print(s)
print("Initial feasible values:")
for i in range(m):
    for j in range(n):
        s = ' ship(producer=%d,consumer=%d) = %.1f' % (i,j,X[i][j])
        print(s)
print("Cost(C,X) = $%.2f" % Cost(C,X))
print("="*30)
print("Optimized values:")
for i in range(m):
    for j in range(n):
        s = ' ship(producer=%d,consumer=%d) = %.1f' % (i,j,X_opt[j+m*i])
        print(s)
print("Cost(C,X_opt) = $%.2f" % Cost(C,X_opt))
print("="*30)
