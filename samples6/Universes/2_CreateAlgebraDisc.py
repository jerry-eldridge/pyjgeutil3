import sys
sys.path.append(r"C:/JGE_Universes/")
import universes
import universes.scene_object as so
import universes.shapes.primitives as ps
import universes.shapes.BasicShapes as ba
import universes.shapes.common.affine as aff

from sympy.combinatorics import Permutation

from math import pi,cos,sin

BIGDATA = r"C:/JGE_Universes/obj/"

Sce = so.Scene()

# Sce.add adds the graph G to the scene and it
# also selects the object graph just added, but
# below we explicitly select each object for clarity.
# Select a shape before a transform else last
# selection will be used.

# convert Euler angle in degrees to quaternion.
def degree2q(R):
    f = lambda x: x*pi/180
    R2 = list(map(f,R))
    # convert Euler angles in radians to quaternion
    q = aff.theta2q(R2)
    return q

# units are 0.01 is one inch for scale, but
# translate basic unit is 50 x 50 x 50., rotate R
# is in degrees.

def CreateScene(Sce):
    G = ps.create_cube()
    Sce.deselectall()
    Sce.add(G,"Floor")
    Sce.select("Floor")
    T = [0,-45,0]
    R = [90,0,0]
    S = [5.5,5.5,0.01]
    Sce.transform(T,R,S)

    N = 7
    TT = []
    r1 = 150
    h1 = 5
    t1 = [0,50,0]
    s1 = [1,1,1]
    for i in range(N+1):
        theta = i*2*pi/(N)
        tup = [t1[0]+r1*cos(theta),
               t1[1],
               t1[2]+r1*sin(theta),
                ]
        TT.append(tup)

    for i in range(len(TT)):
        for j in range(i):
            G = ps.create_cube()
            Sce.deselectall()
            Sce.add(G,f"Cube00-{i}-{j}")
            Sce.select(f"Cube00-{i}-{j}")
            T = [0,0,0]
            R = [0,0,0]
            S = [.1,.1,.1]
            Sce.transform(T,R,S)
            tup = list(TT[i])
            tup[1] = tup[1] + 15*j
            T = tup
            R = [0,90,0]
            S = [1,1,1]
            Sce.transform(T,R,S)

    for i in range(len(TT)):
        for j in range(1+i):
            G = ps.create_cylinder()
            Sce.deselectall()
            Sce.add(G,f"Pillar00-{i}-{j}")
            Sce.select(f"Pillar00-{i}-{j}")
            T = [0,0,0]
            R = [0,0,0]
            S = [.05,1.7,.05]
            Sce.transform(T,R,S)
            tup = list(TT[i])
            T = [0,30,0]
            T[0] = tup[0]
            T[1] = tup[1] + j
            T[2] = tup[2]
            R = [0,0,0]
            S = [1,1,1]
            Sce.transform(T,R,S)
            
    G = ps.create_cube()
    Sce.deselectall()
    Sce.add(G,"SquareHead")
    Sce.select("SquareHead")
    T = [0,0,0]
    R = [0,90,0]
    S = [4.0,.15,.05]
    Sce.transform(T,R,S)
    T = [250,-45,0]
    R = [0,0,0]
    S = [1,1,1]
    Sce.transform(T,R,S)

    def mytransform1(r):
        q0 = degree2q([90,0,0])
        q = degree2q(r)
        q2 = q*q0
        R = list(q2.ToEuler())
        return R

    # Spring Cleaning problem. Rotate square such that
    # square is permutated but stable in the environment
    # in its orientation based on its shape

    def create_disc(n):
        r = r1
        h = 20
        t = [0,50,0]
        s = [1,1,1]
        degrees = 0
        q = aff.HH.rotation_quaternion(degrees,1,0,0)
        H1 = ba.Cylinder(r,h,t,q,s,m=30,n=n)
        return H1
    
    G = create_disc(N)
    Sce.deselectall()
    Sce.add(G,"Disc")
    Sce.select("Disc")
    T = [0,0,0]
    R = mytransform1([0,45,0])
    S = [1,1,1]
    Sce.transform(T,R,S)
    Sce.deselectall()
    Sce.select("Disc")
    for i in range(len(TT)):
        for j in range(1+i):
            Sce.select(f"Cube00-{i}-{j}")
            Sce.select(f"Pillar00-{i}-{j}")
    T = [0, 50, 0]
    Pivot = [0, 0, 0]
    pi2 = Permutation(list(range(1,N))+[0])
    print(f"pi = {pi}")
    a = 6
    sigma = pi2**a
    print(f"sigma = pi**a = {sigma}")
    R = [10,(360/N)*a,0]
    S = [1,1,1]
    Sce.transform(T,R,S,Pivot)
    
    return Sce

Sce = CreateScene(Sce)

fn_save = BIGDATA+"Bed-01.obj"
Sce.save(fn_save)

