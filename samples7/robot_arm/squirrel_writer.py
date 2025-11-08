import jge_kb as kb

jt = kb.jt
pt = kb.pt
Sigma = kb.Sigma
c_T = Sigma[4]
c_squiggle = Sigma[2]
c_rarrow = Sigma[3]
c_adot = Sigma[5]
S1 = kb.S1
cursor_forward = kb.cursor_forward
carriage_return = kb.carriage_return
writer = kb.writer

from copy import deepcopy
import random

def squirrel_writer(txt,font_dir,page_name,
        color,thickness,
        fn_save_blank,
        fn_save_log,
        fn_save_page
        ):

    blankpage = jt.Page(name=page_name,
             width_in=8.5,height_in=11.0,
             sx = .75, sy = 0.75,
             font = font_dir,
             dpi=300)
    T = jt.StackTypewriter("Typewriter1",
            color,thickness)
    npage = T.push_page(blankpage)
    npage = T.push_page(blankpage)
    #fn_save_blank = f"20251007-blankpage.png"
    T.save_page(fn_save_blank, blankpage)

    C = jt.Character
    x = 5*pt
    y = 5*pt
    w = 18*pt
    h = 18*pt
    xadvance = w*.4 # w + w *.25
    yadvance = h*.9
    bbox = [x,y,w,h]
    x,y,w,h = bbox

    print(f"Press 'T' key")
    fn_log = fn_save_log
    #fn_log = "./20251007-logging-001.txt"
    f = open(fn_log,'a') # open for appending
    f.write("\n\nlogging:\n")
    prevA = None
    while True:
        bboxA = deepcopy(bbox)
        bbox2,txt = writer(f, \
                    T, txt,npage, bboxA,
                    xadvance,yadvance)
        if bbox2 is None:
            break
        if bbox2 == "NIL":
            continue
        if bbox2 != "NIL":
            bboxB = deepcopy(bbox2)
        if prevA is None:
            prevA = deepcopy(bbox2)
            bbox = deepcopy(bboxB)
            continue
        colorA = [255,0,0]
        xx,yy,ww,hh = prevA
        A = [xx+ww,yy+hh/2]
        rA = 3
        thicknessA = 2
        
        colorB = [0,0,255]
        xx,yy,ww,hh = bboxA
        B = [xx,yy+hh/2]
        rB = 3
        thicknessB = 2
        epsilon = 1e-8
        if kb.show and abs(A[1] - B[1]) < epsilon:
            colorC = [255,100,100]
            thicknessC = 3
            T.Line(A,B,colorC,thicknessC)
            T.Circle(A,rA,colorA,thicknessA)
            T.Circle(B,rB,colorB,thicknessB)
        prevA = deepcopy(bboxA)
        bbox = deepcopy(bboxB)
    f.close()
    T.show(npage, ms=10)
    T.paper[-1].gr.Close()
    P = T.pop_page()
    #fn_save_page = f"20251007-page-{npage:03d}.png"
    T.save_page(fn_save_page, P)


