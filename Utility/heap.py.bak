#[1] Introduction to Algorithms, Thomas H. Cormen,
# Charles E. Leiserson, Ronald L. Rivest, 6ed, 1992, The MIT Press
#
# We implement heaps from [1].
from math import floor
from copy import deepcopy

class Heap:
    def Parent(self,i):
        return int(floor(i/2))
    
    def Left(self,i):
        return 2*i + 1
    
    def Right(self,i):
        return 2*i + 2
    
    def __init__(self,A,compare):
        """
        A is a list and compare(x,y) return true or false
        such as greater(x,y) and less(x,y) defined by
        
        greater = lambda x,y: x > y
        less = lambda x,y: x < y
        Heap(A,greater)

        or use the unnamed lambda expression for compare:

        Heap(A,lambda x,y: x > y)

        You can later define compare and call BuildHeap
        or other routine that calls BuildHeap.
        """
        self.A = deepcopy(A)
        self.heapsize = 0
        self.compare = compare
        self.BuildHeap()
        return
    
    def Heapify(self,i):
        """
        A is a list and i its index. Will use
        Greater(x,y) = x > y to put greatest first
        and Greater(x,y) = x < y to least first.

        Heapify is recursive and will use the program
        stack.
        """
        l = self.Left(i)
        r = self.Right(i)
        if (l < self.heapsize) and (self.compare(self.A[l],self.A[i])):
            largest = l
        else:
            largest = i
        if (r < self.heapsize) and (self.compare(self.A[r],self.A[largest])):
            largest = r
        if not (largest == i):
            tmp = self.A[i]
            self.A[i] = self.A[largest]
            self.A[largest] = tmp
            self.A = self.Heapify(largest)
        return self.A

    def BuildHeap(self):
        self.heapsize = len(self.A)
        for i in range(int(floor(len(self.A)/2))-1,-1,-1):
            self.A = self.Heapify(i)
        return

    def HeapSort(self):
        """
        Sorts with the self.compare ordering from supremum
        (greatest) to infimum (lowest) using that
        self.compare relation. If you use x < y, it will
        sort from high to low. If you use x > y, it will
        sort from low to high.

        Eg,
        heap = Heap(A, lambda x,y: x < y)
        print heap.HeapSort()

        to sort highest to lowest and
        
        heap = Heap(A, lambda x,y: x > y)
        print heap.HeapSort()

        to sort from lowest to higest.
        """
        self.BuildHeap()
        self.heapsize = len(self.A)
        for i in range(len(self.A)-1,0,-1):
            tmp = self.A[0]
            self.A[0] = self.A[i]
            self.A[i] = tmp
            self.heapsize = self.heapsize - 1
            self.A = self.Heapify(0)
        return self.A

    def HeapExtract(self):
        """
        Eg, extracts the minimum (infimum)
        given the self.compare relation.
        
        heap = Heap(A, lambda x,y: x < y)
        val = heap.HeapExtract()
        print val # will be lowest

        heap = Heap(A, lambda x,y: x > y)
        val = heap.HeapExtract()
        print val # will be highest
        """
        if self.heapsize < 0:
            print "Error: heap underflow"
            return
        val = self.A[0]
        self.A[0] = self.A[self.heapsize-1]
        self.heapsize = self.heapsize - 1
        self.A = self.Heapify(0)
        return val

    def HeapInsert(self,key):
        self.heapsize = self.heapsize + 1
        i = self.heapsize-1
        self.A = self.A+[key]
        while (i > 0) and (not self.compare(self.A[self.Parent(i)],key)):
            self.A[i] = self.A[self.Parent(i)]
            i = self.Parent(i)
        self.A[i] = key
        return

