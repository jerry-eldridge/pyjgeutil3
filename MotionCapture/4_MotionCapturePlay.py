import graphics_cv as racg
import csv
import cv2
import numpy as np

fn = f"./frame-0800-s.jpg"
im = cv2.imread(fn,1)
sh = im.shape
h,w,c = sh

d = {}
with open(f"./20250414-JGE-motion_capture.txt",
          'r') as file:
    rdr = csv.reader(file)
    for row in rdr:
        t,part,x,y,z,visibility = row
        visibility = float(visibility)
        t,x,y,visibility = \
            list(map(float, [t,x,y,visibility]))
        pt = [t,x,y,visibility]
        pt[1] = w*x
        pt[2] = h*y
        #print(pt)
        try:
            d[part].append(pt)
        except:
            d[part] = [pt]
d['MID_SHOULDER'] = []
for i in range(len(d['RIGHT_SHOULDER'])):
    A = d['RIGHT_SHOULDER'][i]
    B = d['LEFT_SHOULDER'][i]
    C = 0.5*(np.array(A) + np.array(B))
    C = list(map(float,list(C)))
    d['MID_SHOULDER'].append(C)
K = list(d.keys())
E = [
    ['LEFT_SHOULDER','LEFT_ELBOW'],
     ['LEFT_ELBOW','LEFT_WRIST'],
     ['LEFT_SHOULDER','LEFT_HIP'],
     ['LEFT_HIP', 'LEFT_KNEE'],
     ['LEFT_KNEE', 'LEFT_ANKLE'],
     ['LEFT_ANKLE','LEFT_HEEL'],
     ['LEFT_HEEL','LEFT_FOOT_INDEX'],
     ['LEFT_ANKLE','LEFT_FOOT_INDEX'],
     ['RIGHT_SHOULDER','RIGHT_ELBOW'],
     ['RIGHT_ELBOW','RIGHT_WRIST'],
     ['RIGHT_SHOULDER','RIGHT_HIP'],
     ['RIGHT_HIP', 'RIGHT_KNEE'],
     ['RIGHT_KNEE', 'RIGHT_ANKLE'],
     ['RIGHT_ANKLE','RIGHT_HEEL'],
     ['RIGHT_HEEL','RIGHT_FOOT_INDEX'],
     ['RIGHT_ANKLE','RIGHT_FOOT_INDEX'],
     ['RIGHT_HIP','LEFT_HIP'],
     ['RIGHT_SHOULDER','LEFT_SHOULDER'],
     ['MID_SHOULDER','NOSE'],
     ]

gr = racg.Graphics(w=w,h=h)
count = 0
color = [255,0,0]
fps = 30
dt = 1/fps
vv = 0.05

sz = (w,h) # scale down the images to sz
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
video = cv2.VideoWriter('./JGE_WalkCycle.avi',
            fourcc, fps, sz)

n_images = 1000
duration = n_images / fps
while True:
    gr.Clear()
    #gr.canvas = im.copy()
    for key in K:
        pt = d[key][count%len(d[key])]
        t,x,y,visibility = pt
        if visibility > vv:
            gr.Point([x,y],color)
    for e in E:
        key1,key2 = e
        A = d[key1][count%len(d[key1])]
        B = d[key2][count%len(d[key2])]
        t1,x1,y1,visibility1 = A
        if visibility1 > vv:
            t2,x2,y2,visibility2 = B
            if visibility2 > vv:
                gr.Line([x1,y1],[x2,y2],color)
    video.write(gr.canvas)            
    count = count + 1
    if count > n_images:
        break
    ch = gr.Show("result",int(dt*1000))
    if ch == ord('e'):
        break

gr.Show("result",-1)
gr.Close()
video.release()


