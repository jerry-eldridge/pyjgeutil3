import image2text as vi
import speech2text as au
import RL_learning as ba

import random

class Robot:
    def __init__(self):
        self.vision = vi.Image2Text()
        self.auditory = au.Speech2Text()
        self.basal = ba.RLLearn()
        return
    def load(self):
        self.vision.load()
        self.auditory.load()
        return

R = Robot()
# R.load() for short
R.vision.load()

fol1 = "./"
L = R.vision.jpg_files(fol1)

fn = random.choice(L)
R.vision.readfn(fn)
c = R.vision.recognize()
print("recognized as c = ",c)
R.basal.insert(action=c,reward=3)
R.basal.learn()
print(R.basal.values())

fn = random.choice(L) # pick an image of me in library
R.vision.readfn(fn)
c = R.vision.recognize()
print("recognized as c = ",c)
R.vision.visualize()
r = input("Reward (value from -10 to 10)> ")
r = float(r)
R.basal.insert(action=c,reward=r)
R.basal.learn()
print(R.basal.values())

print("Vision: thoughts = ",R.vision.thoughts)

# Get image from webcam (video/audio)
R.vision.camera_open(camid=0)
R.vision.camera_read() # could do multiple reads 
R.vision.camera_close()
c = R.vision.recognize()
print("recognized as c = ",c)
R.vision.visualize()
r = input("Reward (value from -10 to 10)> ")
r = float(r)
R.basal.insert(action=c,reward=r)
R.basal.learn()
print(R.basal.values())

# Get image from webcam (video/audio)
R.auditory.load()
print("Input number of seconds to listen...")
secs = input("seconds> ")
secs = float(secs)
R.auditory.listen(secs)
txt = R.auditory.recognize()
txt = '. '.join(txt)
print("txt = ", txt)
r = input("Reward (value from -10 to 10)> ")
r = float(r)
R.basal.insert(action=txt,reward=r)
R.basal.learn()
print(R.basal.values())
print("Auditory: thoughts = ",R.auditory.thoughts)
R.vision.close_visualize()
