import numpy as np
from copy import deepcopy

class MDP:
    def __init__(self,start,S,V0,X,gamma=.1):
        self.s_current = start
        self.S = S # list of states S
        self.V = np.array(V0) # V(s) value function for each state s
        self.X = deepcopy(X)
        self.A = range(len(X)) # set of actions indices ia
        self.P0 = zip(self.A,map(lambda L: L[1],X))
        self.R0 = zip(self.A,map(lambda L: L[2],X))
        self.gamma = gamma # discount constant
        return
    def GetState(self):
        return self.s_current
    def SetState(self,s):
        self.s_current = s
        return
    def E(self,tup):
        def f(s):
            if s == tup[0]:
                return tup[1]
            else:
                return s
        return f
    def P(self,ia,s1,s2):
        """
        P(ia,s1,s2) - Probability of action index ia, state s1 to s2
        """
        tup = self.X[ia]
        if (s1,s2) == tup[0]:
            return tup[1]
        return 0
    def R(self,ia,s1,s2):
        """
        R(ia,s1,s2) - Reward of action index ia, state s1 to s2
        """
        tup = self.X[ia]
        if (s1,s2) == tup[0]:
            return tup[2]
        return 0
    def Q(self,s1,ia):
        """
        Q(s1,ia) a real value for action index ia and state s1 
        """            
        q = 0
        for s2 in self.S:
            val = self.P(ia,s1,s2)*(self.R(ia,s1,s2)+self.gamma*self.V[s2])
            q += val
        return q
    def pi(self,s1):
        """
        pi(s1) - policy returning ia the action index to act at state s1
        """
        Q_s1 = map(lambda ia: self.Q(s1,ia), self.A)
        ia = np.argmax(Q_s1)
        return ia
    def UpdateV(self,s):
        """
        UpdateV(s) - updates values V(s) for state s
        """
        self.V[s] = self.Q(s,self.pi(s))
        return
    def policy(self,s):
        """
        a = policy(s) is a action function such that s2 = a(s) is next state
        """
        ia = self.pi(s)
        a = self.E(self.X[ia][0])
        return a
    def GetV(self):
        """
        GetV() - returns array of values V index by state s
        """
        return self.V
    def GetQ(self,s):
        """
        GetQ(s) - returns array of values Q(s) index by action index ia
        """
        Q_s = map(lambda ia: self.Q(s,ia), self.A)
        return Q_s
    def Decide(self,s):
        """
        Decide() - for current state self.s_current, this
        will create a policy returning an action, update the values,
        and find next state, making self.s_current that next state.
        It makes a decision and acts upon it using information
        of self.X of edges,probabilities,rewards.
        """
        a = self.policy(s)
        s2 = a(s)
        return s2
    def MakeMove(self):
        s = self.GetState()
        s2 = self.Decide(s)
        self.UpdateV(s)
        self.SetState(s2)
        return s2
    def Get_r(self,ia):
        """
        Get_r(ia) - from self.X[ia] get r reward
        """
        tup = self.X[ia]
        e,p,r = tup
        s1,s2 = e
        return r
    def Get_e(self,ia):
        """
        Get_e(ia) - from self.X[ia] get e edge
        """
        tup = self.X[ia]
        e,p,r = tup
        s1,s2 = e
        return e
    def Get_p(self,ia):
        """
        Get_p(ia) - from self.X[ia] get p probability
        """
        tup = self.X[ia]
        e,p,r = tup
        s1,s2 = e
        return p
    def Set_r(self,ia,r):
        """
        Set_r(ia) - from self.X[ia] set r reward
        """
        self.X[ia][2]=r
        return
    def Set_p(self,ia,p):
        """
        Set_p(ia) - from self.X[ia] get p probability
        """
        self.X[ia][1]=p
        return
