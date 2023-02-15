import robot as rb

import random

R = rb.Robot(idx=1,name="Sunny")
# R.load() for short
R.vision.load()
R.greet()

fol1 = "."
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
print("Speak your name: ")
R.auditory.listen(secs)
txt = R.auditory.recognize()
txt = ' '.join(txt)
txt2 = txt.split(' ')[0]
print("txt2 = ", txt2)
R.motor.Say("Hello "+txt2)
r = input("Reward (value from -10 to 10)> ")
r = float(r)
R.basal.insert(action=txt,reward=r)
R.basal.learn()
print(R.basal.values())
print("Auditory: thoughts = ",R.auditory.thoughts)
print("Making Choice...")
action1 = R.basal.choose()
print("Chosen action action1 = ", action1)
R.motor.Say(action1)
R.vision.close_visualize()

