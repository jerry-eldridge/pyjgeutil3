import grammar_obj2 as gob

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
    # [1] https://en.wikipedia.org/wiki/Dyck_language
    # S -> epsilon | "[" S "]" S
    grammar = [
        [
             ("S",["Lbracket","S1"]),
                     # start
             ("S1",["S","S2"]),
             ("S2", ["Rbracket","S"]),
             ("S", ["e"]),
             ("Lbracket", ["["]),
             ("Rbracket", ["]"]),
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
    L1.run("[[e]e][e]e",
        tokenizer_word,detoken_word,show=True)
    return

Demo1()


