import cv2
import numpy as np

# On iPad, a camera person held the iPad steady
# while I walked on a treadmill doing a Walk Cycle.
ca = cv2.VideoCapture('./IMG_2455.MOV')

hsv_tan = cv2.cvtColor(np.uint8([[[140, 180, 210]]]),
                           cv2.COLOR_BGR2HSV)
def ProcessFrame2(f0):
     h,w,c = f0.shape
     scale = .7
     h = int(h*scale)
     w = int(w*scale)
     f = cv2.resize(f0,(w,h))
     im = cv2.flip(f,-1) # =0 v, >0 h, < 0: v and h
     im2 = cv2.GaussianBlur(im,(13,13),0)
     return im2

def ProcessFrame1(f0):
     h,w,c = f0.shape
     scale = .7
     h = int(h*scale)
     w = int(w*scale)
     f = cv2.resize(f0,(w,h))
     g1 = cv2.flip(f,-1) # =0 v, >0 h, < 0: v and h
     g2 = cv2.cvtColor(g1,cv2.COLOR_BGR2GRAY)
     g3 = cv2.Canny(g2, 10,100)
     g4 = cv2.bitwise_not(g3)
     h,w,c = f.shape
     #print(f.shape)
     f2 = cv2.bitwise_and(g1,g1,mask=g4)
     return f2

counter = 0
def ProcessFrame(f):
     global counter
     #g = ProcessFrame1(f)
     fn = './imgs/frame-%04d.jpg' % counter
     g = cv2.rotate(f, cv2.ROTATE_90_CLOCKWISE)
     cv2.imwrite(fn,g)
     counter = counter + 1
     return g

if (ca.isOpened() == False):
     print("Error opening video stream or file")

while (ca.isOpened()):
     r,f = ca.read()
     if r == True:
         g = ProcessFrame(f)
         cv2.imshow("Video",g)
         ch = cv2.waitKey(15)
         if ch == ord('e'):
             break
     else:
         break

ca.release()
cv2.destroyAllWindows()
