#import sys
#sys.path.insert(0,r"C:\_PythonJGE\Utility3")
import graphics_cv as racg
from copy import deepcopy

from functools import reduce

from math import cos,sin,pi,fmod

# [1] https://en.wikipedia.org/wiki/L-system
# Sierpinski arrowhead curve
def apply_rule(s,LHS,RHS):
    L = s.split(LHS)
    s2 = RHS
    s3 = s2.join(L)
    return s3

def r(s):
    s2 = apply_rule(s,"A","B-[A-B]")
    s3 = apply_rule(s2,"B","A+[B-A]")
    return s3

def S(i):
    def f(s):
        val = reduce(lambda n,m: r(n), range(i), s)
        return val
    return f


def draw(gr,s,color=[0,0,255]):
    gr.Clear()
    S = []
    pos = [50,gr.h/2]
    heading = 0
    angle = 26
    r = 20
    for i in range(len(s)):
        c = s[i]
        if c in ["A","B"]:
            theta = heading*pi/180.
            xx = pos[0] + r*cos(theta)
            yy = pos[1] + r*sin(theta)
            B = [xx,yy]
            A = [int(xx),int(yy)]
            gr.Line(pos,A,color,thickness=1)
            pos = deepcopy(B)
        elif c == '-':
            heading = fmod(heading+angle,360)
        elif c == '+':
            heading = fmod(heading-angle,360)
        elif c == '[':
            S.append((pos,heading))
        elif c == ']':
            val = S[-1]
            S = S[:-1]
            pt,theta = val
            pos = deepcopy(pt)
            heading = theta
        else:
            continue
    return

w,h = 500,500
gr = racg.Graphics(w=w,h=h)
s = 'A'
draw(gr,S(5)(s))
gr.Show("result",-1)
gr.Save("Fractal_plant_20220418-3.jpg")
gr.Close()
