import sys
sys.path.insert(0,r"C:\_PythonJGE\Utility")
import graphics_cv as racg
import numpy as np

clamp = lambda x,lo,hi: min(hi,max(lo,x))

# Potential Energy Contour Tracing using Method of Cotterill(PES)
# [1] https://en.wikipedia.org/wiki/Potential_energy_surface
def ShowLevelSet(gr,F,x0,y0,color, tmax=100):
    dx = .1
    dy = .1
    # Partial Derivatives of Gradient
    Gx = lambda F, x0,y0: 1.0*(F(x0+dx,y0)-F(x0,y0))/dx
    Gy = lambda F, x0,y0: 1.0*(F(x0,y0+dy)-F(x0,y0))/dy
    # Gradient of F at (x0,y0)
    grad = lambda F, x0,y0: np.array([Gx(F,x0,y0),Gy(F,x0,y0)])
    v = np.array([100,100]) # initial velocity
    r = np.array([x0,y0]) # initial position
    t = 0
    dt = .1
    r_last = r
    epsilon = .1
    b = 0
    while t <= tmax:
        grad_E = grad(F,r[0],r[1])
        G = np.linalg.norm(grad_E)
        ###############
        # [2] Cotterill, "Biophysics", Potential Energy Contour Tracing
        # suggests updating velocity to follow contours
        # @book{Cotterill02,
        # author = "Cotterill, Rodney",
        # title = "Biophysics: An Introduction, 1st Ed.",
        # publisher = "Wiley",
        # year = "2002"
        # }
        v = v - 1.0*grad_E*np.inner(grad_E,v)/G**2
        ##############
        
        if np.linalg.norm(v) < epsilon:
            break
        # As usual update position based on velocity
        r = r + v*dt
        # lighten color to color0 as particle travels
        # to clean up plot
        color0 = map(lambda x: clamp(x+b,0,255), color)
        gr.Line(list(r_last),list(r),color0)
        t = t + dt
        r_last = r
        b = b + 1
    return
