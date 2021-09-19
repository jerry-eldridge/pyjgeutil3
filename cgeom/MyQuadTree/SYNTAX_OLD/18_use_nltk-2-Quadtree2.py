import nltk
s = """
QT := Q LPAREN QT COMMA QT COMMA QT COMMA QT RPAREN
QT := P LPAREN PTS RPAREN
QT := N LPAREN RPAREN
Q := q
P := p
N := n
PTS := LBRACK PLIST RBRACK
PLIST := PLIST COMMA PT | PT
PT := LPAREN IDX COMMA QNAME RPAREN
IDX := INTEGER
QNAME := QUOTE NAME QUOTE
QUOTE := !
NAME := NAME CHAR | CHAR
LBRACK := [
RBRACK := ]
LPAREN := (
RPAREN := )
COMMA := ,
REAL := SIGN REAL
REAL := INTEGER | INTEGER DOT | INTEGER DOT INTEGER
SINTEGER := SIGN INTEGER | INTEGER
INTEGER := INTEGER INTEGER
DOT := .
SIGN := -
INTEGER := 0
INTEGER := 1
INTEGER := 2
INTEGER := 3
INTEGER := 4
INTEGER := 5
INTEGER := 6
INTEGER := 7
INTEGER := 8
INTEGER := 9
CHAR := a
CHAR := b
CHAR := c
CHAR := d
CHAR := e
"""
s = s.replace(":=", "->")
lines = s.split('\n')
M = []
for line in lines:
    if len(line) <= 3:
        continue
    a,b = line.split('->')
    a = a.strip()
    b = b.strip()
    L = b.split(' ')
    if len(L) == 1:
        c = L[0]
        if c == c.lower():
            c = "'%s'" % c
        b = c
    s2 = '%s -> %s' % (a,b)
    M.append(s2)
s = '\n'.join(M)
g = nltk.CFG.fromstring(s)
parser = nltk.ChartParser(g)
ss = """
q(
    n(),
    n(),
    n(),
    n()
)
"""
ss = """
q(
    q(
        p([(1,!abc!),(2,!cad!)]),
        n(),
        n(),
        n()
    ),
    p([(3,!aa!)]),
    n(),
    n()
)
"""

ss = ss.replace(" ","")
ss = ss.replace("\t","")
ss = ss.replace("\n","")
print(ss)
sent = list(ss)
print(sent)
Alpha = list(parser.parse(sent))
if len(Alpha) < 1:
    print("Does not parse")
else:
    tree = Alpha[0]
    print(tree)
