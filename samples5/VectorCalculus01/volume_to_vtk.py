import re
import time
import os
import fnmatch
import os.path
from datetime import datetime

import cv2
import numpy as np

def Date(seconds):
     return datetime.utcfromtimestamp(seconds).strftime('%Y-%m-%d %H:%M:%S')

def Seconds(year,month,day):
     sec = (datetime(year,month,day)-datetime(1970,1,1)).total_seconds()
     return sec


def ListFiles(folder,pattern):
    L = []
    for root, dire, files in os.walk(folder):
        for fn in fnmatch.filter(files, pattern):
            try:
                root = root.replace('\\','/')
                fn = fn.replace('\\','/')
                filename = root + '/' + fn
                L.append(filename)
            except:
                continue
    return L

def volume_to_vtk(fn_save, volume):
     sh = volume.shape
     f = open(fn_save, 'w')
     txt = f"""# vtk DataFile Version 2.0
Volume example
ASCII

DATASET STRUCTURED_POINTS
DIMENSIONS {sh[0]} {sh[1]} {sh[2]}
ASPECT_RATIO 1 1 1
ORIGIN   0.000 0.000 0.000
SPACING  1.000 {(sh[0]/sh[1])} {(sh[0]/sh[2])}
POINT_DATA {sh[0]*sh[1]*sh[2]}
SCALARS volume_scalars float 1
LOOKUP_TABLE default
"""
     f.write(txt)
     for k in range(sh[2]):
          for j in range(sh[1]):
               s = ''
               for i in range(sh[0]):
                    val = volume[i,j,k]
                    v = f"{val} "
                    s = s + v
               s = s + '\n'
               f.write(s)
     f.close()
     return
    
