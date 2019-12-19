class Queue:
    def __init__(self):
        self.L = []
        self.undef = None
        return
    def Initialize(self):
        self.__init__()
        return
    def Push(self,item):
        self.L = [item] + self.L 
        return
    def Pop(self):
        if self.Empty():
            return self.undef
        item = self.L[-1] # car
        self.L = self.L[:-1] # cdr
        return item
    def Empty(self):
        return self.L == []

