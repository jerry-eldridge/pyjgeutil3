import abstract_types as adt

a = adt.mymixed(3,1,2)
print(f"a = {a}")
b = adt.mymixed(5,1,2)
print(f"b = {b}")
c = a + b
print(f"c = a + b = {c}")
d = a * b
print(f"d = a * b = {d}")
e = adt.mymixed(3,0,1)
print(f"e = {e}")
f = e + e
print(f"f = e + e = {f}")
