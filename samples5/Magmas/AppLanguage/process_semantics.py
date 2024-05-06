d_f = {}
d_x = {}

def set_function(name,f):
    global d_f
    d_f[name] = f
    return
def set_var(name,value):
    global d_x
    d_x[name] = value
    return

def make_name(x):
    try:
        if len(x) == 1:
            return x[0]
        if len(x) >= 2:
            car = x[0]
            cdr = x[1:]
            return s
    except:
        return x

def process(p):
    if len(p) == 2:
        f,x = p
        if len(f) == 2:
            f2 = process(f)
            f2_name = make_name(f2)
            set_function(f2_name,f2)
            f = f2_name
        if len(x) == 2:
            x2 = process(x)
            x2_name = make_name(x2)
            set_var(x2_name, x2)
            x = x2_name
        val = d_f[f](d_x[x])
        return val
    else:
        return p
