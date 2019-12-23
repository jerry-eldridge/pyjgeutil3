# With x1 -> y1 and x2 -> y2, given x, return y using linear map
def MapTo(x1, y1, x2, y2, x):
    epsilon = 0.0001
    if abs(x2 - x1) > epsilon:
        m = 1.*(y2-y1)/(x2-x1)
    else:
        m = 1
    y = m*(x-x1)+y1
    return y

def FalseColor(t, mid):
    P3_MAXVAL = 1.0
    if (t<=mid):
        r = P3_MAXVAL*(-1.0/mid*(t-mid))
        g = P3_MAXVAL*(1.0/mid*(t-mid)+1)
        b = 0
    else:
        r = 0
        g = P3_MAXVAL*(-1.0/(1-mid)*(t-1))
        b = P3_MAXVAL*(1.0/(1-mid)*(t-1)+1)
    return (r,g,b)
