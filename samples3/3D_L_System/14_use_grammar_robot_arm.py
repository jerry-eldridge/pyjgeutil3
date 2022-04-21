import linked_system as lsm
import grammar_robot_arm as ra

def Display(P,goal):
    start = P.Start()
    #print("G = ", P.Graph())
    print()
    print("Before: s = P.get_s() = ",P.get_s())
    print("Before: start: ", start)
    print("Before: d(start,goal) = ", ra.d(start,goal))
    print()
    print("goal = ",goal)
    print("Reaching for goal...")
    P,done = ra.Reach(P, goal, flag=True)
    print("...Finished reaching...done?",done)
    print()
    print("After: s = P.get_s() = ",P.get_s())
    start = P.Start()
    print("After: start: ", start)
    print("After: d(start,goal) = ", ra.d(start,goal))
    print("="*30)
    return
    

E = lsm.E
s_sys_A = E("a**4")
ja_A = [(0,1,0),(2,0,0),(0,0,-5)]
s_A = lsm.PathSystem(s_sys_A,ja_A)
P = ra.RobotArm(s_sys_A, ja_A, subj="",obj="a")

goal = [-50,-70,-40]

Display(P,goal)
Display(P,goal)
