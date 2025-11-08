# [1] Microsoft Copilot, a large language model

class Term:
    def match(self, other, bindings=None):
        raise NotImplementedError
    pass

class Const(Term):
    def __init__(self, name):
        self.name = str(name)
    def __repr__(self):
        return self.name
    def match(self, other, bindings=None):
        return self.name == other.name
    
class Var(Term):
    def __init__(self, name, value = None):
        self.name = name
        self.value = value
    def __repr__(self):
        if self.value is not None:
            return f"${self.name}/{self.value}"
        else:
            return f"${self.name}"
    def match(self, other, bindings=None):
        if bindings is None:
            bindings = {}
        if self.name in bindings:
            return bindings[self.name] == other
        bindings[self.name] = other
        return True

class unary:
    def __init__(self, name, x):
        self.name = name
        self.x = x
    def __repr__(self):
        return f"{self.name}({self.x})"
    def match(self, other, bindings=None):
        if not isinstance(other, unary) or \
           self.name != other.name:
            return False
        return self.x.match(other.x, bindings)

class binary:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    def __repr__(self):
        if self.name == "lambda":
            return f"(lambda {self.x} : {self.y})"
        if self.name == "app":
            return f"{self.x}({self.y})"
        else:
            return f"({self.x}) {self.name} ({self.y})"
    def match(self, other, bindings=None):
        if not isinstance(other, binary) or \
           self.name != other.name:
            return False
        return self.x.match(other.x, bindings) and\
               self.y.match(other.y, bindings)

app = lambda name, x,y: binary(name,x,y)
def abstract(expr, symbol):
    expr2 = app("lambda", symbol, expr)
    return expr2

def replace(x,y,z):
    return app("app",abstract(x,y),z)

def rewrite(expr, rules):
    for rule in rules:
        lhs,rhs = rule
        bindings = {}
        if lhs.match(expr, bindings):
            def substitute(term):
                if isinstance(term, Var):
                    return bindings.get(term.name, term)
                elif isinstance(term, unary):
                    return unary(term.name, \
                        substitute(term.x))
                elif isinstance(term, binary):
                    return binary(term.name, \
                        substitute(term.x),\
                        substitute(term.y))
                else:
                    return term
            return substitute(rhs),rule
    return expr,None
