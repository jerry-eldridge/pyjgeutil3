import pyttsx3

# [1] Microsoft Copilot, a large language model

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set properties (optional)
engine.setProperty('rate', 150)
# Speed of speech (words per minute)
engine.setProperty('volume', 1.0)
# Volume (0.0 to 1.0)

# Text to be spoken
x = "We have cats Dirac, Erwin, Niels, and Emmy."

# Speak the text
engine.say(x)
engine.runAndWait()
