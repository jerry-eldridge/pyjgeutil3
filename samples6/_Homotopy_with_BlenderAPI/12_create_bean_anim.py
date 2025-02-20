import cv2
import glob

root = r"../3D_renders/myrender_JerryBeans_01/"
images = glob.glob(root+'*.jpg')
n_images = len(images)
print(f"n_images = {n_images}")

aspect = 1.85 # 35 mm 1.85 : 1 projection
height = int(500)
width = int(aspect*height)
fps = 24
duration = n_images / fps
print(f"duration = {duration} seconds")
sz = (width,height) # scale down the images to sz
fourcc = cv2.VideoWriter_fourcc(*'MJPG')
video = cv2.VideoWriter('./JerryBeans_01_anim.avi', fourcc, fps, sz)

for image in images:
    frame = cv2.imread(image)
    im2 = cv2.resize(frame, sz)
    cv2.imshow("result",im2)
    c = cv2.waitKey(15)
    video.write(im2)

video.release()
cv2.destroyAllWindows()
