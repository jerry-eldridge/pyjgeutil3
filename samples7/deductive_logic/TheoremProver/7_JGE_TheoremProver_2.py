import JGE_model as mod

Var = mod.Var
Const = mod.Const
replace = mod.replace
rewrite = mod.rewrite
app = mod.app

Alice = Var("Alice")
Bob = Var("Bob")
a = Var("a")
b = Var("b")
w = Var("w")
x = Var("x")
y = Var("y")
z = Var("z")
op = Var("op")
op2 = Var("op2")
Eq = lambda x,y: app("=",x,y)
Lm = lambda x: lambda y: app("l*",x,y)
Rm = lambda x: lambda y: app("r*",y,x)
Ld = lambda x: lambda y: app("L/",x,y)
Rd = lambda x: lambda y: app("R/",y,x)
R = lambda x,y,z: replace(x,y,z)

rules = [
    *[(Eq(app(op2,z,x),app(op2,z,obj)),
     Eq(app(op2,z,x),app(op2,z,a))) \
     for obj in [Alice, Bob]],
    
    *[(Eq(app(op2,z,x),app(op2,z,a)),
     Eq(app(op,z,x),
        app(op,z,a))) \
     for op2 in ['+','-','*','/']],
    
    (Eq(app(op,z,a),app(op,z,x)),
     R(Eq(app(op,z,x),app(op,z,y)),y,a)),
    
    (Eq(app(op,z,x),app(op,z,y)), Eq(x,y)),
    
    (R(Eq(app(op,z,x),app(op,z,y)),y,a),
     R(Eq(x,y),y,a)),
     
    (R(Eq(x,y),y,a),Eq(x,a)),
     
    (Eq(x,z),Const("Done")),
    
    ]

expr = Eq(app("+",w,app("*",z,x)),
          app("+",w,app("*",z,Bob)))
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
    print("<derives>", new_expr)
    print(f" used rule:: {rule[0]} <turnstile> {rule[1]}")
    expr = new_expr
