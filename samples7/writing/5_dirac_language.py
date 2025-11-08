import niels_lexer4 as niels
import erwin_interpreter4 as erwin
import squirrel_writer as kleisi

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

font_dir = "./font3/"
fn_save_blank = "./20251108-blank_page.png"
fn_save_log = "./20251108-dirac_log.txt"
fn_save_page = "./20251108-printout-001.png"
# Image size set in jgetypesetter.py show() .
# other parameters in squirrel_writer.py .
kleisi.squirrel_writer(program,
    font_dir = font_dir,
    page_name = "page_001",
    color=[255,100,100],
    thickness=3,
    fn_save_blank = fn_save_blank,
    fn_save_log = fn_save_log,
    fn_save_page = fn_save_page)

print(f"Dirac program:")
print('='*30)
print(f"{program}")
print('='*30)
raw_tokens = tokenize(program)
variables = {"state":0.0,"x":0.0}
tokens,values = niels.lexer(raw_tokens)
tags = [f"'{tup[0]}'/{tup[1]}" \
        for tup in list(zip(raw_tokens,tokens))]
print(f"Dirac program tags:")
print('='*30)
for i in range(len(tags)):
    print(f"{i:04d}  {tags[i]}")
print('='*30)
transitions = erwin.load_automaton(fn_emmy)

if erwin.run_automaton(tokens, transitions):
    variables = erwin.interpret(tokens,values,
                    variables)
    print("Final variables:", variables)

