# 6/12/2015 added color support for Plot to display lines with an optional color
from numpy import array,zeros,ones
from .vectors import lerp

vertex_r = 8
_id_undef = 1

blue = "black"
red = "red"
green = "green"
black = "black"
white = "white"

def PlotVertex(gr,pt,doc,i):
    try:
        color = doc["colors"][i]
    except:
        color = blue
    gr.Point([pt[0],pt[1]],color)
    try:
        s = doc["labels"][i]
    except:
        s = str(i)
    gr.Text(s,pt[0]+vertex_r,pt[1]+vertex_r,black,scale=vertex_r/15.0)
    return

def Show(gr,wn,ms):
    ch = gr.Show(wn,ms)
    return ch
def End(gr):
    gr.Close()
    return
def Plot(gr,doc,color=black,digraph=False):
    global vertex_r
    old_vertex_r = vertex_r
    try:
        printplain = doc['printplain']
    except:
        printplain = False
    if printplain:
        doc['labels'] = ['']*len(doc['V']) 
        vertex_r = 1

    V = doc['V']
    E = doc['E']
    pts = doc['pts']
    try:
        _id = doc['_id']
    except:
        _id = _id_undef
    s = "Graph: %d" % _id
    gr.Text(s, 30,30,color=blue,scale=1)
    n = len(V)
    i = 0
    for S in E:
        k = len(S)
        if k == 2:
            idxs = S
            pt1 = pts[idxs[0]][:2]
            pt2 = pts[idxs[1]][:2]
            gr.Line(pt1, pt2, color)

            if digraph:
                pt = list(map(int,lerp(pt1,pt2,0.9)))
                gr.Point(pt,black)
            pt3 = list(map(int,list(map(round,(lerp(pt1,pt2,0.4))))))
            try:
                if i < len(doc["Enames"]):
                    s = doc["Enames"][i]
                else:
                    s = ""
                gr.Text(s,pt3[0]+4,pt3[1]+4,red,scale=vertex_r/15.0)
            except:
                ii = 0
        i += 1 #indent2
    i = 0 #indent1
    for pt in pts:
        pt = list(map(int,pt))
        PlotVertex(gr,pt,doc,i)
        i += 1
    vertex_r = old_vertex_r
    return

def PlotDigraph(gr,doc,color=black):
    Plot(gr,doc,color=black,digraph=True)
    return
