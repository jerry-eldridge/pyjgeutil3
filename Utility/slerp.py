"""
http://pydoc.net/Python/Quaternion/0.03.1/Quaternion/
"""
from quarternion import Quat as Q
from quarternion import normalize

def slerp(q1,q2,t):
    """
    spherical lerp or slerp
    interpolates between quarternion rotations q1 and q2
    with t = 0 to 1. t = 0 is q1 and t = 1 is q2.
    We must have q1 and q2 afterwards normalized with norm(q) = 1
    """
    q = Q(normalize(q1.q*(1-t) + q2.q*t))
    return q
