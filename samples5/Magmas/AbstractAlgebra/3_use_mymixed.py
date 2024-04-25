import abstract_types as adt

a = adt.mymixed(3,1,4)
print(f"a = {a}")
b = adt.mymixed(5,1,4)
print(f"b = {b}")
c = a + b
print(f"c = a + b = {c}")
d = a * b
print(f"d = a * b = {d}")
