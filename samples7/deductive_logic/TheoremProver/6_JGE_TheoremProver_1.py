# [1] Microsoft Copilot, a large language model

class Term:
    def match(self, other, bindings=None):
        raise NotImplementedError
    pass

class Const(Term):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name

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
        return f"{self.name}({self.x},{self.y})"
    def match(self, other, bindings=None):
        if not isinstance(other, binary) or \
           self.name != other.name:
            return False
        return self.x.match(other.x, bindings) and\
               self.y.match(other.y, bindings)

class equals:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    def __repr__(self):
        return f"{self.x} = {self.y}"
    def match(self, other, bindings=None):
        if not isinstance(other, equals) or \
           self.name != other.name:
            return False
        return self.x.match(other.x, bindings) and\
               self.y.match(other.y, bindings)

class add:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}+{self.y})"
    def match(self, other, bindings=None):
        if not isinstance(other, add) or \
           self.name != other.name:
            return False
        return self.x.match(other.x, bindings) and\
               self.y.match(other.y, bindings)

class sub:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}-{self.y})"
    def match(self, other, bindings=None):
        if not isinstance(other, sub) or \
           self.name != other.name:
            return False
        return self.x.match(other.x, bindings) and\
               self.y.match(other.y, bindings)
    
class mul:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}*{self.y})"
    def match(self, other, bindings=None):
        if not isinstance(other, mul) or \
           self.name != other.name:
            return False
        return self.x.match(other.x, bindings) and\
               self.y.match(other.y, bindings)

class div:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
    def __repr__(self):
        return f"({self.x}/{self.y})"
    def match(self, other, bindings=None):
        if not isinstance(other, div) or \
           self.name != other.name:
            return False
        return self.x.match(other.x, bindings) and\
               self.y.match(other.y, bindings)

class rep:
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
    def __repr__(self):
        return f"{self.name}({self.x},{self.y},{self.z})"
    def match(self, other, bindings=None):
        if not isinstance(other, rep) or \
           self.name != other.name:
            return False
        return self.x.match(other.x, bindings) and\
               self.y.match(other.y, bindings) and\
               self.z.match(other.z, bindings)

def rewrite(expr, rules):
    for rule in rules:
        lhs,rhs = rule
        bindings = {}
        if lhs.match(expr, bindings):
            def substitute(term):
                if isinstance(term, Var):
                    return bindings.get(term.name, term)
                elif isinstance(term, binary):
                    return binary(term.name, \
                        substitute(term.x),\
                        substitute(term.y))
                else:
                    return term
            return substitute(rhs),rule
    return expr,None

v = Var("v")
w = Var("w")
x = Var("x")
y = Var("y")
z = Var("z")
Eq = lambda x,y: equals("Eq",x,y)
Lm = lambda x: lambda y: mul("Lm",x,y)
Rm = lambda x: lambda y: mul("Rm",y,x)
Ld = lambda x: lambda y: div("Ld",x,y)
Rd = lambda x: lambda y: div("Rd",y,x)
R = lambda x,y,z: rep("rep",x,y,z)

rules = [
    (Eq(Rm(z)(w),Rm(z)(x)),
     R(Eq(Rm(z)(x),Rm(z)(y)),y,w)),
    (Eq(Rm(z)(x),Rm(z)(y)), Eq(x,y)),
    (R(Eq(Rm(z)(x),Rm(z)(y)),y,w), R(Eq(x,y),y,w)),
    (R(Eq(x,y),y,w),Eq(x,w)),
    (Eq(x,z),Const("Done"))
    ]

expr = Eq(Rm(z)(x),Rm(z)(w))
print("Start:", expr)

Sigma = []
while True:
    Sigma.append(str(expr))
    yn = input("quit?>")
    if yn == 'q':
        break
    new_expr,rule = rewrite(expr, rules)
    if str(new_expr) in Sigma:
        break
    print("→", new_expr)
    print(f" used rule = {rule[0]} ⊢ {rule[1]}")
    expr = new_expr
