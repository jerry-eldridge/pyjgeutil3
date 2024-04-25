import abstract_types as adt
import random

def demo():
    key = random.choice(adt.mycurrency_names)
    a = adt.mycurrency(key)('1')
    c = random.choice(range(1,20))
    count = adt.myint(str(c))
    b = count*a
    print(f"a = {a}")
    print(f"b = {b}")
    print()
    return

N = 10
for i in range(N):
    demo()



