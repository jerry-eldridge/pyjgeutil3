from . import CoordSystem as cs
from . import doll
from . import affine as aff
from . import QuaternionGroup as cog

import numpy as np
from copy import deepcopy

def lerp(A,B,t):
    C = aff.lerp(np.array(A),np.array(B),t)
    C = list(map(float,C))
    return C

##       |y
##       |
##       
##       o
##      ---
##       |
##      / \
##       ---------x
##      /O
##     /
##    /z

## T = [tx,ty,tz], S = [sx,sy,sz], R = [rx,ry,rz]

def ps(pt):
    s = f"[{pt[0]:.3f},{pt[1]:.3f}, {pt[2]:.3f}]"
    return s

class HumanDoll:
    def __init__(self,O,weight_lbs,height_in):
        self.O = deepcopy(O)
        self.lbs = weight_lbs
        self.height = height_in
        self.dw,self.l = \
            doll.doll_weights(weight_lbs,height_in)
        self.cm = doll.doll_cm()
        self.effectors = [
            "head effector",
            "L hand effector",
            "R hand effector",
            "L foot effector",
            "R foot effector"]
        for key in self.effectors:
            self.l[key] = 0.0001
            self.cm[key] = 0.5
            self.dw[key] = 0.00001
        self.l[key] = 0.01
        self.CSPs = {}
        self.OTRS = {}
        self.E = [
         ["hip","trunk"],
         ["trunk","neck"],["neck","head"],
         ["head","head effector"],
         ["trunk","L upper arm"],["L upper arm","L arm"],
         ["L arm","L hand"],
         ["L hand","L hand effector"],
         ["trunk","R upper arm"],["R upper arm","R arm"],
         ["R arm","R hand"],
         ["R hand","R hand effector"],
         ["hip","L waist"],
         ["L waist","L thigh"],
         ["L thigh","L leg"],
         ["L leg","L foot"],
         ["L foot","L foot effector"],
         ["hip","R waist"],
         ["R waist","R thigh"],
         ["R thigh","R leg"],
         ["R leg","R foot"],
         ["R foot","R foot effector"],
         ]
        self.l["hip"] = 0.0001
        self.dw["hip"] = 0.00001
        self.cm["hip"] = 0.5
        self._pts = {}
    def add_path(self,name,O,T,R,S):
        K = list(self.CSPs.keys())
        if name in K:
            self.CSPs[name].Push_TRS(O,T,R,S)
            self.OTRS[name].append([O,T,R,S])
        else:
            CSP = cs.CoordSystemPath()
            CSP.Push_TRS(O,T,R,S)
            self.CSPs[name] = CSP
            self.OTRS[name] = [[O,T,R,S]]
    def forward(self,name, shape_in):
        shape_out = self.CSPs[name].forward(shape_in)
        return shape_out
    def bbox(self):
        parts = list(self.CSPs.keys())
        segments = {}
        pts = []
        for name in parts:
            for i in range(len(self.OTRS[name])):
                A = self.OTRS[name][i][0]
                B = self.CSPs[name].Locus(A)
                M = lerp(A,B,0.5)
                CM = lerp(A,B,self.cm[name])
                pts.append(A)
                pts.append(B)
                segment = [A,M,B,CM]
                segments[(name,i)] = segment
        P = np.array(pts)
        Pmin = np.min(P,axis=0)
        Pmax = np.max(P,axis=0)
        dims1 = Pmax - Pmin                
        return dims1
    def build(self,kind="human"):
        if kind == "human":
            self._pts = {}
            # build trunk
            name = "hip"
            O_hip = deepcopy(self.O)
            self._pts["O_hip"] = O_hip
            T1 = [0,self.l[name],0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_hip,T1,R1,S1)
            O_trunk = self.CSPs[name].Locus(O_hip)
            self._pts["O_shoulder"] = O_trunk

            name = "trunk"
            T1 = [0,self.l[name],0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_trunk,T1,R1,S1)
            O_shoulder = self.CSPs[name].Locus(O_trunk)
            self._pts["O_shoulder"] = O_shoulder            

            name = "neck"
            T1 = [0,self.l[name],0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_shoulder,T1,R1,S1)
            O_bottom_of_head = \
                    self.CSPs[name].Locus(O_shoulder)
            self._pts["O_bottom_of_head"] =\
                O_bottom_of_head

            name = "head"
            T1 = [0,self.l[name],0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_bottom_of_head,T1,R1,S1)
            O_top_of_head = \
                    self.CSPs[name].Locus(\
                        O_bottom_of_head)
            self._pts["O_top_of_head"] =\
                O_top_of_head

            name = "head effector"
            T1 = [0,self.l[name],0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_top_of_head,T1,R1,S1)
            O_head_effector = \
                    self.CSPs[name].Locus(\
                        O_top_of_head)
            self._pts["O_head_effector"] =\
                O_head_effector

            name = "L upper arm"
            w_shoulder = 18 # inch
            O_L_upper_arm = \
                np.array([w_shoulder/2.0,0,0])+\
                np.array(O_shoulder)
            self._pts["O_L_upper_arm"] =\
                O_L_upper_arm
            O_L_upper_arm = \
                list(map(float,list(O_L_upper_arm)))
            T1 = [self.l[name],0,0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_L_upper_arm,T1,R1,S1)
            O_L_lower_arm = \
                    self.CSPs[name].Locus(O_L_upper_arm)
            self._pts["O_L_lower_arm"] =\
                O_L_lower_arm

            name = "L arm"
            T1 = [self.l[name],0,0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_L_lower_arm,T1,R1,S1)
            O_L_hand = \
                    self.CSPs[name].Locus(O_L_lower_arm)
            self._pts["O_L_hand"] = O_L_hand

            name = "L hand"
            T1 = [self.l[name],0,0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_L_hand,T1,R1,S1)
            O_L_hand_effector = \
                    self.CSPs[name].Locus(O_L_hand)
            self._pts["O_L_hand_effector"] = \
                O_L_hand_effector

            name = "L hand effector"
            T1 = [self.l[name],0,0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_L_hand_effector,T1,R1,S1)
            O_L_hand_effector2 = \
                    self.CSPs[name].Locus(O_L_hand_effector)
            self._pts["O_L_hand_effector2"] = \
                O_L_hand_effector2
            
            name = "R upper arm"
            w_shoulder = 18 # inch
            O_R_upper_arm = \
                np.array([-w_shoulder/2.0,0,0])+\
                np.array(O_shoulder)
            O_R_upper_arm = \
                list(map(float,list(O_R_upper_arm)))
            self._pts["O_R_upper_arm"] = \
                O_R_upper_arm
            T1 = [-self.l[name],0,0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_R_upper_arm,T1,R1,S1)
            O_R_lower_arm = \
                    self.CSPs[name].Locus(O_R_upper_arm)
            self._pts["O_R_lower_arm"] = \
                O_R_lower_arm

            name = "R arm"
            T1 = [-self.l[name],0,0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_R_lower_arm,T1,R1,S1)
            O_R_hand = \
                    self.CSPs[name].Locus(O_R_lower_arm)
            self._pts["O_R_hand"] = O_R_hand

            name = "R hand"
            T1 = [-self.l[name],0,0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_R_hand,T1,R1,S1)
            O_R_hand_effector = \
                    self.CSPs[name].Locus(O_R_hand)
            self._pts["O_R_hand_effector"] = \
                O_R_hand_effector

            name = "R hand effector"
            T1 = [-self.l[name],0,0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_R_hand_effector,T1,R1,S1)
            O_R_hand_effector2 = \
                    self.CSPs[name].Locus(O_R_hand_effector)
            self._pts["O_R_hand_effector2"] = \
                O_R_hand_effector2

            name = "L waist"
            #print(f"L_waist: O_hip = {O_hip}")
            w_hip = 12 # inches
            self.l[name] = w_hip/2.0
            self.cm[name] = 0.5
            self.dw[name] = .01
            T1 = [self.l[name],0,0]
            T1 = list(map(float,list(T1)))
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_hip,T1,R1,S1)
            O_L_waist = \
                    self.CSPs[name].Locus(O_hip)
            #print(f"L_waist: O_L_waist = {O_L_waist}")
            self._pts["O_L_waist"] = \
                O_L_waist

            name = "L thigh"
            T1 = [0,-self.l[name],0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_L_waist,T1,R1,S1)
            O_L_leg = \
                    self.CSPs[name].Locus(O_L_waist)
            self._pts["O_L_leg"] = \
                O_L_leg
            
            name = "L leg"
            T1 = [0,-self.l[name],0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_L_leg,T1,R1,S1)
            O_L_foot = \
                    self.CSPs[name].Locus(O_L_leg)
            self._pts["O_L_foot"] = \
                O_L_foot

            name = "L foot"
            T1 = [0,0,self.l[name]]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_L_foot,T1,R1,S1)
            O_L_foot_effector = \
                    self.CSPs[name].Locus(O_L_foot)
            self._pts["O_L_foot_effector"] = \
                O_L_foot_effector

            name = "L foot effector"
            T1 = [0,0,self.l[name]]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_L_foot_effector,T1,R1,S1)
            O_L_foot_effector2 = \
                    self.CSPs[name].Locus(O_L_foot_effector)
            self._pts["O_L_foot_effector2"] = \
                O_L_foot_effector2

            name = "R waist"
            w_hip = 12 # inches
            self.l[name] = w_hip/2.0
            self.cm[name] = 0.5
            self.dw[name] = 0.01
            T1 = [-self.l[name],0,0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_hip,T1,R1,S1)
            O_R_waist = \
                    self.CSPs[name].Locus(O_hip)
            self._pts["O_R_waist"] = \
                O_R_waist

            name = "R thigh"
            T1 = [0,-self.l[name],0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_R_waist,T1,R1,S1)
            O_R_leg = \
                    self.CSPs[name].Locus(O_R_waist)
            self._pts["O_R_leg"] = \
                O_R_leg

            name = "R leg"
            T1 = [0,-self.l[name],0]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_R_leg,T1,R1,S1)
            O_R_foot = \
                    self.CSPs[name].Locus(O_R_leg)
            self._pts["O_R_foot"] = \
                O_R_foot

            name = "R foot"
            T1 = [0,0,self.l[name]]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_R_foot,T1,R1,S1)
            O_R_foot_effector = \
                    self.CSPs[name].Locus(O_R_foot)
            self._pts["O_R_foot_effector"] = \
                O_R_foot_effector

            name = "R foot effector"
            T1 = [0,0,self.l[name]]
            R1 = [0,0,0]
            S1 = [1,1,1]
            self.add_path(name,O_R_foot_effector,T1,R1,S1)
            O_R_foot_effector2 = \
                    self.CSPs[name].Locus(O_R_foot_effector)
            self._pts["O_R_foot_effector2"] = \
                O_R_foot_effector2
            
        else:
            print(f"kind must be set to 'human'")
        return
    def pose_helper(self): # input edges
        for e in self.E:
            u,v = e
            F = self.OTRS[u]
            O,T,R,S = F[0]
            for idx in range(len(F)):
                F_idx = F[idx]
                _,T,R,S = F_idx
                self.change(e,idx,O,T,R,S)
                O = self.CSPs[u].Locus(O)
        return
    def pose(self,e,idx,Oi=None,T=None,R=None,S=None):
        self.change(e,idx,Oi,T,R,S)
        self.pose_helper()
        return
    def change(self,e,idx,Oi=None,T=None,R=None,S=None):
        u,v = e
        OTRS1 = deepcopy(self.OTRS[u])
        
        self.OTRS[u] = []
        self.CSPs[u] = cs.CoordSystemPath()
        if len(OTRS1) == 0:
            return

        if Oi is None:
            Oi = OTRS1[0][0]

        q = cog.rotation_quaternion(0,0,0,1)
        for i in range(len(OTRS1)):
            _,Ti,Ri,Si = OTRS1[i]
            if i == idx:
                if T is not None:
                    Ti = deepcopy(T)
                if R is not None:
                    Ri = deepcopy(R)
                if S is not None:
                    Si = deepcopy(S)
            q = cog.FromEuler(*Ri) * q
            #Ri = q.ToEuler()
            self.add_path(u,Oi,Ti,Ri,Si)
            Oi = self.CSPs[u].Locus(Oi)
        O,T,R,S = self.OTRS[v][0]
        self.OTRS[v][0] = [Oi,T,R,S]
        return
    def get_segments(self):
        parts = list(self.CSPs.keys())
        segments = {}
        for name in parts:
            for i in range(len(self.OTRS[name])):
                A = self.OTRS[name][i][0]
                B = self.CSPs[name].Locus(A)
                M = lerp(A,B,0.5)
                CM = lerp(A,B,self.cm[name])
                segment = [A,M,B,CM]
                segments[(name,i)] = segment
        return segments
    def center_of_mass_segment(self, name, idx):
        segments = self.get_segments()
        A,M,B,CM = segments[(name,idx)]
        return A,M,B,CM
    def center_of_mass(self):
        segments = self.get_segments()
        K = list(segments.keys())
        x_CM = np.array([0,0,0])
        total_mass = 0
        if len(K) == 0:
            total_mass = 1
        for key in K:
            segment = segments[key]
            A,M,B,CM = segment
            name,i = key
            mass = self.dw[name]
            xi = np.array(CM)
            total_mass = total_mass + mass
            x_CM = x_CM + xi*mass
        x_CM = x_CM/total_mass
        x_CM = list(map(float,list(x_CM)))
        return x_CM
    def __str__(self):        
        s = 'HumanDoll:\n'
        segments = self.get_segments()
        K = list(segments.keys())
        for key in K:
            segment = segments[key]
            A,M,B,CM = segment
            name,i = key
            t = f" x_proximal: {ps(A)}"+\
                f" x_cm: {ps(CM)}"+\
                f" x_distal: {ps(B)}"
            s = s + f'  {name}.{i}: {t}\n'
        x_CM = self.center_of_mass()
        s = s + f"  HumanDoll Center of Mass: "+\
                f"  x_CM = {ps(x_CM)}\n"
        s = s + f"  bbox: {self.bbox()}\n"
        return s
    def display(self,f):
        s = str(self)
        lines = s.split('\n')
        for line in lines:
            f.write(line+"\n")
        return        
    def __repr__(self):
        return str(self)

##       |y
##       |
##       
##       o
##      ---
##       |
##      / \
##       ---------x
##      /O
##     /
##    /z

## T = [tx,ty,tz], S = [sx,sy,sz], R = [rx,ry,rz]

