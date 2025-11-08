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

from math import log,ceil

def BuildTreeString(derivation):
     return ""

# https://en.wikipedia.org/wiki/CYK_algorithm
def CYK(grammar):
     TT = True # must be boolean true
     FF = False
     R = grammar[0]
     I = grammar[1]
     #print(f"I = {I}")
     N = grammar[2]
     n = len(I)
     nlog = ceil(log(n)/log(10)+1)
     r = len(N)
     E = ['']
     P = np.zeros((n+1,n+1,r+1))
     B = np.zeros((n+1,n+1,r+1),dtype=list)
     Q = np.zeros((n+1,n+1,r+1),dtype=list)
     for L in range(n+1):
          for s in range(n+1):
               for a in range(r+1):
                    B[L,s,a] = []
                    Q[L,s,a] = ""
     #print("P.shape = ",P.shape)
     for s in range(1,n+1):
         for v in range(len(R)):
             rule = R[v]
             flag = len(rule[1]) == 1 and \
                     (rule[1][0] == I[s-1])
             #print(s,v)
             #print(rule,flag, rule[1][0])
             if not flag:
                 continue
             #print(f"rule = {rule}, {I[s-1]}")
             vv = N.index(R[v][0])+1
             P[1,s,vv] = TT
             a_s = f"{I[s-1]}"
             R_a = f"{R[v][0]}"
             s_rule = [f"R_{v}",' ',f'a_%0{nlog}d'%s,
                       ':',R_a , " -> '" , a_s, "'"]
             #print(s_rule)
             Q[1,s,vv] = s_rule
     #print("here")
     for L in range(2,n+1):
         for s in range(1,n-L+1+1):
             for p in range(1,L-1+1):
                 for v in range(len(R)):
                     rule = R[v]
                     flag1 = len(rule[1]) == 2
                     flag2 = set(rule[1]) <= set(N)
                     flag = (flag1 and flag2)
                     if not flag:
                         continue

                     a = N.index(R[v][0])+1
                     b = N.index(rule[1][0])+1
                     c = N.index(rule[1][1])+1

                     if P[p,s,b] and \
                        P[L-p,s+p,c]:
                         P[L,s,a] = TT
                         R_a = f"{R[v][0]}"
                         R_b = f"{rule[1][0]}"
                         R_c = f"{rule[1][1]}"
                         pre = f"({L},{s},{p},{v})"
                         pre = f"R_{v}"
                         s_rule = [pre , ":" , \
                                  R_a ," -> " , \
                                  R_b , " " , R_c]
                         #print(s_rule)
                         B[L,s,a].append((p,b,c))
                         Q[L,s,a] = s_rule
                         
     if P[n,1,1] == TT:
         M = True
     else:
         M = False
     # Show derivation if M is True:
     derivation = ""
     tags = []
     if M == True:
          txt = ""
          L,s,a = n,1,1
          done = False
          count = 1
          D = [(L,s,a)]
          key = 0
          D2 = []
          while len(D) > 0:
               L,s,a = D[0]
               D = D[1:]
               rule = Q[L,s,a]
               key = key + 1
               txt = txt + f"{''.join(rule)}\n"
               #txt = txt + f"{rule}\n"
               D2.append(rule)
               L2 = B[L,s,a]
               if len(L2) == 0:
                    done = True
               else:
                    tup = L2[0]
                    B[L,s,a] = B[L,s,a][1:]
                    p,b,c = tup
                    D.append((p,s,b))
                    D.append((L-p,s+p,c))
          derivation = txt[:-1]
          tags = []
          for x in D2:
               if len(x) == 8:
                    tag = (x[2],x[6]+f"/{x[4]}")
                    tags.append(tag)
          tags.sort()
          tags = list([tup[1] for tup in tags])
     tags2 = list(zip(list(range(len(tags)+1))[1:],
                           tags))
     return M, P, N, derivation, tags2

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
     flag,P, N, derivation, tags = CYK(grammar)
     s = ''
     if not flag:
         flag2 = False
         s = f"'{detoken(grammar[1])}'"
         return flag2,s,derivation,tags
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
     return True,s,derivation,tags

