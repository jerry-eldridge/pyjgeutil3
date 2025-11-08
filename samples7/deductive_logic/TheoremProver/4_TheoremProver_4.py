###############################################
# [1] Microsoft Copilot, a large language model
#
class Term:
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

class Predicate:
    def __init__(self, name, args):
        self.name = name
        self.args = args  # list of Term
    def __repr__(self):
        args_str = ", ".join(map(str, self.args))
        return f"{self.name}({args_str})"
    def match(self, other, bindings=None):
        if self.name != other.name or \
           len(self.args) != len(other.args):
            return False
        if bindings is None:
            bindings = {}
        for a, b in zip(self.args, other.args):
            if isinstance(a, Var):
                if a.name in bindings:
                    if bindings[a.name] != b:
                        return False
                else:
                    bindings[a.name] = b
            elif a != b:
                return False
        return True

def apply_modus_ponens(kb):
    new_facts = set()
    for p in kb:
        if isinstance(p, tuple) and \
           p[0] == "implies":
            antecedent, consequent = p[1], p[2]
            for fact in kb:
                if isinstance(fact,tuple):
                    continue
                bindings = {}
                if antecedent.match(fact, bindings):
                    instantiated = \
                        Predicate(consequent.name, \
                        [bindings.get(arg.name, arg) \
                        if isinstance(arg, Var) \
                        else arg for arg in \
                        consequent.args])
                    new_facts.add(instantiated)
    kb = kb | new_facts
    return kb
#
###############################################

# Based on [1] but different

x = Var("x")
Dirac = Const("Dirac")

kb = {
    ("implies",
     Predicate("Cat", [x]),
     Predicate("Cuddle", [x])),
    Predicate("Cat", [Dirac])
}
print(f"Before: kb = {kb}")
kb = apply_modus_ponens(kb)
print(f"After: kb = {kb}")

#
###############################################
