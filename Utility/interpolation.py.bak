import mapto
def interpolation(x,X,Y):
    if x <= X[0]:
        return Y[0]
    elif x >= X[-1]:
        return Y[-1]
    else:
        i = 0
        while X[i] < x:
            i += 1
        return mapto.MapTo(X[i-1],Y[i-1],X[i],Y[i],x)
