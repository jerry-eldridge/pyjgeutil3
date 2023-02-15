import robot as rb

import random

R = rb.Robot(idx=1,name="Sunny")
# R.load() for short
R.vision.load()
#R.greet()

R.vision.readfn("./shape-20220606-01.jpg")
c = R.vision.recognize()
print("recognized as c = ",c)
ch = R.vision.visualize(wn="result",ms=-1)

R.vision.readfn("./shape-20220606-02.jpg")
c = R.vision.recognize()
print("recognized as c = ",c)
ch = R.vision.visualize(wn="result",ms=-1)

R.vision.close_visualize()
