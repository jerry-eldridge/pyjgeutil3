##[1] https://en.wikipedia.org/wiki/CYK_algorithm
##
##[2] @book{Schalkoff92,
##author = "Schalkoff, Robert",
##title = "Pattern Recognition: Statistical, Structural, and Neural Approaches",
##publisher = "John Wiley & Sons, Inc.",
##year = "1992"
##}
##
##[3] @book{Brookshear89,
##author = "Brookshear, J. Glenn",
##title = "Theory of Computation: Formal Languages, Automata, and Complexity",
##publisher = "The Benjamin-Cummings Publishing Company, Inc.",
##year = "1989"
##}
##
##[4] @book{Bird09,
##author = "Bird, Steven  and  Klein, Ewan  and  Loper, Edward",
##title = "Natural Language Processing with Python",
##publisher = "OReilly",
##year = "2009"
##}
##
## 20210806 - Grammar and Language - Parsing Context Free Grammars with CYK algorithm

import numpy as np

from copy import deepcopy

# https://en.wikipedia.org/wiki/CYK_algorithm
def CYK(grammar):
     TT = 1
     FF = 0
     R = grammar[0]
     I = grammar[1]
     N = grammar[2]
     n = len(I)
     r = len(N)
     P = np.zeros((n+1,n+1,r+1))
     #print("P.shape = ",P.shape)
     for s in range(1,n+1):
         for v in range(len(R)):
             rule = R[v]
             flag = len(rule[1]) == 1 and rule[1][0] == I[s-1]
             if not flag:
                 continue
             a = N.index(R[v][0])+1
             P[1,s,a] = TT
             #print(rule)
     #print("here")
     for L in range(2,n+1):
         for s in range(1,n-L+1+1):
             for p in range(1,L-1+1):
                 for v in range(len(R)):
                     rule = R[v]
                     flag1 = len(rule[1]) == 2
                     flag2 = set(rule[1]) <= set(N)
                     flag = flag1 and flag2
                     if not flag:
                         continue

                     a = N.index(R[v][0])+1
                     b = N.index(rule[1][0])+1
                     c = N.index(rule[1][1])+1
                     #print(rule)
                     if P[p,s,b] == TT and P[L-p,s+p,c] == TT:
                         P[L,s,a] = TT
     if P[n,1,1] == TT:
         M = True
     else:
         M = False
     return M, P, N

def Display(P):
     I,J,K = P.shape
     for i in range(1,I):
         M_i = []
         for j in range(1,J):
             M_ij = []
             for k in range(1,K):
                 if P[i,j,k]:
                     M_ij.append(N[k-1])
             M_i.append(M_ij)
         print((i,M_i))
     print()
     return

def Parse(grammar,
          detoken=lambda toks: ' '.join(toks)):
     flag,P, N = CYK(grammar)
     s = ''
     if not flag:
         s = f"'{detoken(grammar[1])}'"
         return False,s
     else:
         #print("It parses.")
         I,J,K = P.shape
         M = []
         for i in range(1,I):
             M_i = []
             for j in range(1,J):
                 M_ij = []
                 for k in range(1,K):
                     if P[i,j,k]:
                         M_ij.append(N[k-1])
                 M_i.append(M_ij)
             M.append(M_i)
         try:
             tag = list(zip(grammar[1],M[0]))
             #print(tag)
         except:
             s = f"It parses but something went wrong with tag."
     return True,s

def ProcessRules(rules, i, start0, start):
     rules2 = []
     LHS,RHS = rules[0]
     if LHS == start0:
          LHS = start
     if len(RHS) == 2:
          A,B = RHS
          A = (A,i)
          B = (B,i)
          RHS = [A,B]
     rule = (LHS,RHS)
     rules2.append(rule)
     for rule in rules[1:]:
          LHS,RHS = rule
          if LHS == start0:
               LHS = start
          else:
               LHS = (LHS,i)
          if len(RHS) == 2:
               A,B = RHS
               A = (A,i)
               B = (B,i)
               RHS = [A,B]
          rule2 = (LHS,RHS)
          rules2.append(rule2)
     return rules2

def ProcessSymbols(syms, i):
     syms2 = list([(t,i) for t in syms])
     return syms2

def GrammarUnion(grammar1,grammar2,start="S"):
     idx1 = 1
     idx2 = 2
     rules1,sent1,syms1 = grammar1
     rules2,sent2,syms2 = grammar2
     syms1 = ProcessSymbols(syms1,idx1)     
     syms2 = ProcessSymbols(syms2,idx2)
     rules3 = ProcessRules(rules1, idx1,syms1[0][0],
                           start) + \
              ProcessRules(rules2, idx2,syms2[0][0],
                         start)
     sent3 = sent1
     syms3 = [start]+syms1+syms2
     grammar3 = [rules3,sent3,syms3]
     return grammar3

