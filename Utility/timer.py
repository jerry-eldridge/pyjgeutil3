import time

class Timer:
    def __init__(self):
        self.secs = time.clock()
        return
    def tic(self):
        self.secs = time.clock()
        return
    def toc(self):
        secs = time.clock() - self.secs
        return secs
