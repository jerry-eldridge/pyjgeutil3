################################################
# [1] Microsoft Copilot, a large language model
#
class Expr:
    def __eq__(self, other):
        return isinstance(other, Expr) and \
               self.__dict__ == other.__dict__

class Atom(Expr):
    def __init__(self, name):
        self.name = name
    def __repr__(self):
        return self.name
    def __eq__(self, other):
        return isinstance(other, Atom) and \
               self.name == other.name

class Not(Expr):
    def __init__(self, operand):
        self.operand = operand
    def __repr__(self):
        return f"¬{self.operand}"
    def __eq__(self, other):
        return isinstance(other, Not) and \
               self.operand == other.operand

class And(Expr):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    def __repr__(self):
        return f"({self.left} ∧ {self.right})"
    def __eq__(self, other):
        return isinstance(other, And) and \
               self.left == other.left and \
               self.right == other.right

def rewrite(expr, rules):
    for lhs, rhs in rules:
        if expr == lhs:
            return rhs
    return expr

# Example rule: Double negation elimination ¬¬A → A
A = Atom("A")
rule1 = (Not(Not(A)), A)

# Another rule: De Morgan ¬(A ∧ B) → (¬A ∨ ¬B)
B = Atom("B")
rule2 = (Not(And(A, B)), "DeMorgan")
    # Placeholder for now

expr = Not(Not(Atom("A")))
rules = [(Not(Not(Atom("A"))), Atom("A"))]

result = rewrite(expr, rules)
print("Before:", expr)
print("After:", result)

#
################################################
