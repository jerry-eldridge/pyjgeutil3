
def ptup(tup):
    value = tup
    if type(value) == type(()):
        value = f"{value[0]}:{value[1]}"
    return value

###############################################
# [1] "Code generated with the assistance of
# Microsoft Copilot (AI), April 2025."
#Attribution-NonCommercial-ShareAlike 4.0
#International Public License (CC BY-NC-SA 4.0)

# [2] modifications made by JGE.

def dynamic_reduce(hasse, types, \
        reduce_function, identity):
    # Step 1: Build dependencies (reverse
    # adjacency list)
    dependencies = {}
    dp_table = {}  # Workspace memory
    for lhs, rhs in hasse:
        if rhs not in dependencies:
            dependencies[rhs] = []
        dependencies[rhs].append(lhs)
        if lhs not in dependencies:
            dependencies[lhs] = []
            # Ensure all nodes are initialized
    print(f"dependencies:")
    K = list(dependencies.keys())
    for key in K:
        M = list(map(ptup, dependencies[key]))
        s = '['+','.join(M)+']'
        print(f"{ptup(key)} : {s}")
    print()
    # Step 2: Topological Sort to process nodes
    # in order
    def topological_sort(dependencies):
        sorted_nodes = []
        visited = set()
        def visit(node):
            if node in visited:
                return
            visited.add(node)
            for dep in dependencies.get(node, []):
                visit(dep)
            sorted_nodes.append(node)
        for node in dependencies.keys():
            visit(node)
        return sorted_nodes[::-1]
        # Reverse order for processing
    sorted_nodes = topological_sort(dependencies)
    sorted_nodes.reverse()
    print()
    print(f"Topological Sort:")
    for tup in sorted_nodes:
        value = ptup(tup)
        print(value)
    print()
    # Step 3: Initialize leaf nodes based on their type
    for key in types.items():
        node,node_type = key
        if not dependencies[key]:
            # No dependencies, this is a leaf
            dp_table[key] = identity if \
                node_type == v else key
                # Constants stay as-is
    # Step 4: Process nodes using reduce
    print("Process nodes:")
    for key in sorted_nodes:
        if key in dp_table:
            continue  # Already processed
        input_values = []
        for dep in dependencies[key]:
            if dep in dp_table:
                input_values.append(dp_table[dep])
        dp_table[key] = reduce_function(\
            input_values, identity)
        value = dp_table[key]
        value = ptup(value)
        print(f"Assign {ptup(key)} to {value};")
    print()
    return dp_table
#
#############################################

##############################################
# [2] JGE

class cons:
    def __init__(self, a,b, f):
        self.f = f # function
        self.a = a
        self.b = b
    def car(self): # projection operator 1
        return self.a
    def cdr(self): # projection operator 2
        return self.b
    def set_f(self, f):
        self.f = f
        return
    def get_f(self):
        return self.f
    def __repr__(self):
        return str(self)
    def __str__(self):
        sa = self.a
        sb = self.b
        if type(sa) == type(()):
            sa = sa[0]
        if type(sb) == type(()):
            sb = sb[0]
        return str(self.f(sa,sb))

class Monoid:
    def __init__(self,identity,func,\
                 domain_type):
        self.id = identity
        self.func = func
        self.domain_type = domain_type
    # Reduce Function Example: Summation
    def f(self,a,b):
        #print(f"reduce_function: a = {a}, b = {b}")
        if a == self.id and b == self.id:
            return self.id
        elif a ==  self.id:
            if type(b) == type([]):
                if len(b) == 0:
                    return self.id
                elif len(b) == 1:
                    return b[0]
                else:
                    return self.f(b[0],b[1:])

            return b
        elif b == self.id:
            if type(a) == type([]):
                if len(a) == 0:
                    return self.id
                elif len(a) == 1:
                    return a[0]
                else:
                    return self.f(a[0],a[1:])
            return a
        else:
            if type(a) == type([]):
                if len(a) == 0:
                    return self.f(self.id,b)
                elif len(a) == 1:
                    return self.f(a[0],b)
                else: 
                    return self.f(a[0],self.f(a[1:],b))
            if type(b) == type([]):
                if len(b) == 0:
                    return self.f(a,self.id)
                elif len(b) == 1:
                    return self.f(a,b[0])
                else:
                    return self.f(a,self.f(b[0],b[1:]))
            return (cons(a,b,self.func),c)

# variable for name of type 
c = '<val>' # constant
v = '<var>' # variable

