import grammar_obj2 as gob

def Demo1():
    # Note that it is now with [ and ] not ( and )
    grammar1 = [
         [ # R, production rules
         ("T",list("SA")), # start
         ("S",list("SS")),
         ("S",list("b")),
         ("A",list("a"))
         ],
         list("bbba"), # I, characters
         ["T","S","A"] # N, nonterminal symbols
                ]
    grammar2 = [
         [
             ("S",["NP","VP"]), # start
             ("VP", ["VP","PP"]),
             ("VP",["V","NP"]),
             ("VP",["eats"]),
             ("PP",["P","NP"]),
             ("NP",["Det","N"]),
             ("NP",["she"]),
             ("V",["eats"]),
             ("P",["with"]),
             ("N",["pizza"]),
             ("N",["spoon"]),
             ("Det",["a"])],
        "she eats a pizza with a spoon".split(' '),
        ["S","VP","PP","NP","V","P","N","Det"]
        ]

    tokenizer_word = lambda s: list(s)
    detoken_word = lambda toks: ''.join(toks)
    tokenizer_sent = lambda s: s.split(' ')
    detoken_sent = lambda toks: ' '.join(toks)

    L1 = gob.Language('grammar1', grammar1)
    ##L1.interpreter(tokenizer_word,detoken_word,show=True)
    L1.run("bba",
        tokenizer_word,detoken_word,show=True)

    L2 = gob.Language('grammar2', grammar2)
    #L2.interpreter(tokenizer_sent,detoken_sent,show=True)
    L2.run("a fish eats with a fork",
        tokenizer_sent,detoken_sent,show=True)

    L3 = gob.Language().KleeneStar(['x','y'])
    #L3.interpreter(tokenizer_word,detoken_word)
    L3.run("xyyxxx",
        tokenizer_word,detoken_word,show=True)

    L4 = gob.Language().StringGrammar('a')
    #L4.interpreter(tokenizer_word,detoken_word)
    L4.run("aa",
        tokenizer_word,detoken_word,show=True)
    L4.run("a",
        tokenizer_word,detoken_word,show=True)

    L5 = L3 | L4
    #L5.interpreter(tokenizer_word,detoken_word)
    L5.run("xaa",
        tokenizer_word,detoken_word,show=True)
    L5.run("xxa",
        tokenizer_word,detoken_word,show=True)
    L5.run("xyx",
        tokenizer_word,detoken_word,show=True)
    L5.run("a",
        tokenizer_word,detoken_word,show=True)

    L6 = L3 + L4
    #L6.interpreter(tokenizer_word,detoken_word)
    L6.run("xyxa",
        tokenizer_word,detoken_word,show=True)
    L6.run("xa",
        tokenizer_word,detoken_word,show=True)

    L7 = gob.Language().Word("apple")
    L7.run("apple",
        tokenizer_word,detoken_word,show=True)
    L7.run("aapple",
        tokenizer_word,detoken_word,show=True)
    #L7.interpreter(tokenizer_word,detoken_word)
    return

def Demo2():
    tokenizer_word = lambda s: list(s)
    detoken_word = lambda toks: ''.join(toks)
    tokenizer_sent = lambda s: s.split(' ')
    detoken_sent = lambda toks: ' '.join(toks)

    gbL = gob.Language
    gbKS = gob.Language().KleeneStar
    gbSG = gob.Language().StringGrammar
    gbW = gob.Language().Word
    
    Run_L_0 = lambda L,s: L.run(s,
                tokenizer_word, detoken_word,
                show=True)
    Int_L = lambda L: L.interpreter(
                tokenizer_word, detoken_word,
                show=False)

    def slow_parse_L(L,s):
        accept = True
        for i in range(len(s)):
            u = s[:i+1]
            t,derivation,tags = L.parse(u,
                tokenizer_word,detoken_word)
            accept = t == "accept"
            if accept:
                print((str(L),t,u))
            else:
                print((str(L),t))
        return

    #Run_L = run_L_0
    Run_L = slow_parse_L

    digits_binary = list("01")
    L_binary = gbKS(digits_binary)
    L_binary.name = "<binary>"
    #Int_L(L_binary)
    Run_L(L_binary,"01010101100")
    Run_L(L_binary,"01010101100")
    Run_L(L_binary,"02010140670801")
    
    digits_decimal = list("0123456789")
    L_whole = gbKS(digits_decimal)
    L_whole.name = "<whole>"
    #Int_L(L_whole)
    Run_L(L_whole,"02010140670801")
    Run_L(L_whole,"-6230")

    L_minus = gbSG('-')
    L_minus.name = "<minus>"
    L_integer = L_whole | (L_minus + L_whole)
    L_integer.name = "<integer>"
    
    #Int_L(L_decimal)
    Run_L(L_integer,"-6230")
    Run_L(L_integer,"423599")
    
    L_dot = gbW('.')
    L_dot.name = "<dot>"
    F1 = L_integer
    F2 = L_dot | (L_dot + L_whole)
    L_real = F1 | F1 + F2
    L_real.name = "<real>"
    #Int_L(L_real)
    M = ["50","1.123","-123.","-123.45678",
         "0.123","-0.123"]
    for s in M:
        Run_L(L_real, s)

    L_comma = gbW(",")
    L_comma.name = "<comma>"
    L_cmpt = L_real + L_comma + L_real
    L_lparen = gbW("<")
    L_lparen.name = "<lparen>"
    L_rparen = gbW(">")
    L_rparen.name = "<rparen>"
    L_2D_pt = L_lparen + L_cmpt + L_rparen
    L_2D_pt.name = "<point2d>"
    M = ["<4,1.123>","<-123.,-123.45678>",
         "<0.123,-0.123>"]
    for s in M:
        Run_L(L_2D_pt, s)

    return

#Demo1()
Demo2()

