import extrusion as ext

BIGDATA = r"C:/_BigData/_3D/my_scenes/"

G = {}
G['V'] = []
G['E'] = []
G['F'] = []
G['N'] = []
G['pts'] = []
Gs = []

w,h,d = 10,10,10
degrees = 90
axis = [0,0,1]
q = ext.aff.HH.rotation_quaternion(degrees,axis[0],axis[1],axis[2])
t = [-50,0,0]
s = [1,1,1]
G2 = ext.CubeObj(w,h,d, t,q,s)
Gs = ext.Append(Gs,G2)
G = ext.GraphUnionS(G,G2)

#H = Parabola()
H = ext.TrefoilKnot()
Gs = ext.Append(Gs,H)
G = ext.GraphUnionS(G,H)

ext.Graph2OBJ(BIGDATA+"extrude-1.obj",G,"scene")
import os
print "Open extrude-1.obj with 3D Viewer by double-clicking on it"
os.system(BIGDATA+"extrude-1.obj")
