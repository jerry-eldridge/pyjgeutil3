from . import affine as aff

import numpy as np
from copy import deepcopy

class CoordSystem():
    def __init__(self):
        self.L = []
        return
    def forward(self, shape_in):
        shape_out = shape_in
        for k in range(len(self.L)):
            Lk = self.L[k]
            if Lk[0]=="translate":
                t = Lk[1]
                shape_out = aff.Translate(shape_out,t[0],t[1],t[2],align=False)
            elif Lk[0]=="scale":
                s = Lk[1]
                shape_out = aff.Scale(shape_out,s[0],s[1],s[2],align=False)
            elif Lk[0]=="rotate":
                q = Lk[1]
                shape_out = aff.Rotate(shape_out,q,align=False)
            elif Lk[0]=="transform3x3":
                T = Lk[1]
                shape_out = aff.Transform(shape_out,T)
        return shape_out
    def backward(self, shape_out):
        shape_in = shape_out
        for k in range(len(self.L)-1,-1,-1):
            Lk = self.L[k]
            if Lk[0]=="translate":
                t = Lk[1]
                ti = [-t[0],-t[1],-t[2]]
                shape_in = aff.Translate(shape_in,ti[0],ti[1],ti[2],align=False)
            elif Lk[0]=="scale":
                s = Lk[1]
                si = [1./s[0],1./s[1],1./s[2]]
                shape_in = aff.Scale(shape_in,si[0],si[1],si[2],align=False)
            elif Lk[0]=="rotate":
                q = Lk[1]
                qi = q.inv()
                shape_in = aff.Rotate(shape_in,qi,align=False)
            elif Lk[0]=="transform3x3":
                T = Lk[1]
                epsilon = 1e-3
                if abs(np.linalg.det(T)) > epsilon:
                    Ti = np.linalg.inv(T)
                else:
                    print("Error: singular transform3x3")
                    Ti = np.identity(3)
                shape_in = aff.Transform(shape_in,Ti)
        return shape_in
    def SetOrigin(self,O):
        typ = "translate"
        t = [-O[0],-O[1],-O[2]]
        tup = (typ,t)
        self.L.append(tup)
        self.Compress()
        return
    def Locus(self,O):
        A = self.forward([O])[0]
        return A
    def Translate(self,t):
        typ = "translate"
        tup = (typ,t)
        self.L.append(tup)
        self.Compress()
        return
    def Scale(self,s):
        typ = "scale"
        tup = (typ,s)
        self.L.append(tup)
        self.Compress()
        return
    def Rotate(self,q):
        typ = "rotate"
        tup = (typ,q)
        self.L.append(tup)
        self.Compress()
        return
    def Transform3x3(self,T):
        typ = "transform3x3"
        T2 = np.identity(4)
        T2[:3,:3] = T
        tup = (typ,T2)
        self.L.append(tup)
        self.Compress()
        return
    def Compare(self,tup1,tup2):
        if (tup1[0]==tup2[0]):
            if tup1[0]=="translate":
                typ = "translate"
                t1 = tup1[1]
                t2 = tup2[1]
                # vector sum
                t = list(np.array(t1)+np.array(t2))
                tup = (typ,t)
                flag = True
        if (tup1[0]==tup2[0]):
            if tup1[0]=="scale":
                typ = "scale"
                s1 = tup1[1]
                s2 = tup2[1]
                # hadamard product
                s = list(np.array(s1)*np.array(s2))
                tup = (typ,s)
                flag = True
        if (tup1[0]==tup2[0]):
            if tup1[0]=="rotate":
                typ = "rotate"
                q1 = tup1[1]
                q2 = tup2[1]
                # hadamard product
                q = q2*q1
                tup = (typ,q)
                flag = True
        if (tup1[0]==tup2[0]):
            if tup1[0]=="transform3x3":
                typ = "transform3x3"
                T1 = tup1[1]
                T2 = tup2[1]
                # hadamard product
                T = np.einsum('ij,jk->i,k',T2,T1)
                tup = (typ,T)
                flag = True
        if (tup1[0] != tup2[0]):
            tup = tup2
            flag = False
        return flag,tup
        
    def CompressHelper(self):
        L = deepcopy(self.L)
        if len(L) < 2:
            return
        L2 = [L[0]]
        for i in range(1,len(L)):
            tup1 = L2[-1]
            tup2 = L[i]
            flag,tup = self.Compare(tup1,tup2)
            if flag:
                L2[-1]=tup
            else:
                L2.append(tup)
        self.L = L2
        return
    def Compress(self,N=10):
        for i in range(N):
            self.CompressHelper()
        return

def Compose(CS_L):
    CS = CoordSystem()
    CS.L = []
    for CSk in CS_L:
        CS.L = CS.L + CSk.L
    CS.Compress()
    return CS

class CoordSystemPath:
    def __init__(self,O=[0,0,0]):
        self.CS_L = []
        self.Push(O=O,t=O)
        return
    def Push_TRS(self,O=[0,0,0],
            T = [0,0,0],
            R = [0,0,0],
            S = [1,1,1],
            basis=np.identity(3)):
        self.Push(O,S,
                  aff.HH.FromEuler(*R),
                  T,
                  basis)
        return
    def Push(self,O=[0,0,0],s=[1.,1.,1.],
          q=aff.HH.Quaternion([1,0,0,0]),
          t=[0,0,0],basis=np.identity(3)):
        CS2 = CoordSystem() 
        CS2.SetOrigin(O)
        CS2.Translate(t)
        CS2.Scale(s)
        CS2.Rotate(q)
        CS2.Translate(O)
        self.CS_L.append(CS2)
        return
    def Pop(self):
        CS = self.CS_L[-1]
        self.CS_L = self.CS_L[:-1]
        return CS
    def FK(self,O): # forward kinematics
        pt = Compose(self.CS_L).Locus(O)
        pt = list(map(float, list(pt)))
        return pt
    def Locus(self,O): # locus of end effector
        return self.FK(O)

def Rotation(deg=0,axis=[0,0,1]):
    ax = axis
    q = aff.HH.rotation_quaternion(deg,ax[0],ax[1],ax[2])
    return q
