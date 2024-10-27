import cv2
import glob
import numpy as np

root_render = r"C:/JGE_Universes/render3/"

bkg = cv2.imread("./object_bkg.jpg",1)

root = root_render
images = glob.glob(root+'*.png')

scale = 50
sz = (16*scale, 9*scale) # scale down the images to sz
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
fps = 30
video = cv2.VideoWriter('./algebra-disc.avi', \
                        fourcc,fps,sz)
if not video.isOpened():
    print(f"Error opening video")

d = lambda A,B: np.linalg.norm(np.array(B)-\
                    np.array(A))
def create_image(bkg, im2):
    bkg2 = bkg.copy()
    
    bkg2 = cv2.resize(bkg2, sz)
        
    green_screen = [0,177,64] # R,G,B
    sh = bkg2.shape
    green_screen_BGR = [green_screen[2],green_screen[1],
                        green_screen[0]]
    green_screen_BGR = np.array(green_screen_BGR)
    epsilon = 70    
    
    mask = np.linalg.norm(im2 - \
            green_screen_BGR, axis=-1) > epsilon
    bkg2[mask] = im2[mask]
    
    cv2.imshow("result",bkg2)
    ch = cv2.waitKey(15)
    return bkg2

for image in images:
    frame = cv2.imread(image)
    im2 = cv2.resize(frame, sz)
    bkg2 = create_image(bkg, im2)
    cv2.imshow("result",bkg2)
    c = cv2.waitKey(15)
    video.write(bkg2)

video.release()
cv2.destroyAllWindows()