def Interpreter(grammar, tokenizer,
          detoken = lambda toks: ' '.join(toks)):
     grammar0 = grammar
     print(f"grammar: {grammar}")
     done = False
     print("Enter 'Q:' to quit")
     while not done:
          line = eval(input("L> "))
          line = line.strip(" ")
          if len(line) == 0:
               continue
          if line == 'Q:':
               done = True
               break
          try:
               grammar0[1] = tokenizer(line)
               flag,s = Parse(grammar0,detoken)
               if flag:
                    t = "accept"
               else:
                    t = f"syntax error: {s}"
               print(t)
          except:
               continue
     return

# This is 'a*' in regular expression.
def Star_char(a):
     assert(len(a) == 1)
     sent = list(a)
     grammar = [
          [ # R, production rules
          ("T",list("AA")),
          ("T",list(a)),
          ("T",['']),
          ("A",list("AA")), # start
          ("A",list(a)),
          ("A",['']),
          ],
          sent, # I, characters
          ["T","A"] # N, nonterminal symbols
          ]
     return grammar

# This is Sigma* in regular expression.
def KleeneStar(Sigma):
     for a in Sigma:
          assert(len(a) == 1)
     sent = list(Sigma[0])
     grammar = [
          [ # R, production rules
          ("T",list("AA")),
          ("T",['']),
          ("A",list("AA")), # start
          ("A",['']),
          ],
          sent, # I, characters
          ["T","A"] # N, nonterminal symbols
          ]
     for a in Sigma:
          rule_a = ("A", list(a))
          grammar[0].append(rule_a)
          rule_b = ("T", list(a))
          grammar[0].append(rule_b)
     return grammar

# StringGrammar inputs list elements as accepted
# strings in the language where S is a list of
# characters in string s.
# Eg, grammar = StringGrammar(s) where s = "ab".
# This creates a language L = {'a','b'} by
# specifying grammar to generate language L.
def StringGrammar(s):
     S = list(s)
     sent = S[0] # first element of list
     grammar = []
     rules = []
     for x in S:
          rule = ("T",x)
          rules.append(rule)
     grammar.append(rules)
     grammar.append(sent)
     syms = ["T"]
     grammar.append(syms)
     return grammar

def GrammarConcat(grammar1,grammar2,start="T"):
     idx1 = 1
     idx2 = 2
     rules1,sent1,syms1 = grammar1
     rules2,sent2,syms2 = grammar2
     syms1 = ProcessSymbols(syms1,idx1)     
     syms2 = ProcessSymbols(syms2,idx2)
     rules3 = ProcessRules(rules1, idx1,syms1[0][0],
                           "T1") + \
              ProcessRules(rules2, idx2,syms2[0][0],
                         "T2")
     sent3 = sent1
     syms3 = [start]+["T1","T2"]+syms1[1:]+syms2[1:]
     rule_start = (start,
                   ["T1", "T2"])
     rules3 = [rule_start] + rules3
     grammar3 = [rules3,sent3,syms3]
     return grammar3     

def RegularExpression(s):
     print("Error: unimplemented")
     return

class Language:
     def __init__(self,s='',grammar=[[],'',[]]):
          self.s = s
          self.grammar = deepcopy(grammar)
     def __str__(self):
          s = self.s
          return s
     def __repr__(self):
          return str(self)
     def StringGrammar(self, s):
          s = '{'+','.join(list(s))+'}'
          grammar = StringGrammar(s)
          return Language(s, grammar)
     def KleeneStar(self, Sigma):
          s = '{'+','.join(Sigma)+'}+'
          grammar = KleeneStar(Sigma)
          return Language(s, grammar)
     def __or__(self, y):
          s = '('+str(self) + '|' + str(y)+')'
          grammar = GrammarUnion(self.grammar,
                         y.grammar)
          return Language(s,grammar)
     def __add__(self, y):
          s = '('+str(self) + '' + str(y) + ')'
          grammar = GrammarConcat(self.grammar,
                         y.grammar)
          return Language(s,grammar)
     def parse(self, line,
          tokenizer = lambda s: list(s),
          detoken = lambda toks: ''.join(toks)):
          self.grammar[1] = tokenizer(line)
          flag,s = Parse(self.grammar,detoken)
          if flag:
               t = "accept"
          else:
               t = f"syntax error: {s}"
          return t
     def interpreter(self,
          tokenizer = lambda s: list(s),
          detoken = lambda toks: ''.join(toks),
          show = False):
          grammar0 = self.grammar
          if show:
               print(grammar0)
          else:
               print(self)
          done = False
          print("Enter 'Q:' to quit")
          while not done:
               line = eval(input("L> "))
               line = line.strip(" ")
               if len(line) == 0:
                    continue
               if line == 'Q:':
                    done = True
                    break
               t = self.parse(line,
                    tokenizer,detoken)
               print(t)
          return

