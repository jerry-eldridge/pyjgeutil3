import graphics_cv as racg
import csv
import cv2
import numpy as np
import math

import os
import fnmatch
import os.path
from datetime import datetime
import time

def video_to_frames(fn_video_mov,root_save):
    ca = cv2.VideoCapture(fn_video_mov)

    counter = 0
    def ProcessFrame(f,counter,root_save):
         #g = ProcessFrame1(f)
         fn = f'{root_save}/frame-%04d.jpg' % counter
         print(f"Saving...fn = {fn}")
         g = cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE)
         cv2.imwrite(fn,g)
         counter = counter + 1
         return g,counter

    if (ca.isOpened() == False):
         print("Error opening video stream or file")

    while (ca.isOpened()):
         r,f = ca.read()
         if r == True:
             g,counter = ProcessFrame(f,counter,
                                      root_save)
             cv2.imshow("Video",g)
             ch = cv2.waitKey(15)
             if ch == ord('e'):
                 break
         else:
             break
    ca.release()
    cv2.destroyAllWindows()
    return counter

def Date2(seconds):
    return datetime.utcfromtimestamp(\
        seconds).strftime('%b %m, %Y')

def Seconds(year,month,day):
    sec = (datetime(year,month,day)-\
           datetime(1970,1,1)).total_seconds()
    return sec

def DirList(fol):
## Directory listing for a folder
    L = []
    for root, dire, files in os.walk(fol):
        for fn in fnmatch.filter(files, "*.jpg"):
            try:
                filename = root + '/'+fn
                L.append(filename)
            except:
                continue
    return L

def frames_to_motion(root, fn_save_verb_txt):
    import mediapipe as mp # Python 312, not yet in 313.

    L = DirList(root)

    ##########################################
    # [1] Google Gemini 2.5 Pro, a large language model
    #

    # Initialize MediaPipe Pose
    mp_pose = mp.solutions.pose
    mp_drawing = mp.solutions.drawing_utils
    pose = mp_pose.Pose(min_detection_confidence=0.5,
                        min_tracking_confidence=0.5)

    L1 = list(mp_pose.PoseLandmark)
    names = [str(L1[i].name) for i in range(len(L1))]
    names = list(set(names))
    names.sort()
    no_show = ["LEFT_EAR","RIGHT_EAR",
            "LEFT_EYE","RIGHT_EYE",
            "LEFT_EYE_INNER","LEFT_EYE_OUTER",
            "RIGHT_EYE_INNER","RIGHT_EYE_OUTER",
            "LEFT_INDEX","LEFT_PINKY",
            "RIGHT_INDEX","RIGHT_PINKY",
            "LEFT_THUMB","RIGHT_THUMB",
            "MOUTH_LEFT","MOUTH_RIGHT"]
    for name in no_show:
        names.remove(name)
    print(names)

    n = 0
    flag = False
    count = 0
    fn_save = fn_save_verb_txt
    ff = open(fn_save,'w')
    print(f"reading frames...")
    for fn in L:
        image0 = cv2.imread(fn,1)
        sh = image0.shape
        hh,ww,cc = sh
        hh2 = int(hh*0.5)
        ww2 = int(ww*0.5)
        image = cv2.resize(image0, (ww2,hh2))

        cv2.imshow("result",image)
        cv2.waitKey(15)
        image = cv2.cvtColor(image.copy(),
                             cv2.COLOR_BGR2RGB)
        
        image.flags.writeable = False
        # Performance optimization

        # Process the image and find pose landmarks
        results = pose.process(image)
        d = {}
        for name in names:
            try:
                val = results.pose_landmarks.landmark[\
                    eval(f"mp_pose.PoseLandmark.{name}")]
                d[name] = [val.x,val.y,val.z,val.visibility]
            except:
                continue
        for name in names:
            try:
                pt = d[name]
                s = f"{count},{name},{pt[0]},"+\
                    f"{pt[1]},{pt[2]},{pt[3]}\n"
                ff.write(s)
            except:
                continue
        
        count = count + 1

    ff.close()
    # Release resources
    pose.close()
    cv2.destroyAllWindows()

    ####################################################
    return len(L)

def add_motion_to_verbs(verbs,fn_verb_txt,name,w,h):
    d = {}
    T = []
    with open(fn_verb_txt,
              'r') as file:
        rdr = csv.reader(file)
        for row in rdr:
            t,part,x,y,z,visibility = row
            visibility = float(visibility)
            t,x,y,visibility = \
                list(map(float, [t,x,y,visibility]))
            if t not in T:
                T.append(t)
            pt = [t,x,y,visibility]
            pt[1] = w*x
            pt[2] = h*y
            #print(pt)
            try:
                d[part].append(pt)
            except:
                d[part] = [pt]
    d['MID_SHOULDER'] = []
    d['MID_HIP'] = []
    K = list(d.keys())
    if 'RIGHT_SHOULDER' in K and \
       'LEFT_SHOULDER' in K and \
       'RIGHT_HIP' in K and \
       'LEFT_HIP' in K:
        for i in range(len(d['RIGHT_SHOULDER'])):
            A = d['RIGHT_SHOULDER'][i]
            B = d['LEFT_SHOULDER'][i]
            C = 0.5*(np.array(A) + np.array(B))
            C = list(map(float,list(C)))
            d['MID_SHOULDER'].append(C)
            A = d['RIGHT_HIP'][i]
            B = d['LEFT_HIP'][i]
            C = 0.5*(np.array(A) + np.array(B))
            C = list(map(float,list(C)))
            d['MID_HIP'].append(C)
    verbs[name] = d
    counter = len(T)
    return verbs,counter

def verb_to_video(verbs,name,fn_video,w,h,c,
              n_images=1000):
    d = verbs[name]
    K = list(d.keys())
    if len(K) == 0:
        return
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
         ['RIGHT_HIP','MID_HIP'],
         ['MID_HIP','LEFT_HIP'],
         ['RIGHT_SHOULDER','MID_SHOULDER'],
         ['MID_SHOULDER','LEFT_SHOULDER'],
         ['MID_SHOULDER','NOSE'],
         ]

    gr = racg.Graphics(w=w,h=h)
    count = 0
    color = [255,0,0]
    fps = 30
    dt = 1/fps
    vv = 0.00001

    sz = (w,h) # scale down the images to sz
    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video = cv2.VideoWriter(fn_video,
                fourcc, fps, sz)
    duration = n_images / fps
    while True:
        gr.Clear()
        #gr.canvas = im.copy()
        for key in K:
            if len(d[key]) == 0:
                continue
            pt = d[key][count%len(d[key])]
            t,x,y,visibility = pt
            if visibility > vv:
                gr.Point([x,y],color)
        for e in E:
            key1,key2 = e
            if key1 in K and key2 in K:
                if len(d[key1]) == 0 or\
                   len(d[key2]) == 0:
                    continue
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
    return
