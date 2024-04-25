import abstract_types as adt

x = adt.myreal('x')
y = adt.myreal('y')
print(f' x = {x}')
print(f' y = {y}')
print(f' x*y = {x*y}')

f = adt.L('myfunction')(adt.myreal('a')) # left multiplication
print(f" f = {f}")
print(f" f*x = {f*x}")
g = adt.R('myfunction')(adt.myreal('b')) # right multiplication
print(f" g = {g}")
print(f" g*x = {g*x}")
h = adt.L('myfunction')(adt.myreal('c')) # right multiplication
print(f" h = {h}")
print(f" h*x = {h*x}")
print(f" f*(g*x) = {f*(g*x)}")
print(f" (f*g)*x = {(f*g)*x}")
print(f" f*g = {f*g}")
print(f" f*g*x = {f*g*x}")

A = adt.L('my-L-operator')(h)
print(f" A = {A}")
print(f" A*f = {A*f}")
print(f" A*(f*x) = {A*(f*x)}")
print(f" (A*f)*x = {(A*f)*x}")
B = adt.L('my-L-operator')(g)
print(f" B = {B}")
print(f" B*f*x = {B*f*x}")
print(f" (B*A)*f*x = {(B*A)*f*x}")
print(f" B*A = {B*A}")
print(f" B*(A*f)*x = {B*(A*f)*x}")
print(f" (B*A)*(f*x) = {(B*A)*(f*x)}")
print(f" (B*A)*f = {(B*A)*f}")
print(f" (B*A)*f*x = {(B*A)*f*x}")

