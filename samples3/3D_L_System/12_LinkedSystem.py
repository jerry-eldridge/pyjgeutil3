import linked_system as lsm

# Note Sigma is 'A','B','x','i','y','j','z','k','[',
# and ']'.
start = "S"

# A rule is a list (LHS,RHS,p) where
# LHS -> RHS with probability p.
start1 = "S"
rules1 = [
    ("S","[DxDxDx]",.9),
    ("D","[EyEyEy]",.9),
    ("E","[FzFzFz]",.9),
    ("F","aca",.9),
    ("[","<(",1),
    ("]",")>",1)
    ]

start2 = "S"
rules2 = [
    ("S","o[HHH]",1),
    ("H","FoG",1),
    ("G","zFxx",1),
    ("F","[DDDDD]",.9),
    ("D","Exyz",.9),
    ("E","aca",.9),
    ("[","<(",1),
    ("]",")>",1)
    ]

start3 = "D"
rules3 = [
    ("D","N",1),
    ("N","[E]O",1),
    ("O","ffffff",1),
    ("E","XZF",1),
    ("F","XZG",1),
    ("G","XZH",1),
    ("H","XZIX", 1),
    ("I","YJ",1),
    ("J","XWK",1),
    ("K","XWL",1),
    ("L","XWM",1),
    ("M","XW", 1),
    ("X","aaaa",1),
    ("Y","yyyy",1),
    ("Z","zzzz",1),
    ("W","xxxx",1),
    ("[","<(",1),
    ("]",")>",1)
    ]

start4 = "S"
rules4 = [
    ("S","[CC]",1),
    ("C","BBBB",1),
    ("B","aO",1),
    ("O","xGy",1),
    ("G","FFFF",1),
    ("F","ffff",1)
    ]

# set the parameters one by one until reasonably
# too slow. The growth is exponential like.
# Each character A or B is a cylinder shape which
# has lots of points and triangles in it.
## growth burst
F = lambda start,rules: lsm.less_rapid_growth(2,rules)(start)
E = lsm.E

s1 = "[*a*f**8*y**4*f**2*]"
s2 = "x**3*y**2*f**2*a**3"
s3 = "[*a*x*f**16*y*a*x*f**16*]"
s4 = "af**3*a*a*f**3*a"
s6 = lsm.less_rapid_growth(3,rules4)(start4)
s7 = lsm.dec(lsm.enc2(s6))
s8 = F(start1,rules1)
s9 = F(start4,rules4)

###############################################
# These grammars are like robot systems.
#

# The notation is use 'a' for vertex and
# use (nx,ny,nz) for joint angles for edge between
# vertices. Or in other words for vertices
# A,B, and C, then set u = AB, v = BC, and
# angle(u,v) is specified by (nx,ny,nz) to
# represent x**nx*y**ny*z**nz which is roll, yaw,
# and pitch combined as an Euler angles made
# into a quaternion. There are 4 vertices
# and so there are 3 edges in the path graph.
# Integers nx = roll, ny = yaw, nz = pitch in
# discrete quanta.
s_sys1 = E("a**4")
print("There are |s_sys1| = ",len(s_sys1),"segments.")
print("s_sys1 = ",s_sys1)
s10 = lsm.PathSystem(s_sys1,
            [(0,0,0),(0,0,0),(0,0,0)])
s11 = lsm.PathSystem(s_sys1,
            [(0,1,0),(0,0,0),(0,0,0)])
s12 = lsm.PathSystem(s_sys1,
            [(0,1,0),(1,0,0),(0,0,0)])
s13 = lsm.PathSystem(s_sys1,
            [(0,1,0),(2,0,0),(0,0,0)])
s14 = lsm.PathSystem(s_sys1,
            [(0,1,0),(2,0,0),(0,0,-1)])

#
###############################################

bob = ""
ball = "a"

VS = [s1,s10,s11,s12,s13,s14]
print("""
Curves display time i, translation t = [tx,ty,tz]
and quaternion q = [q0,qi,qj,qk] =
q0 + qi*i + qj*j + qk*k where i**2 = j**2 = k**2
= i*j*k = -1.
""")
for i in range(len(VS)):
    v_s = VS[i]
    print(i,"v_s = ",v_s)
    S = lsm.Sentence(s=bob,v=v_s,o=ball,verbose=False)
    ss0 = str(S)
    if v_s in [s8]:
        flag = False
    else:
        flag = True
    t0,q0,pos_curve,q_curve = lsm.Shape0(ss0,flag)
    print("begin_curve")
    for j in range(len(pos_curve)):
        print(j, ss0[:j])
        print(" "*len(str(j))+" t =",pos_curve[j])
        print(" "*len(str(j))+" q =",q_curve[j])
    print("end_curve")
    print("="*30)

