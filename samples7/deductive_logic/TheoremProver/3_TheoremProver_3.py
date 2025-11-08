###################################################
# [1] Microsoft Copilot, a large language model
#
class Expr:
    def match(self, other, bindings=None):
        raise NotImplementedError

class Var(Expr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return f"${self.name}"
    def match(self, other, bindings=None):
        if bindings is None:
            bindings = {}
        if self.name in bindings:
            return bindings[self.name] == other
        bindings[self.name] = other
        return True

class Atom(Expr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
    def match(self, other, bindings=None):
        return isinstance(other, Atom) and \
               self.name == other.name

class Not(Expr):
    def __init__(self, operand):
        self.operand = operand
    def __repr__(self):
        return f"¬{self.operand}"
    def match(self, other, bindings=None):
        if not isinstance(other, Not):
            return False
        return self.operand.match(other.operand, \
                    bindings)

# Pattern: ¬¬X
X = Var("X")
pattern = Not(Not(X))

# Expression: ¬¬A
expr = Not(Not(Atom("Apple")))

# Match and extract bindings
bindings = {}
if pattern.match(expr, bindings):
    print("Matched!")
    print("Bindings:", bindings)
else:
    print("No match.")

#
###################################################
