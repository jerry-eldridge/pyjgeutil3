def encode(msg):
    #print(f"-"*20)
    #print(f"encode:")
    #print(f"msg = '{msg}'")
    data = bytes(list(map(ord,list(msg))))
    #print(f"data = {list(data)}")
    #print(f"-"*20)
    return data

def parse(net,cmds):
    lines = cmds.split('\n')
    try:
        for line in lines:
            if len(line) == 0:
                continue
            print(f"cmd = '{line}'")
            sep = ':'
            toks = line.split(sep)
            if toks[0] == 'cons':
                cons = net.cons
                print(f"cons = {cons}")
            if toks[0] == 'assign':
                a,b,c = list(map(int,toks[1:4]))
                net.assign(a,b,c)
            if toks[0] == 'link':
                a,b = list(map(int,toks[1:3]))
                net.link(a,b)
            if toks[0] == 'switches':
                idx = int(toks[1])
                L = net.nets[idx].get_switches()
                for x in L:
                    print(x)
            if toks[0] == 'graph':
                G = net.get_graph()
                print(f"G = {G}")
            if toks[0] == 'path':
                a,b = list(map(int,toks[1:3]))
                path2 = net.get_path(a,b)
                print(f"path({a},{b}) = {path2}")
            if toks[0] == 'tracert_n':
                na,nb = toks[1:3]
                net.tracert_n(na,nb)
            if toks[0] == 'tracert':
                a,b = list(map(int,toks[1:3]))
                net.tracert(a,b)
            if toks[0] == 'send':
                a,b,val = list(map(int,toks[1:4]))
                net.send(a,b,val)
            if toks[0] == 'chat':
                a,b = list(map(int,toks[1:3]))
                msg = toks[3]
                data = encode(msg)
                net.txrx(a,b,data)
            if toks[0] == '?':
                s = f"""
Instructions (?):
cons - connections on network
assign:<a>:<b>:<c> - call from a to b via c
link:<a>:<b> - link a to b
chat:<a>:<b>:msg - chat from a to b with message msg
switches:<idx> - index idx can be [0,1] currently
graph
path:<a>:<b>
tracert:<a>:<b>
tracert_n:<na>:<nb>

"""
                print(s)
    except:
        return net
    return net
