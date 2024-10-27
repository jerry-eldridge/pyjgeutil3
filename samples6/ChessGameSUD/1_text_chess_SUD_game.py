from game_graph import G
import build_game_inventory_db as bgi
import blindsearch as bs

flag_build = False
if flag_build:
    bgi.build_game_inventory()


def InAdj(doc,i):
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[i]
    for e in E:
        v,w = e
        if (u == w):
            adj.append(v)
    return adj

def OutAdj(doc,i):
    V = doc['V']
    E = doc['E']
    adj = []
    u = V[i]
    for e in E:
        v,w = e
        if (u == v):
            adj.append(w)
    return adj

def get_containers():
    return bgi.SelectContainersRec()
def get_items():
    return bgi.SelectItemsRec()
def get_inventory(container_idx):
    return bgi.SelectInventoryRec(container_idx)    

def play_game(G,start):
    done = False
    u = G['VnamesS'].index(start)
    same_room = False
    I = [rec.name for rec in get_items()]
    print(f"I = {I}")
    C = [rec.name for rec in get_containers()]
    print(f"C = {C}")
    player_inventory = []
    player_capacity = 10
    while not done:
        if not same_room:
            print(G['VnamesL'][u])
            print()
        d = input("> ")
        if d == 'h' or d == 'help':
            print("""
Enter
'i' (inventory),
'l' (list) or 'list',
'lk' (look) or 'look',
'q' (quit),
'go <direction> (combine with 'list')
'get <item>' (get from a room)
'drop <item>' (drop to a room)
'find <item>' (search for item)
""")
            same_room = True
        N = OutAdj(G,u)
        L = []
        for v in N:
            e = [u,v]
            if e in G['E']:
                idx = G['E'].index(e)
                dv = G['Enames'][idx]
                L.append((v,dv))
        if d == 'l' or d == 'list':
            L2 = [tup[1] for tup in L]
            print(f"list: {L2}")
            same_room = True
        if d == 'q' or d == 'quit':
            done = True
            break
        if d == 'lk' or d == 'look':
            same_room = True
            print(G['VnamesL'][u])
            print()
            print(G['VnamesDesc'][u])
            name = G['VnamesS'][u]
            print(f"name = {name}")
            idx = C.index(name)
            J = get_inventory(idx)
            K = [str((rec.item,rec.item_count)) \
                 for rec in J]
            s = 'This room contains '+','.join(K)+'.'
            print(s)
        if d == 'i' or d == 'inventory':
            same_room = True
            name = G['VnamesS'][u]
            print(f"name = {name}")
            idx = C.index(name)
            J = get_inventory(idx)
            K = [rec.item for rec in J]
            s = 'This room contains '+','.join(K)+'.'
            print(s)
        if d[:3] == 'get':
            same_room = True
            name = G['VnamesS'][u]
            room = name
            #print(f"room = {room}")
            room_idx = C.index(room)
            #print(f"room_idx = {room_idx}")
            toks = d.split(' ')
            if len(toks) == 2:
                #print(f"get")
                item_name = toks[1]
                #print(f"item_name = {item_name}")
                J = get_inventory(room_idx)
                K = [rec.item for rec in J]
                if item_name in K:
                    item = get_items()[I.index(item_name)]
                    #print(f"item = {item}")
                    name = item.name
                    desc = item.desc
                    weight = item.weight
                    rec = J[K.index(name)]
                    #print(f"rec = {rec}")
                    if player_capacity - weight >= 0 \
                       and rec.item_count > 0:
                        player_inventory.append(item)
                        player_capacity = player_capacity - weight
                        bgi.InsertInventory(\
                            room_idx,
                            item.idx,
                            rec.item_count-1,
                            verbose=False)
        if d[:4] == 'drop':
            same_room = True
            name = G['VnamesS'][u]
            room = name
            #print(f"room = {room}")
            room_idx = C.index(room)
            #print(f"room_idx = {room_idx}")
            toks = d.split(' ')
            if len(toks) == 2:
                #print(f"drop")
                item_name = toks[1]
                #print(f"item_name = {item_name}")
                J = get_inventory(room_idx)
                K = [rec.name for \
                     rec in player_inventory]
                if item_name in K:
                    rec = None
                    for rec in player_inventory:
                        if rec.name == item_name:
                            break
                    if rec is not None:
                        player_inventory.remove(rec)
                        item2 = rec
                        #print(f"item = {item}")
                        name = item2.name
                        desc = item2.desc
                        weight = item2.weight
                        KJ = [rec.item for rec in J]
                        try:
                            item3 = J[KJ.index(name)]
                            bgi.InsertInventory(\
                                room_idx,
                                item3.idx,
                                item3.item_count+1,
                                verbose=False)
                        except:
                            bgi.InsertInventory(\
                                room_idx,
                                item2.idx,
                                1,verbose=False)
                        player_capacity = player_capacity + weight
        if d[:4] == 'find':
            name = G['VnamesS'][u]
            room = name
            #print(f"room = {room}")
            room_idx = C.index(room)
            toks = d.split(' ')
            if len(toks) < 2:
                continue
            item_name = toks[1]
            u_last = u
                
            path = bs.BFS(G,room_idx)
            while len(path) > 0:
                same_room = False
                u = path[0]
                e = [u_last,u]
                if e in G['E']:
                    idx_e = G['E'].index(e)
                    action = G['Enames'][idx_e]
                    print(f"go {action}")
                path = path[1:]
                same_room = True
                name = G['VnamesS'][u]
                idx = C.index(name)
                J = get_inventory(idx)
                K = [str((rec.item,rec.item_count)) \
                     for rec in J]
                s = 'This room contains '+','.join(K)+'.'
                JJ = [rec.item for rec in J \
                      if rec.item_count > 0]
                if item_name in JJ:
                    print(f"look")
                    print(G['VnamesL'][u])
                    print()
                    print(G['VnamesDesc'][u])
                    print(f"name = {name}")
                    print(s)
                    break
        if d == 'i':
            print(f"player_inventory = {player_inventory}")
        for tup in L:
            if f"go {tup[1]}".lower() == d.lower():
                same_room = False
                u = tup[0]
                break
    return



play_game(G,start="a1")


    
    
