# Requirements:
# pip install opencv-python mediapipe numpy

import cv2
import mediapipe as mp # Python 312, not yet in 313.
import numpy as np
import math

import os
import fnmatch
import os.path
from datetime import datetime
import time

root = f"./imgs/"

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

L0 = DirList("./imgs/")
five_cycles = len(L0)//5
two_cycles = int(five_cycles*10/5)
L = L0[:two_cycles]

##########################################
# [1] Google Gemini 2.5 Pro, a large language model
#

# Initialize MediaPipe Pose
mp_pose = mp.solutions.pose
mp_drawing = mp.solutions.drawing_utils
pose = mp_pose.Pose(min_detection_confidence=0.5,
                    min_tracking_confidence=0.5)

# --- Configuration ---
# You might need to change the camera index
#if 0 is not your default webcam
CAMERA_INDEX = 0

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

#Gets pixel coordinates for a specific landmark.
def get_landmark_coords(landmarks, landmark_enum,
                        image_shape):
    if landmarks:
        try:
            landmark = landmarks.landmark[landmark_enum]
            # Check visibility - landmarks might
            #be detected but estimated as not visible
            if landmark.visibility < 0.5:
                # Adjust threshold if needed
                 return None
            # Convert normalized coordinates
            #(0.0 - 1.0) to pixel coordinates
            img_h, img_w = image_shape[:2]
            x = int(landmark.x * img_w)
            y = int(landmark.y * img_h)
            return (x, y)
        except IndexError:
            return None
    return None

### Start video capture
##cap = cv2.VideoCapture(CAMERA_INDEX)
##
##if not cap.isOpened():
##    print(f"Error: Could not open video source "+\
##          f"{CAMERA_INDEX}.")
##    exit()
##
##print("Starting video stream. Press 'q' to quit.")

n = 0
flag = False
count = 0
fn_save = f"20250414-JGE-motion_capture.txt"
ff = open(fn_save,'w')
for fn in L:
    #success, image = cap.read()
##    if not success:
##        print("Ignoring empty camera frame.")
##        continue
    image00 = cv2.imread(fn,1)
    image0 = cv2.flip(image00,1)
    sh = image0.shape
    hh,ww,cc = sh
    hh2 = int(hh*0.5)
    ww2 = int(ww*0.5)
    image = cv2.resize(image0, (ww2,hh2))

    # Flip the image horizontally for a later
    # selfie-view display
    # Also convert the BGR image to RGB before
    # processing
    cv2.imshow("result",image)
    cv2.waitKey(15)
    image = cv2.cvtColor(cv2.flip(image, 1),
                         cv2.COLOR_BGR2RGB)
    
    image.flags.writeable = False
    # Performance optimization

    # Process the image and find pose landmarks
    results = pose.process(image)
    d = {}
    for name in names:
        val = results.pose_landmarks.landmark[\
            eval(f"mp_pose.PoseLandmark.{name}")]
        d[name] = [val.x,val.y,val.z,val.visibility]
    for name in names:
        pt = d[name]
        s = f"{count},{name},{pt[0]},"+\
            f"{pt[1]},{pt[2]},{pt[3]}\n"
        ff.write(s)
    
    count = count + 1

ff.close()
# Release resources
pose.close()
cv2.destroyAllWindows()

####################################################
