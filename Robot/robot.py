import image2text as vi
import speech2text as au
import RL_learning as ba
import text2speech as sp

class Actuators:
    def __init__(self,agent=""):
        self.agent = agent
        return
    def Say(self,txt):
        print(self.agent,":",txt)
        sp.Speak(txt)
        return

class Robot:
    def __init__(self,idx,name):
        self.idx = idx
        self.name = name
        self.vision = vi.Image2Text()
        self.auditory = au.Speech2Text()
        self.basal = ba.RLLearn()
        self.motor = Actuators(self.name)
        return
    def load(self):
        self.vision.load()
        self.auditory.load()
        return
    def greet(self):
        s = "Hello, my name is "+self.name
        self.motor.Say(s)
        return