def ProcessRules(rules, i, start0, start):
     rules2 = []
     LHS,RHS = rules[0]
     if LHS == start0:
          LHS = start
     if len(RHS) == 2:
          A,B = RHS
          #A = (A,i)
          #B = (B,i)
          A = f"{A}.{i}"
          B = f"{B}.{i}"
          RHS = [A,B]
     rule = (LHS,RHS)
     rules2.append(rule)
     for rule in rules[1:]:
          LHS,RHS = rule
          if LHS == start0:
               LHS = start
          else:
               #LHS = (LHS,i)
               LHS = f"{LHS}.{i}"
          if len(RHS) == 2:
               A,B = RHS
               #A = (A,i)
               #B = (B,i)
               A = f"{A}.{i}"
               B = f"{B}.{i}"
               RHS = [A,B]
          rule2 = (LHS,RHS)
          rules2.append(rule2)
     return rules2

def ProcessSymbols(syms, i):
     syms2 = list([f"{t}.{i}" for t in syms])
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
               flag,s,derivation,tags = \
                    Parse(grammar0,detoken)
               if flag:
                    t = "accept"
                    if len(derivation) > 0:
                         print((f"Derivation:\n",
                               derivation))
                         print(("tags: ", tags))
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
     S = list(set(list(s)))
     sent = S[0] # first element of list
     grammar = []
     rules = []
     for x in S:
          rule = ("T",list(x))
          #print(f"StringGrammar: rule = {rule}")
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
     def __init__(self,s='',grammar=[
          [("T",[''])],'',["T"]],
               name=''):
          self.s = s
          self.name0 = 'language'
          if name == '':
               name = self.name0
          self.name = name
          self.grammar = deepcopy(grammar)
     def __str__(self):
          if self.name != self.name0:
               s = self.name
          else:
               s = self.s
          return s
     def __repr__(self):
          return str(self)
     def Word(self, t):
          lst = list(t)
          L1 = Language().StringGrammar(lst[0])
          for ch in lst[1:]:
               L_ch = Language().StringGrammar(ch)
               L1 = L1 + L_ch
          L1.s = "\""+t+"\""
          L1.name = "\""+t+"\""
          return L1
     def StringGrammar(self, s):
          t = '{"'+'","'.join(list(s))+'"}'
          grammar = StringGrammar(s)
          return Language(t, grammar)
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
          if len(line) == 0:
               return 'empty',"",[]
          self.grammar[1] = tokenizer(line)
          flag,s,derivation,tags = \
                    Parse(self.grammar,detoken)
          if flag:
               t = "accept"
          else:
               t = f"syntax error: {s}"
          return t, derivation,tags
     def interpreter(self,
          tokenizer = lambda s: list(s),
          detoken = lambda toks: ''.join(toks),
          show = False):
          grammar0 = self.grammar
          if show:
               print(f"grammar: {self.name} = {grammar0}")
          else:
               print(f"language: {self.name} = ::{self.s}::")
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
               t,derivation,tags = self.parse(line,
                    tokenizer,detoken)
               if len(derivation) > 0:
                    print(f"Derivation:\n{derivation}")
                    print(("tags: ", tags))
               print(t)
          return
     def run(self, line,
               tokenizer = lambda s: list(s),
               detoken = lambda toks: ''.join(toks),
               show = False):
          line = line.strip(" ")
          if len(line) == 0:
               return
          print(f"language: {self.name} = ::{self.s}::")
          print(f"Parsing line = '{line}'")
          t,derivation,tags = self.parse(line,
               tokenizer,detoken)
          if len(derivation) > 0:
               print(f"Derivation:\n{derivation}")
               print(("tags: ", tags))
          print(t)
          print()
          return
