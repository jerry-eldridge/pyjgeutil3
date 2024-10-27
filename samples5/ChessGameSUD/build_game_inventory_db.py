import sqlite3
import time
from datetime import datetime
from game_graph import G
import random

import collections

seed0 = 12345
random.seed(seed0)

db = r"./game_inventory_20240917.db"
InventoryRec = collections.namedtuple(\
    "Inventory",["container",
                 "item",
                 "item_count"])
ContainerRec = collections.namedtuple(\
    "Container",
        ["idx",
        "name",
        "desc",
        "capacity"])
ItemRec = collections.namedtuple(\
    "Item",["idx",
            "name",
            "desc",
            "weight"])

def CreateInventoryTable():
     con = sqlite3.connect(db)
     cur = con.cursor()
     q = """
create table INVENTORY (
container_idx   int,
item_idx        int,
item_count      int,
primary key (container_idx,item_idx,item_count)
);
     """
     print(q)
     cur.execute(q)
     con.commit()
     con.close()
     return

def CreateContainersTable():
     con = sqlite3.connect(db)
     cur = con.cursor()
     q = """
create table CONTAINERS (
idx             int,
name            string,
desc            string,
capacity        float,
primary key (idx)
);
     """
     print(q)
     cur.execute(q)
     con.commit()
     con.close()
     return

def CreateItemsTable():
     con = sqlite3.connect(db)
     cur = con.cursor()
     q = """
create table ITEMS (
idx             int,
name            string,
desc            string,
weight          float,
primary key (idx)
);
     """
     print(q)
     cur.execute(q)
     con.commit()
     con.close()
     return

def DropInventoryTable():
     con = sqlite3.connect(db)
     cur = con.cursor()
     q = """
drop table INVENTORY;
     """
     print(q)
     try:
          cur.execute(q)
     except:
          i = 1
     con.commit()
     con.close()
     return

def DropContainersTable():
     con = sqlite3.connect(db)
     cur = con.cursor()
     q = """
drop table Containers;
     """
     print(q)
     try:
          cur.execute(q)
     except:
          i = 1
     con.commit()
     con.close()
     return

def DropItemsTable():
     con = sqlite3.connect(db)
     cur = con.cursor()
     q = """
drop table Items;
     """
     print(q)
     try:
          cur.execute(q)
     except:
          i = 1
     con.commit()
     con.close()
     return

def SelectInventory(container_idx,verbose=False):
     con = sqlite3.connect(db)
     q = f"""
select CONTAINERS.name,
       ITEMS.name,
       INVENTORY.item_count
from INVENTORY,CONTAINERS,ITEMS where
container_idx = {container_idx} and
CONTAINERS.idx = container_idx and
ITEMS.idx = item_idx and
INVENTORY.item_count > 0;
"""
     if verbose:
          print(q)
     cur = con.cursor()    
     cur.execute(q)
     rows = []
     try:
        rows = cur.fetchall()
     except:
        i = 1
     con.close()
     return rows

def SelectContainers(verbose=False):
     con = sqlite3.connect(db)
     q = f"""
select * from Containers;
"""
     if verbose:
          print(q)
     cur = con.cursor()    
     cur.execute(q)
     rows = []
     try:
        rows = cur.fetchall()
     except:
        i = 1
     con.close()
     return rows

def SelectItems(verbose=False):
     con = sqlite3.connect(db)
     q = f"""
select * from Items;
"""
     if verbose:
          print(q)
     cur = con.cursor()    
     cur.execute(q)
     rows = []
     try:
        rows = cur.fetchall()
     except:
        i = 1
     con.close()
     return rows

def SelectInventoryRec(container_idx):
     rows = SelectInventory(container_idx)
     return list(map(InventoryRec._make,rows))

def SelectContainersRec():
     rows = SelectContainers()
     return list(map(ContainerRec._make,rows))

def SelectItemsRec():
     rows = SelectItems()
     return list(map(ItemRec._make,rows))

def InsertInventory(container_idx,item_idx,
            new_item_count,verbose=False):
     q = f"""
select * from INVENTORY where
container_idx = {container_idx} and
item_idx = {item_idx};
"""
     con = sqlite3.connect(db)
     cur = con.cursor()
     cur.execute(q)
     rows = []
     try:
         rows = cur.fetchall()
     except:
         i = 1
     c = len(rows)
     if c == 0:
         item_count = 1
     else:
         item_count = rows[0][2]
     cur = con.cursor()
     if verbose:
          print("Inserting into table")
     if c == 0:
         q = f"""
insert into INVENTORY values
   ({container_idx},{item_idx},{item_count});
"""
         if verbose:
             print(q)
         cur.execute(q)
     elif c > 0:
         q = f"""
update INVENTORY set
   item_count = {new_item_count}
where
   container_idx = {container_idx} and
   item_idx = {item_idx};
"""
         if verbose:
             print(q)
         cur.execute(q)
     con.commit()
     con.close()
     return

def InsertContainer(idx,name,desc,capacity,verbose=False):
     con = sqlite3.connect(db)
     cur = con.cursor()
     if verbose:
          print("Inserting into table")
     q = f"""
insert into CONTAINERS values
   ({idx},"{name}","{desc}",{capacity});
"""
     if verbose:
          print(q)
     cur.execute(q)
     con.commit()
     con.close()
     return

def InsertItem(idx,name,desc,weight,verbose=False):
     con = sqlite3.connect(db)
     cur = con.cursor()
     if verbose:
          print("Inserting into table")
     q = f"""
insert into ITEMS values
   ({idx},"{name}","{desc}",{weight});
"""
     if verbose:
          print(q)
     cur.execute(q)
     con.commit()
     con.close()
     return


def build_game_inventory():
    try:
        DropItemsTable()
        CreateItemsTable()
    except:
        i = 1
    try:
        DropContainersTable()
        CreateContainersTable()
    except:
        i = 1
    try:
        DropInventoryTable()
        CreateInventoryTable()
    except:
        i = 1
    for i in range(len(G['V'])):
         nameS = G['VnamesS'][i]
         nameL = G['VnamesL'][i]
         nameDesc = G['VnamesDesc'][i]
         capacity = 10
         InsertContainer(
               i,
               nameS,
               nameL,
               capacity,
               verbose=False)
    items = []
    def setup_piece(items,item,s1):
         item_idx = len(items)
         InsertItem(item_idx,*item,verbose=False)
         i1 = ['a','b','c','d','e',\
               'f','g','h'].index(s1[0])
         j1 = 7-(int(s1[1])-1)
         container_idx = j1 + i1*8
         item_count = 1
         InsertInventory(\
            container_idx,item_idx,item_count,
                verbose=False)
         items = SelectItemsRec()
         return items
    items = setup_piece(items,['K','King',1000],'d2')
    items = setup_piece(items,['R','Rook',5],'e2')
    items = setup_piece(items,['Q','Queen',9],'c4')
    items = setup_piece(items,['k','king',-1000],'g7')
    items = setup_piece(items,['p','pawn',-1],'h6')
    C = [rec.idx for rec in SelectContainersRec()]
    for idx in range(len(C)):
         L = SelectInventoryRec(idx)
         print(L)
    return

