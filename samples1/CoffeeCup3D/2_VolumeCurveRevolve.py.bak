# https://docs.scipy.org/doc/scipy/reference/interpolate.html
from scipy.interpolate import interp1d
from scipy.integrate import quad
import numpy as np

from math import pi

# With x1 -> y1 and x2 -> y2, given x, return y using linear map
def MapTo(x1, y1, x2, y2, x):
    epsilon = 0.0001
    if abs(x2 - x1) > epsilon:
        m = 1.*(y2-y1)/(x2-x1)
    else:
        m = 1
    y = m*(x-x1)+y1
    return y

def f(curve):
    X = map(lambda pt: pt[0], curve)
    Y = map(lambda pt: pt[1], curve)
    ymin = min(Y)
    ymax = max(Y)
    domain = [ymin,ymax]
    g = interp1d(Y,X)
    return g,domain

def RevolveCurve(g,domain):
    x = lambda t: MapTo(0,domain[0],1,domain[-1],t)
    y = lambda t: g(x(t))
    return y

def RevolveCurveVolume(y,domain):
    A = lambda t: pi*(y(t))**2
    dx = (domain[1]-domain[0])
    I = quad(A,0,1)[0]*dx
    return I
    
curve1a = [[406, 388], [441, 384], [469, 378], [489, 363], [506, 347],
       [518, 330], [520, 314], [522, 297], [525, 276], [528, 258],
       [530, 228], [528, 182], [528, 150], [527, 113], [527, 91],
       [532, 73], [540, 68]]
curve1b = [[554, 70], [554, 86], [549, 108],
       [550, 136], [546, 181], [547, 214], [544, 249], [544, 268],
       [538, 281], [540, 288], [539, 300], [531, 312], [532, 329],
       [526, 350], [513, 362], [502, 378], [482, 393], [446, 406],
       [417, 409]]

import matplotlib.pyplot as plt

g_1a,domain_1a = f(curve1a)
g_1b,domain_1b = f(curve1b)
xi = lambda x: MapTo(domain[0],0,domain[-1],1,x)
domain = [max(domain_1a[0],domain_1b[0]),
            min(domain_1a[1],domain_1b[1])]
T = np.arange(0,1,.01)

y1 = RevolveCurve(g_1a,domain)
y2 = RevolveCurve(g_1b,domain)

I1 = RevolveCurveVolume(y1,domain)
I2 = RevolveCurveVolume(y2,domain)
print I1,I2

Y1 = map(y1,T)
Y2 = map(y2,T)
plt.plot(T,Y1)
plt.plot(T,Y2)
plt.show()
