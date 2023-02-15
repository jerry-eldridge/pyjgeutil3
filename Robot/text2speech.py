import pyttsx3

def Speak(txt):
    engine = pyttsx3.init()
    engine.say(txt)
    engine.runAndWait()
    return
