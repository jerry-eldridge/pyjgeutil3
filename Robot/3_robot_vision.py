import robot as rb

import random

R = rb.Robot(idx=1,name="Sunny")
# R.load() for short
R.vision.load()
#R.greet()

# Get image from webcam (video/audio)
R.vision.camera_open(camid=1)
R.vision.camera_read() # could do multiple reads
R.vision.camera_read() # could do multiple reads 
R.vision.camera_close()
c = R.vision.recognize()
print("recognized as c = ",c)
R.vision.visualize()
R.vision.close_visualize()
