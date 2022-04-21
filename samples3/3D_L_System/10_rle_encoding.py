# works with compressed string like above's s1
def enc(s1):
    s2 = s1.replace('**',':')
    L = list(map(lambda s: tuple(s.split(':')),s2.split('*')))
    for i in range(len(L)):
        tup = L[i]
        if len(tup) == 1:
            L[i] = (tup[0],1)
    L2 = list(map(lambda tup: (tup[0],int(tup[1])), L))
    return L2

def dec2(L):
    s1 = ''
    for tup in L:
        val = tup[0]*tup[1]
        s1 = s1 + val
    return s1

def enc2(s):
    s2 = ''
    if len(s) < 1:
        return s
    tup0 = (s[0],1)
    L = []
    for i in range(1,len(s)):
        a = s[i-1]
        b = s[i]
        if a == b:
            tup = (tup0[0],tup0[1]+1)
        else:
            tup = (b,1)
            L.append(tup0)
        tup0 = tup
    L.append(tup0)
    return L

def dec(L):
    s1 = ''
    for tup in L:
        val = tup[0] + '**' + str(tup[1])
        s1 = s1 + '*' + val
    if len(s1) > 0:
        s1 = s1[1:]
    return s1

def E(s):
    L = enc(s)
    s2 = dec2(L)
    return s2

def Display(s):
    print("s = \"%s\"" % s)
    s2 = E(s)
    print("s2 = \"%s\"" % s2)
    print("="*30)
    return

s1 = "[*f**8*x**4*]"
Display(s1)
s2 = "x**3*y**2*f**2*a**3"
Display(s2)
s3 = "[*a*x*f**16*y*a*x*f**16*]"
Display(s3)

