import centrosome as ce

# Create Fiber Bundle of Microtubules. It is
# called a Centrosome.

# [3] https://en.wikipedia.org/wiki/Fiber_bundle
# The continuous surjective map pi : E -> B
# is F(i)(t) = C.B[i].curve(t) where E is [0,1] and
# B is the Microtubule C.B[i]. Below we use i = 0 for
# 0-th Microtubule or Fiber F(i). The Fibers
# have operations push_plus, pop_plus, push_minus,
# and pop_minus, and also cap_plus and cap_minus.

tmin = 0
tmax = 1
dt = .1

C = ce.Centrosome(O=[0,0])

C.add_fiber(O=[1,1])
C.B[0].push_plus([1,3])
C.B[0].push_plus([2,3.5])
C.B[0].push_plus([3,5])
C.B[0].push_plus([3.5,3])
ce.DisplayFiber(C,0,dt,tmin,tmax)
C.B[0].pop_minus()
ce.DisplayFiber(C,0,dt,tmin,tmax)

C.add_fiber(O=[2,2])
C.B[1].push_plus([3,1])
C.B[1].push_plus([3,2.5])
C.B[1].push_plus([4,5])
C.B[1].push_plus([2.5,2])
ce.DisplayFiber(C,1,dt,tmin,tmax)
