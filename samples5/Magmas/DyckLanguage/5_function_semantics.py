import grammar_obj2 as gob
import process_tags as pt
import process_semantics as ps

# Rules is of form:
# <non-terminal> := <non-terminal> <non-terminal>
# <non-terminal> := <terminal>
# which is of the form:
# (<non-terminal>, [<non-terminal>,<non-terminal>])
# (<non-terminal>, [<terminal>])
# grammar = [rules,example,non_terminals]
# The first rule non-terminal must be what the
# grammar defines. (Below it is "Currency").
def Demo1():
##    # [1] https://en.wikipedia.org/wiki/Dyck_language
##    # S -> epsilon | "[" S "]" S
##    grammar = [
##        [
##             ("S",["Lbracket","S1"]),
##                     # start
##             ("S1",["S","S2"]),
##             ("S2", ["Rbracket","S"]),
##             ("S", ["e"]),
##             ("Lbracket", ["["]),
##             ("Rbracket", ["]"]),
##        ],
##        [], # this is an example tokens
##        None # this is non_terminals below
##        ]
    
##    # Let us adapt the Dyck language to be the
##    # more familiar language:
##    # S -> epsilon | S "(" S ")"
##    eSigma = ["x","y","z","f","g","h","a","b","c"]
##    grammar = [
##        [
##             ("S",["S","S1"]),
##                     # start
##             ("S1",["Lparen","S2"]),
##             ("S2", ["S","Rparen"]),
##             *[("S",[c]) for c in eSigma],
##             ("S", ["e"]),
##             ("Lparen", ["("]),
##             ("Rparen", [")"]),
##        ],
##        [], # this is an example tokens
##        None # this is non_terminals below
##        ]

    # Let us adapt the Dyck language to be the
    # more familiar language:
    # S -> epsilon | S "(" S ")"
    alpha = [chr(c) for c in range(ord('a'),ord('z')+1)]
    digit = [chr(c) for c in range(ord('0'),ord('9')+1)]
    alphadigit = alpha + digit
    grammar = [
        [
             ("S",["S","S1"]),
                     # start
             ("S1",["Lparen","S2"]),
             ("S2", ["S","Rparen"]),
             ("S", ["Alpha","S"]),
             ("S", ["S","AlphaDigit"]),
             *[("S",[c]) for c in alpha], 
             *[("Alpha",[c]) for c in alpha],
             *[("AlphaDigit",[c]) for c in alphadigit],
             ("Lparen", ["("]),
             ("Rparen", [")"]),
        ],
        [], # this is an example tokens
        None # this is non_terminals below
        ]
    
    non_terminals = []
    for tup in grammar[0]:
        LHS,RHS = tup
        if LHS not in non_terminals:
            non_terminals.append(LHS)
    print(f"non_terminals = {non_terminals}")
    grammar[2] = non_terminals

    tokenizer_word = lambda s: list(s)
    detoken_word = lambda toks: ''.join(toks)
    tokenizer_sent = lambda s: s.split(' ')
    detoken_sent = lambda toks: ' '.join(toks)

    L1 = gob.Language('DyckLanguage', grammar)
    ##L1.interpreter(tokenizer_word,detoken_word,
    # show=True)

    from math import sqrt,sin,cos
    def myfunc(x):
        y = x*x
        return y
    f = lambda x: x + 1
    g = lambda x: x * 2
    h = lambda y: lambda x: x + y
    ps.set_function("myfunc",myfunc)
    ps.set_function("sin",sin)
    ps.set_function("cos",cos)
    ps.set_function("f",f)
    ps.set_function("g",g)
    ps.set_function("h",h)
    ps.set_var("x",100)
    ps.set_var("y",200)

    words = ["f(x)","f(g(x))", "h(g(x))(y)",
             "sin(cos(x))"]
    
    for word in words:
        print(f"parsing word = '{word}'")
        t,derivation,tags = L1.parse(word,
            tokenizer_word,detoken_word)
        print(f"t = {t}")
        #print(f"derivation = {derivation}")
        if t == 'accept':
            #print(f"tags = {tags}")
            p = pt.process_tags(tags, debug=False)
            print(f"p = {p}")
            y = ps.process(p)
            print(f"process(p) = {y}")
    return

Demo1()


