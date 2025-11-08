import jgetypesetter as jt
from copy import deepcopy
import random

C = jt.Character

def lower_script(char):
    n = char.n
    bbox = char.bbox
    x0,y0,w0,h0 = bbox
    x1 = x0 + w0
    y1 = y0 + h0
    w1 = .49*w0
    h1 = .49*h0
    char2 = jt.Character(n,x1,y1,w1,h1)
    return char2
def upper_script(char):
    n = char.n
    bbox = char.bbox
    x0,y0,w0,h0 = bbox
    x1 = x0 + w0
    y1 = y0
    w1 = .49*w0
    h1 = .49*h0
    char2 = jt.Character(n,x1,y1,w1,h1)
    return char2

def hatdot(char):
    n = char.n
    bbox = char.bbox
    x0,y0,w0,h0 = bbox
    x1 = x0
    y1 = y0 - 1.1*h0/2
    h1 = h0/2
    w1 = w0
    char2 = jt.Character(n,x1,y1,w1,h1)
    return char2

show = False

def S1(T,x,y,w,h):
    def F(n):
        char1 = C(n,x,y,w,h)
        T.key(char1,show)
        char2 = lower_script(C([84],x,y,w,h))
        T.key(char2,show)
        return char1.bbox
    return F

def udot(T,x,y,w,h):
    def F(n):
        char1 = C(n,x,y,w,h)
        T.key(char1,show)
        n = [204,135]
        char2 = hatdot(C(n,x,y,w,h))
        T.key(char2,show)
        return char1.bbox
    return F

def uddot(T,x,y,w,h):
    def F(n):
        char1 = C(n,x,y,w,h)
        T.key(char1,show)
        n = [194,168]
        char2 = hatdot(C(n,x,y,w,h))
        T.key(char2,show)
        return char1.bbox
    return F

def cursor_forward(T,bbox,xadvance):
    # cursor forward
    bbox = deepcopy(bbox)
    bbox = T.advance_bbox(bbox, *[xadvance,0])
    return bbox

def carriage_return(T,bbox,yadvance,lmargin=0):
    bbox = deepcopy(bbox)
    bbox[0] = lmargin
    bbox = T.advance_bbox(bbox, *[0,yadvance])
    return bbox

pt = 1/72 # inch
# define Alphabet (valid codes are specified
# in the font folder "./alphabet".
Sigma = [[52],[88],[196,129],[226,134,146],[84],
         [204,135]]

def keyboard(f, T, npage, bbox,
        xadvance,yadvance,
        margin=5*pt):
    global show
    ch = T.show(npage, ms=15)
    if ch == -1:
        return "NIL"
    if ch == ord('Q'):
        return None
    if ch == ord('&'):
        show = not show
        return bbox
    print(ch, end = ' ')
    f.write(chr(ch)+ ' ')
    if ch == 10: # line feed, n
        bbox = carriage_return(T,bbox,\
                yadvance,lmargin=margin)
        bbox[0] = margin
        return bbox
    elif ch == 13: # carriage return, r
        bbox = carriage_return(T,bbox,\
                yadvance,lmargin=margin)
        bbox[0] = margin
        return bbox

    # if ch in a,b,c,..., up to length of Sigma
    # then use Sigma characters, else use ASCII
    # except for those used up by Sigma's representation
    if ch in range(ord('a'),ord('a')+len(Sigma)):
        n = Sigma[ch-ord('a')]
    elif ch == ord('!'):
        ch2 = T.show(npage, ms=-1, verbose=False)
        if ch2 == -1:
            return bbox
        print(ch2, end = ' ')
        f.write(chr(ch2)+ ' ')
        if ch2 in range(ord('a'),ord('a')+len(Sigma)):
            n = Sigma[ch2-ord('a')]
            F = S1(T,*bbox)
            bbox = F(n)
            bbox = cursor_forward(T,bbox,xadvance)
            return bbox
        else:
            n = [ch2]
            F = S1(T,*bbox)
            bbox = F(n)
            bbox = cursor_forward(T,bbox,xadvance)
            return bbox
    elif ch == ord('@'):
        ch2 = T.show(npage, ms=-1, verbose=False)
        if ch2 == -1:
            return bbox
        print(chr(ch2), end = ' ')
        f.write(chr(ch2)+ ' ')
        if ch2 in range(ord('a'),ord('a')+len(Sigma)):
            n = Sigma[ch2-ord('a')]
            F = udot(T,*bbox)
            bbox = F(n)
            bbox = cursor_forward(T,bbox,xadvance)
            return bbox
        else:
            n = [ch2]
            F = udot(T,*bbox)
            bbox = F(n)
            bbox = cursor_forward(T,bbox,xadvance)
            return bbox
    elif ch == ord('#'):
        ch2 = T.show(npage, ms=-1, verbose=False)
        if ch2 == -1:
            return bbox
        print(chr(ch2), end = ' ')
        f.write(chr(ch2)+ ' ')
        if ch2 in range(ord('a'),ord('a')+len(Sigma)):
            n = Sigma[ch2-ord('a')]
            F = uddot(T,*bbox)
            bbox = F(n)
            bbox = cursor_forward(T,bbox,xadvance)
            return bbox
        else:
            n = [ch2]
            F = uddot(T,*bbox)
            bbox = F(n)
            bbox = cursor_forward(T,bbox,xadvance)
            return bbox
    else:
        n = [ch]

    if 0 <= npage and npage <= len(T.paper)-1:
        P = T.paper[npage]
        width = P.width/(P.dpi*P.sx)
        height = P.height/(P.dpi*P.sy)
    if bbox[0] > width - 100*pt:
        bbox = carriage_return(T,bbox,\
                yadvance,lmargin=margin)
    c = C(n,*bbox)
    T.key(c,show_bbox=show)
    bbox = cursor_forward(T,bbox,xadvance)
    return bbox

def writer(f, T, txt, npage, bbox,
        xadvance,yadvance,
        margin=5*pt):
    global show

    M = list(str(txt))
    if len(M) == 0:
        return None,''.join(M)
    ch = ord(M[0])
    M = M[1:]
    T.show(npage, ms=15)
    if ch == ord('&'):
        show = not show
        return bbox,''.join(M)
    print(ch, end = ' ')
    f.write(chr(ch)+ ' ')
    if ch == 10: # line feed, n
        bbox = carriage_return(T,bbox,\
                yadvance,lmargin=margin)
        bbox[0] = margin
        return bbox,''.join(M)
    elif ch == 13: # carriage return, r
        bbox = carriage_return(T,bbox,\
                yadvance,lmargin=margin)
        bbox[0] = margin
        return bbox,''.join(M)

    # if ch in a,b,c,..., up to length of Sigma
    # then use Sigma characters, else use ASCII
    # except for those used up by Sigma's representation
    S = range(256)
    if ch in S:
        n = [ch]
    else:
        n = [ch]

    if 0 <= npage and npage <= len(T.paper)-1:
        P = T.paper[npage]
        width = P.width/(P.dpi*P.sx)
        height = P.height/(P.dpi*P.sy)
    if bbox[0] > width - 100*pt:
        bbox = carriage_return(T,bbox,\
                yadvance,lmargin=margin)
    c = C(n,*bbox)
    T.key(c,show_bbox=show)
    bbox = cursor_forward(T,bbox,xadvance)
    return bbox, ''.join(M)

