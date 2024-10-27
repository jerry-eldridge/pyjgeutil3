import sql_multisets as smm

# This is a non-standard example of a sqlite3 over-simplistic
# interface

def display(name,L):
    print(f"Name: {name}")
    print(f"-"*30)
    for x in L:
        print(x)
    print(f"-"*30)
    return

db = r'./game_inventory_20240917.db'
C = smm.SQLMultisets(db)
# insert will assume multiset
# update is used with a condition

# [flag_create,flag_drop] set to
# [True,False], then [False,False], then if done
# with data to [False,True]. To Create and Drop
# in only one session set to [True,True].
flag_create = False
flag_drop = False

names = C.schema()
for tup in names:
    name = tup[0]
    print(f"name = {name}")

L = C.select(\
"ITEMS as I, CONTAINERS as C,INVENTORY as V",
"*",
"""
where V.container_idx == C.idx and
V.item_idx == I.idx
""")
for tup in L:
    print(tup)

C.history()
