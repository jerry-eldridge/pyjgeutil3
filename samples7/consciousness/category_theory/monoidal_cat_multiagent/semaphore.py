class Semaphore:
    def __init__(self):
        self.count = 0
    def lock(self):
        self.count = self.count + 1
    def unlock(self):
        if self.count > 0:
            self.count = self.count - 1
    def is_accessible(self):
        return self.count == 0

