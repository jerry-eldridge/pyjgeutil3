import cv2
import numpy as np

import image_compress as imc
import time

def GetImageY(fn):
    # read image as grayscale as numpy array
    im = cv2.imread(fn,0)
    return im

def GetImageC(fn):
    # read image as color as numpy array
    im = cv2.imread(fn,1)
    return im

def SaveImage(fn_save, x):
    print("Saving image fn_save=",fn_save)
    f = open(fn_save,'wb')
    f.write(bytes(x))
    f.close()
    return

def LoadImage(fn_save):
    print("Loading image fn_save=",fn_save)
    g = open(fn_save,'rb')
    x = g.read()
    g.close()
    return x

def ShowImage(im,wn,ms):
    cv2.imshow(wn,im)
    ch = cv2.waitKey(ms)
    return ch

def CloseWindows():
    cv2.destroyAllWindows()
    return

def Do_Encoding(fn_jpg,fn_imdat_save,
                n_compression=10):
    wn = "result"
    ms = 15
    im = GetImageC(fn_jpg)
    sh = im.shape
    print("raw image size = ", sh[1]*sh[0]*sh[2])
    #ch = ShowImage(im, wn,ms)
    print("Starting encoding...")
    t_start = time.time()
    x = imc.encode_image_compress_2D_C(im,
            n_compression = n_compression,
            zlib_level = 1)
    t_end = time.time()
    dt = float(t_end - t_start)
    print("Elapsed time dt = ",dt,"seconds")
    print("compressed signal x size =",len(x))
    SaveImage(fn_imdat_save,x)
    return

def Do_Decoding(fn_imdat_save):
    wn = "result"
    ms = 150
    x = LoadImage(fn_imdat_save)
    print("compressed signal x size =",len(x))
    print("Starting decoding...")
    t_start = time.time()
    im = imc.decode_image_compress_2D_C(x)
    t_end = time.time()
    dt = float(t_end - t_start)
    print("Elapsed time dt = ",dt,"seconds")
    sh = im.shape
    print("raw image size = ", sh[1]*sh[0]*sh[2])
    ch = ShowImage(im, wn,ms)
    return

ext = ".jpg"
fn_jpg1 = r"./microscope-7.jpg"

##M = [5,10,15,20,25,30]
M = [10]
files = []
for i in range(len(M)):
    nc = M[i]
    s = '-%02d' % (nc)
    fn_save_nc = fn_jpg1[:-len(ext)]+s+".im_dat"
    files.append(fn_save_nc)
    Do_Encoding(fn_jpg1,fn_save_nc,
                n_compression=nc)
    print("===")
print()
for i in range(len(files)):
    fn_save_nc = files[i]
    Do_Decoding(fn_save_nc)
    print("===")

CloseWindows()


