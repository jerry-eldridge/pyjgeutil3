from math import sqrt,acos,cos,pi

d = lambda A,B: np.linalg.norm(np.array(A)-\
                    np.array(B))
clamp = lambda x, a,b: max(a,min(b,x))

def mass(lbs):
     return lbs*0.453592 #kg
def weight(newtons):
     return newtons*0.224808943 # lbs

def doll_weights(lbs, inches):
     g = 9.8
     BW = mass(lbs)*g #body weight in newtons
     # "Biomechanical Basis of Human Movement",Hamill and Knutzen
     # Chandler et al, "Investigation of inertial properties of
     # the human body", AMRL Technical Report, Wright-Patterson
     # Air Force Base, 1975
     dw = {}
     dw["head"] = weight(0.032*BW + 18.70)
     dw["neck"] = .1*dw["head"] # fabricated
     dw["trunk"] = weight(0.532*BW - 6.93)
     dw["R upper arm"] = weight(0.022*BW + 4.76)
     dw["L upper arm"] = weight(0.022*BW + 4.76)
     dw["R arm"] = weight(0.013*BW + 2.41)
     dw["L arm"] = weight(0.013*BW + 2.41)
     dw["R hand"] = weight(0.005*BW + 0.75)
     dw["L hand"] = weight(0.005*BW + 0.75)
     dw["R thigh"] = weight(0.127*BW - 14.82)
     dw["L thigh"] = weight(0.127*BW - 14.82)
     dw["R leg"] = weight(0.044*BW - 1.75)
     dw["L leg"] = weight(0.044*BW - 1.75)
     dw["R foot"] = weight(0.009*BW + 2.48)
     dw["L foot"] = weight(0.009*BW + 2.48)
     H = inches
     l = {}
     # average length using Plagenhoef data
     # "Anatomical data for analyzing human motion",
     # Plagenhoef et al (1983), Research Quarterly for Exercise
     # and Sport 54, 169-178
     l["head"] = 10.75/100.00*H
     l["neck"] = 3.0/100.0*H # fabricated
     l["trunk"] =  29.5/100.00*H
     l["R upper arm"] = 17.25/100.0*H
     l["L upper arm"] = 17.25/100.0*H
     l["R arm"] = 15.85/100.0*H
     l["L arm"] = 15.85/100.0*H
     l["R hand"] = 5.75/100.0*H
     l["L hand"] = 5.75/100.0*H
     l["R thigh"] = 24.05/100.0*H
     l["L thigh"] = 24.05/100.0*H
     l["R leg"] = 25.2/100.0*H
     l["L leg"] = 25.2/100.0*H
     l["R foot"] = 4.25/100.0*H
     l["L foot"] = 4.25/100.0*H

     # these I guessed
     l["L pelvis"] = 15.25/100.0*H
     l["R pelvis"] = 15.25/100.0*H
     l["R shoulder"] = 20.75/100.00*H
     l["L shoulder"] = 20.75/100.00*H
     l["neck"] = 10.75/100.00*H
     return dw, l

def doll_cm():
     cm = {}
     cm["neck"] = 50/100.0
     cm["head"] = 55/100.00
     cm["trunk"] =  59.95/100.00
     cm["R upper arm"] = 44.7/100.0
     cm["L upper arm"] = 44.7/100.0
     cm["R arm"] = 43.2/100.0
     cm["L arm"] = 43.2/100.0
     cm["R hand"] = 46.8/100.0
     cm["L hand"] = 46.8/100.0
     cm["R thigh"] = 43.05/100.0
     cm["L thigh"] = 43.05/100.0
     cm["R leg"] = 42.65/100.0
     cm["L leg"] = 42.65/100.0
     cm["R foot"] = 50/100.0
     cm["L foot"] = 50/100.0
     return cm
