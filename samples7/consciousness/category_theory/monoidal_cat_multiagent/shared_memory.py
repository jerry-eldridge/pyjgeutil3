from copy import deepcopy

class SharedMemory:
    def __init__(self, L):
        self.L = deepcopy(L)
        self.n = len(self.L)
    def set(self, i, val):
        if 0 <= i and i < self.n-1:
            self.L[i] = val
    def get(self, i):
        if 0 <= i and i < self.n-1:
            return self.L[i]
        return None

