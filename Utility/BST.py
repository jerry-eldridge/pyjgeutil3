# [1] https://en.wikipedia.org/wiki/Binary_search_tree

def BST_inorder_traversal(node,callback):
    if node == None:
        return
    BST_inorder_traversal(node.C[0],callback)
    callback((node.key,node.value))
    BST_inorder_traversal(node.C[1],callback)
    return

def BST_insert(T,key,value):
    if (T is None):
        T = BST(key,value)
    elif key == T.key:
        T.value = value
    elif key < T.key:
        T.C[0] = BST_insert(T.C[0],key,value)
        T.C[0].parent = T
    else:
        T.C[1] = BST_insert(T.C[1],key,value)
        T.C[1].parent = T
    return T

class BST:
    def __init__(self,key=0,value=None,
                 left=None,right=None):
        self.key = key
        self.value = value
        self.C = [left,right]
        self.L = []
        self.parent = None
        return
    def __str__(self):
        s = 'BST(key=%s,value=%s,left=%s,right=%s)' % (str(self.key),
            str(self.value),str(self.C[0]),str(self.C[1]))
        return s
    def insert(self,key,value):
        self = BST_insert(self,key,value)
        return
    def search(self,key,node):
        new_node = node
        while (new_node is not None):
            current_node = new_node
            if key < current_node.key:
                d = 0 # LEFT
            else:
                d = 1 # RIGHT
            new_node = current_node.C[d]
        return (d,current_node)
    def is_BST(self,minKey,maxKey):
        if self is None:
            return True
        if (self.key < minKey) or (self.key > maxKey):
            return False
        if self.C[0] is not None:
            flag1 = self.C[0].is_BST(minKey,self.key-1)
        else:
            flag1 = True
        if not flag1:
            return flag1
        if self.C[1] is not None:
            flag2 = self.C[1].is_BST(self.key+1,maxKey)
        else:
            flag2 = True
        return flag1 and flag2
    def traverse_callback(self,callback):
        BST_inorder_traversal(self,callback)
        return
    def build(self,L):
        self = None
        for i in range(len(L)):
            key,value = L[i]
            self = BST_insert(self,key,value)
        return self
    def traverse(self):
        L = []
        def Accum_M(val):
            L.append(val)
            return L
        self.traverse_callback(Accum_M)
        self.L = L
        return self.L
    def find_min(self):
        current_node = self
        while current_node.C[0]:
            current_node = current_node.C[0]
        return current_node
    def replace_node_in_parent(self, newval=None) -> None:
        if self.parent:
            if self == self.parent.C[0]:
                self.parent.C[0] = newval
            else:
                self.parent.C[1] = newval
        if newval:
            new_value.parent = self.parent
    def delete(self,key):
        if key < self.key:
            self.C[0].delete(key)
            return
        if key > self.key:
            self.C[1].delete(key)
            return
        if (self.C[0] is not None) and \
           (self.C[1] is not None):
            succ = self.C[1].find_min()
            self.key = succ.key
            succ.delete(succ.key)
        elif (self.C[0] is not None):
            self.replace_node_in_parent(self.C[0])
        elif (self.C[1] is not None):
            self.replace_node_in_parent(self.C[1])
        else:
            self.replace_node_in_parent(None)
        return
