import sympy

import numpy as np

def pyBezier4(pts):
	import sympy
	import numpy as np
	def f(t):
	    M = sympy.Matrix(np.array([
            [-1, 3, -3, 1],
            [3, -6, 3, 0],
            [-3, 3, 0, 0],
            [1, 0, 0, 0]]))
	    Mt = sympy.Matrix(np.array([t*t*t, t*t, t, 1])).T
	    MP1 = sympy.Matrix(np.array(map(lambda pt: pt[0], pts)))
	    MP2 = sympy.Matrix(np.array(map(lambda pt: pt[1], pts)))
	    Mb = M*MP1
	    x = Mt*Mb
	    Mb = M*MP2
	    y = Mt*Mb
	    pt = [x[0],y[0]]
	    return pt
	return f

def line(A,B):
        def f(t):
             x = A[0]*(1-t) + B[0]*t
             y = A[1]*(1-t) + B[1]*t
             pt = [x,y]
             return pt
        return f

def pyBezier(pts,s,t):
        n = len(pts)
        A = [0,   0]
        B = [1, n-1]
        i = int(line(A,B)(s)[1])
        if i >= 2:
                i = i - 2
        if i+4 > n-1:
                i = (n-1) - 4
        pts4 = pts[i:i+4]
        f = pyBezier4(pts4)
        return f(t)
                

pts_head = [[334, 57], [266, 58], [193, 64], [156, 88],
       [124, 118], [116, 145], [115, 180], [140, 183],
       [143, 197], [137, 209], [133, 218], [123, 241],
       [107, 264], [86, 295], [60, 330], [61, 354],
       [68, 372], [90, 376], [117, 379], [137, 380],
       [149, 373], [149, 357], [164, 352], [165, 364],
       [166, 379], [162, 390], [160, 402], [159, 408],
       [147, 414], [147, 423], [159, 426], [170, 428],
       [182, 426], [191, 433], [174, 444], [168, 445],
       [159, 448], [153, 455], [159, 461], [165, 464],
       [172, 472], [174, 484], [178, 500], [181, 517],
       [187, 533], [204, 547], [230, 552], [255, 553],
       [301, 552], [353, 542], [399, 527], [427, 492],
       [435, 460], [438, 449], [451, 470], [452, 497],
       [456, 523], [457, 543], [460, 564], [481, 568],
       [511, 562], [545, 547], [570, 520], [587, 474],
       [592, 428], [594, 404], [585, 385], [541, 366],
       [503, 366], [466, 368], [447, 362], [433, 324],
       [441, 265], [467, 201], [493, 149], [482, 96],
       [428, 70], [375, 62], [321, 61], [280, 56],
       [280, 57], [281, 58]]

t = sympy.symbols('t') # symbol
s = .2 # value in interval [0,1]
print "s = ",s
p = pyBezier(pts_head,s,s)
q = pyBezier(pts_head,s,t)
print "p(s) = pyBezier(pts_head,s,s) = ",p
print "p(t) = pyBezier(pts_head,s,t) = ",q
s = .6 # value in interval [0,1]
print "s = ",s
p = pyBezier(pts_head,s,s)
q = pyBezier(pts_head,s,t)
print "p(s) = pyBezier(pts_head,s,s) = ",p
print "p(t) = pyBezier(pts_head,s,t) = ",q

display = False
if display:
        import sys
        sys.path.insert(0,r"C:\_PythonJGE\Utility")
        import graphics_cv as racg
        w = 600
        h = 600
        gr = racg.Graphics(w=w,h=h)
        gr.Clear()
        t = 0
        dt = .01
        while t <= 1.0+dt:
                A = pyBezier(pts_head,t,t)
                B = pyBezier(pts_head,t+dt,t+dt)
                gr.Line(A,B,[0,0,255])
                t = t + dt
        gr.Show("result",-1)
        gr.Save()
        gr.Close()
