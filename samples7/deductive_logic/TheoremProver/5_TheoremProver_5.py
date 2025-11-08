################################################
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
    
class Func:
    def __init__(self, name, arg):
        self.name = name
        self.arg = arg
    def __repr__(self):
        return f"{self.name}({self.arg})"
    def match(self, other, bindings=None):
        if not isinstance(other, Func) or \
           self.name != other.name:
            return False
        return self.arg.match(other.arg, bindings)

def rewrite(expr, rules):
    for lhs, rhs in rules:
        bindings = {}
        if lhs.match(expr, bindings):
            def substitute(term):
                if isinstance(term, Var):
                    return bindings.get(term.name, term)
                elif isinstance(term, Func):
                    return Func(term.name, \
                        substitute(term.arg))
                else:
                    return term
            return substitute(rhs)
    return expr

x = Var("x")
A = Const("A")
rules = [(Func("f", Func("f", x)), Func("f", x))]

expr = Func("f", Func("f", Func("f", A)))
print("Start:", expr)

while True:
    new_expr = rewrite(expr, rules)
    if new_expr == expr:
        break
    print("→", new_expr)
    expr = new_expr

