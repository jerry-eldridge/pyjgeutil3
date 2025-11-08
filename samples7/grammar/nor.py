count = 0

def SaveCount():
    global count
    count = count + 1
    return
def Count():
    global count
    n = count
    return n

def Nor(x,y):
    SaveCount()
    z = ~(x|y) % 2
    return z
