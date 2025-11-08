
# [1] Microsoft Copilot, a large language model

LEXICAL_RULES = {
    "start" : "START_PROG",
    ":=": "ASSIGN",
    "+": "PLUS",
    "<": "LT",
    ">": "GT",
    "<=": "LE",
    ">=": "GE",
    "==": "EQ",
    "while": "WHILE",
    "do": "DO",
    "}": "END",
    ";": "SEMICOLON",
    "print":"PRINT",
    ".":"PERIOD",
    "finish":"FINISH",
    "if":"IF",
    "else":"ELSE",
    "{":"BEGIN",
    "\"":"QUOTE",
}

def lexer(raw_tokens):
    token_stream = []
    value_stream = []
    quotes = False
    for tok in raw_tokens:
        if tok == "\"":
            quotes = not quotes
            token_stream.append("QUOTE")
            value_stream.append("QUOTE")
        elif tok in LEXICAL_RULES and not quotes:
            token_stream.append(LEXICAL_RULES[tok])
            value_stream.append(LEXICAL_RULES[tok])
        elif tok.isdigit() and not quotes:
            token_stream.append("NUM")
            value_stream.append(float(tok))
        elif tok.isidentifier() and not quotes:
            token_stream.append("NAME")
            value_stream.append(tok)
        elif quotes:
            token_stream.append("STRING")
            value_stream.append(tok)
    return token_stream,value_stream

