def build_graph(Vdata,Edata):
    G = {}
    V = []
    E = []
    VnamesS = []
    VnamesL = []
    VnamesDesc = []
    c = 0
    for tup in Vdata:
        if tup[0] not in VnamesS:
            VnamesS.append(tup[0])
            VnamesL.append(tup[1])
            VnamesDesc.append(tup[2].strip())
            V.append(c)
            c = c + 1
    Enames = []
    c = 0
    for tup in Edata:
        un,vn,d = tup
        u = VnamesS.index(un)
        v = VnamesS.index(vn)
        e = [u,v]
        if e not in E:
            E.append(e)
            Enames.append(d)
    G['V'] = V
    G['E'] = E
    G['VnamesS'] = VnamesS
    G['VnamesL'] = VnamesL
    G['VnamesDesc'] = VnamesDesc
    G['Enames'] = Enames
    return G

Vdata = []
Edata = []
cols = list(map(lambda i: chr(ord('a')+i), range(8)))
rows = list(map(lambda i: chr(ord('1')+i), range(8)))
for i in range(8):
    for j in range(8):
        square = cols[i]+rows[7-j]
        square_long = square
        square_desc = square
        tup = (square,square,square)
        Vdata.append(tup)
for i in range(7):
    for j in range(8):
        s1 = cols[i]+rows[7-j]
        s2 = cols[i+1]+rows[7-j]
        e = (s1,s2,"E")
        Edata.append(e)
for i in range(7):
    for j in range(8):
        s1 = cols[i]+rows[7-j]
        s2 = cols[i+1]+rows[7-j]
        e = (s2,s1,"W")
        Edata.append(e)
for i in range(8):
    for j in range(7):
        s1 = cols[i]+rows[7-j]
        s2 = cols[i]+rows[7-(j+1)]
        e = (s1,s2,"S")
        Edata.append(e)
for i in range(8):
    for j in range(7):
        s1 = cols[i]+rows[7-j]
        s2 = cols[i]+rows[7-(j+1)]
        e = (s2,s1,"N")
        Edata.append(e)

G = build_graph(Vdata,Edata)

