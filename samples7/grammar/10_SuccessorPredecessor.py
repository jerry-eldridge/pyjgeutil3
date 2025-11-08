import grammar_obj2 as gob
import arithmetic as ar
from copy import deepcopy

def OnesComplement(A):
    B = list([ar.Not(b) for b in A])
    return B
def TwosComplement16(A16):
    B16 = OnesComplement(A16)
    Cin = 0
    One = [0]*16
    One[15] = 1
    C16,Cout = ar.RCA16(B16,One,Cin)
    return C16
def inc(A):
    Cin = 0
    One = [0]*16
    One[15] = 1
    B,Cout = ar.RCA16(A,One,Cin)
    return B
def dec(A):
    Cin = 0
    One = [0]*16
    One[15] = 1
    MinusOne = TwosComplement16(One)
    B,Cout = ar.RCA16(A,MinusOne,Cin)
    return B
def mov(A):
    B = deepcopy(A)
    return B

def Demo1():
    # Note that it is now with [ and ] not ( and )
    # Note N denotes "Number" and F denotes "function"
    # and "p" is "pred" or "predecessor" and
    # "s" is "succ" or "successor". Note for example
    # "ps" is "pred(succ(ground))" and
    # "psss" is "pred(succ(succ(succ(ground))))". "p"
    # and "s" are unary operators and we could always
    # use "-" for "p" and "+" for "s". 
    grammar1 = [
         [ # R, production rules
         ("N",list("NF")), # start
         ("F",list("p")),
         ("F",list("s")),
         ("N",list("p")),
         ("N",list("s")),
         ],
         list("psss"), # I, characters
         ["N","F"] # N, nonterminal symbols
                ]

    tokenizer_word = lambda s: list(s)
    detoken_word = lambda toks: ''.join(toks)
    tokenizer_sent = lambda s: s.split(' ')
    detoken_sent = lambda toks: ' '.join(toks)

    L1 = gob.Language('grammar1', grammar1)
    #L1.interpreter(tokenizer_word,detoken_word,show=True)
    #L1.run("bba",
    #    tokenizer_word,detoken_word,show=True)
    tokenizer = tokenizer_word
    detoken = detoken_word
    grammar0 = L1.grammar
    show = True
    if show:
       print(f"grammar: {L1.name} = {grammar0}")
    else:
       print(f"language: {L1.name} = ::{L1.s}::")
    done = False
    print("Enter 'Q:' to quit")
    while not done:
       line = input("L> ")
       line = line.strip(" ")
       if len(line) == 0:
            continue
       if line == 'Q:':
            done = True
            break
       t,derivation,tags = L1.parse(line,
            tokenizer,detoken)
       if len(derivation) > 0:
            print(f"Derivation:\n{derivation}")
            print(("tags: ", tags))
       print(t)
       if t == 'accept':
           toks = tokenizer(line)
           #print(f"toks = {toks}")
           A16 = [0]*16
           B16 = [0]*16
           for x in toks:
               if x == 's':
                   B16 = inc(A16)
                   A16 = mov(B16)
               elif x == 'p':
                   B16 = dec(A16)
                   A16 = mov(B16)
           print(''.join(list(map(str,A16))))
    
Demo1()


