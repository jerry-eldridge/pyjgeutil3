import niels_lexer4 as niels
import erwin_interpreter4 as erwin

def tokenize0(program):
    raw_tokens0 = program.strip().replace('\n',' ').\
                 split(" ")
    raw_tokens = []
    for x in raw_tokens0:
        if len(x) == 0:
            continue
        else:
            raw_tokens.append(x)
    return raw_tokens

tokenize = tokenize0

fn_emmy = "emmy_automata4.txt"    

program = """
start ;
print " Program is starting. " ;
while state < 10
{
   state := state + 1 ;
   if state >= 6 {
       print " -> Eat! " ;
   } else {
       print " -> Play! " ;
   }
   print state ;
}
print " Program is halting. " ;
finish ;
"""
raw_tokens = tokenize(program)
print(raw_tokens)
variables = {"state":0.0,"x":0.0}
tokens,values = niels.lexer(raw_tokens)
print(f"tokens = {tokens}")
transitions = erwin.load_automaton(fn_emmy)

if erwin.run_automaton(tokens, transitions):
    variables = erwin.interpret(tokens,values,
                    variables)
    print("Final variables:", variables)

