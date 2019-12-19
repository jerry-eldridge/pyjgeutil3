import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import LinkageForce as RA
from copy import deepcopy
import graphics_cv as racg
import mapto

from math import fmod,pi,sin,cos
import numpy as np

def PlotGraph(gr,G,color):
    for e in G['E']:
        A,B = map(lambda v: G['pts'][v],e)
        gr.Line(A,B,color)
    for v in G['V']:
        A = G['pts'][v]
        gr.Point(A,color)
    return

l1 = 100
l2 = 90
l3 = 80
theta1 = 0
theta2 = 0
theta3 = 0

L = [l1,l2,l3]
Theta = [theta1,theta2,theta3]
P = RA.RobotArm([0,0,0],deepcopy(L),deepcopy(Theta))

maxiters = 20
goal = deepcopy(P.Start())
epsilon = 0.1
i = 0

w = 600
h = 600
gr = racg.Graphics(w=w,h=h)
P.pt = [w/2,h/2,0]

use_mouse = True
pt_mouse = [0,0,0]
pt_select = [0,0,0]
selected = False
wn = "result"
if use_mouse:
    import cv2
    def getxy(event, x, y, flags, param):
        global pt_mouse,pt_select,selected
        if (event == cv2.EVENT_MOUSEMOVE):
            pt_mouse = [x,y,0]
            return
        if (event == cv2.EVENT_LBUTTONDOWN):
            pt_select = [x,y,0]
            selected = True
            return
    def StartMouse():
        cv2.namedWindow(wn)
        cv2.setMouseCallback(wn,getxy)
        return
    StartMouse()

black = [0,0,0]
blue = [0,0,255]
red = [255,0,0]
t = 0
dt = 1

clamp = lambda lo,hi,x: min(hi,max(lo,x))

class JointAccel:
    def __init__(S,P,dt,DEG=360,MAXSPEED=2):
        S.q = np.array(P.Theta)
        S.J = P.Jacobian(S.q)
        S.P = P
        S.dt = dt
        S.DEG = DEG
        S.MAXSPEED = MAXSPEED
        return
    def Solve_qdd(S,Xdd):
        # Solve for Joint Parameter Accelerations qdd
        S.q_last = S.q.copy()
        S.J_last = S.J.copy()
        S.J = S.P.Jacobian(S.q)
        JI = np.linalg.pinv(S.J)
        S.qd = 1.0*(S.q-S.q_last)/S.dt
        S.Jd = 1.0*(S.J-S.J_last)/S.dt
        val = np.einsum('ij,j->i',S.Jd,S.qd)
        S.qdd = np.einsum('ij,j->i',JI,Xdd-val)
        return S.qdd
    def Solve_q(S,Xdd):
        S.Solve_qdd(Xdd)
        S.qd = S.qd + S.qdd*S.dt # qd Joint Velocity
        S.qd = np.array(map(lambda x: clamp(-S.MAXSPEED,S.MAXSPEED,x),list(S.qd)))
        S.q = S.q + S.qd*S.dt # q Joint Positions
        S.q = np.array(map(lambda x: clamp(-S.DEG/2.0,S.DEG/2.0,fmod(x,360)),list(S.q)))
        return S.q

regular = 180
continuous = 360
JA = JointAccel(P,dt,DEG=regular)#continuous)
Xdd = np.array([0,-5,0])
q = JA.Solve_q(Xdd)
X = np.array(pt_mouse)
X_last = np.array(P.Start())
us = 1 # microsecond
# [1] Wikipedia "Pulse Width Modulation"
# [2] Wikipedia "Servo Control"
# Angle of Servo Motor Joint depends on how long
# a pulse is sent every 50Hz or 20ms. 0 degrees 1500 us
# -90 degrees is 1000 us and 90 degrees is 2000 us.
# YouTube videos have control set by DutyCycle say
# for example between -90 as 2% and +90 as 12% duty cycles
# on Raspberry Pi using an example servo, and via degrees
# with Arduino
DC_lo = 2 # 2 percent duty cycle
DC_hi = 12 # 12 percent duty cycle
T = lambda x: mapto.MapTo(-90,DC_lo,90,DC_hi,clamp(-90,90,x))
while True:
    gr.Clear()
    G = P.Graph()
    PlotGraph(gr,G,black)
    gr.Line(X_last,X,red)
    s = "ServoPWM=[%.2fDC,%.2fDC,%.2fDC]" % tuple(map(T,list(JA.q)))
    gr.Text(s,50,50,blue,scale=.5)
    ch = gr.Show("result",15)
    if ch == ord('e'):
        break

    q = JA.Solve_q(Xdd)
    # Set Robot Arm to Joint Parameters q
    P.Theta = list(q)
    X = np.array(pt_mouse)
    X_last = np.array(P.Start())

    Xdd = .01*(X-X_last)

    t += dt

gr.Close()

