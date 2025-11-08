import niels_lexer4 as niels
import erwin_interpreter4 as erwin

def tokenize(program):
    raw_tokens0 = program.strip().replace('\n',' ').\
                 split(" ")
    raw_tokens = []
    for x in raw_tokens0:
        if len(x) == 0:
            continue
        else:
            raw_tokens.append(x)
    return raw_tokens

fn_emmy = "emmy_automata4.txt"    

program = """
start ;
while x < 10
{
   x := x + 1 ;
   if x < 6 {
       print z ;
   } else {
       print w ;
   }
   print x ;
}
print y ;
finish ;
"""
raw_tokens = tokenize(program)
print(raw_tokens)
variables = {"x":0.0,"y":"End of Program",
             "z":"A","w":"B"}
tokens,values = niels.lexer(raw_tokens)
print(f"tokens = {tokens}")
transitions = erwin.load_automaton(fn_emmy)

if erwin.run_automaton(tokens, transitions):
    variables = erwin.interpret(tokens,values,
                    variables)
    print("Final variables:", variables)

