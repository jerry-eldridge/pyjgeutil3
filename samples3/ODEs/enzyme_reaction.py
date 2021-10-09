import solve_ode_system as odes

import numpy as np

class EnzymeR:
    def __init__(self,kf,kr,kcat,E,S,ES,P,dt):
        # dy/dt = f(t,y)
        self.kf = kf
        self.kr = kr
        self.kcat = kcat
        self.dt = dt
        self.E = E
        self.S = S
        self.ES = ES
        self.P = P
        self.y0 = np.array([E,S,ES,P]) # E S ES P
    def f(self,t,y):
        kf = self.kf
        kr = self.kr
        kcat = self.kcat
        E,S,ES,P = list(y)
        e = (-kf*E*S + kr*ES + kcat*ES)
        s = (-kf*E*S + kr*ES)
        es = (kf*E*S - kr*ES - kcat*ES)
        p = kcat*ES
        dydt = np.array([e,s,es,p])
        return dydt
    def sim(self,tmin,tmax,name="Euler"):
        T,Y = odes.Solve(self.f,tmin,tmax,self.dt,
                    self.y0,name)
        return T,Y
