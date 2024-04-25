import abstract_types as adt
import random

def demo(N):
    p1 = adt.mypercent(0,2,10) # 2/10
    p2 = adt.mypercent(1,2,10) # 1 2/10
    p = p2
    print(f"p1 = {p1}")
    print(f"p2 = {p2}")
    dollarmax = 1000
    pennymax = 100
    dollars = int(random.uniform(0,dollarmax))
    pennies = int(random.uniform(0,pennymax))
    balance = adt.myucurrency(dollars,pennies,100)
    for period in range(N):
        print(f"balance[{period}] = {balance}")       
        balance = p * balance
    print(f"balance[{period+1}] = {balance}")
    return

demo(N=20)



