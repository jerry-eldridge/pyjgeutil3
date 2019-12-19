import graph as g
def plot_graph_turtle(G,wn="result",ms=-1,digraph=False):
    import graphics_turtle as racg
    gr = racg.Graphics()
    import plot_graph_simple_turtle as pgs
    w = h = gr.h
    G2 = g.CreateCircleGeometry(G,w,h,0,h/3)
    gr.Clear()
    pgs.Plot(gr,G2,digraph=digraph)
    pgs.Show(gr,wn,ms)
    gr.Close()
    return

def plot_graph_cv(G,wn="result",ms=-1,digraph=False):
    import graphics_cv as racg
    gr = racg.Graphics()
    import plot_graph_simple_cv as pgs
    w = h = gr.h
    G2 = g.CreateCircleGeometry(G,w/2,h/2,0,h/3)
    gr.Clear()
    pgs.Plot(gr,G2,digraph=digraph)
    pgs.Show(gr,wn,ms)
    gr.Close()
    return
