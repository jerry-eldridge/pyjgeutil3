import simple_vowel_model as svm
import os
import nltk
import re

x_cmudict = nltk.corpus.cmudict.dict()

vowels = "ae eh ey iy ow ay ih aa uh ao aw oy ah uw".split(' ')
def F(s):
    pat = "([A-Z]+)[0-9]*"
    val = re.match(pat,s).group(1)
    val = val.lower()
    return val

def translate(word):
    L = []
    if word in x_cmudict:
        L = list(map(F,x_cmudict[word][0]))
    L = [L[i] for i in range(len(L)) if L[i] in vowels]
    return L

def translate_s(sent):
    L = sent.split(" ")
    M = []
    for x in L:
        M = M + translate(x)
    s = '^ '+' '.join(M)+' $'
    return s

#[1] @book{Parker86,
#author = "Parker, Frank",
#title = "Linguistics for Non-Linguists",
#publisher = "College-Hill",
#year = "1986"
#}

# JGE speaks the parker words for phonology
p = {}
p["ae"] = "D6 A5 C5" # sad
p["eh"] = "D#5 A6 F#6" # said
p["ey"] = "A6 G#6 C#5" # say
p["iy"] = "A5 B6 E6" # seat
p["ow"] = "E5 A6 A#6" # sewed
p["ay"] = "G#4 E5 A#5" # sight
p["ih"] = "A6" # sit
p["aa"] = "G5 F#5 E5" # sod
p["uh"] = "C5 C#5 A#6" # soot
p["ao"] = "C#6 D#4 G#6" # sought
p["aw"] = "C5 F#6 F#5" # south
p["oy"] = "G#6 A6 F#6" # soy
p["ah"] = "D#5 E4 A6" # suds
p["uw"] = "G#5 F6 G#6" # suit
svm.p = p

##m11 = """
##^ ae ae ow ow ao ao uw eh iy eh iy ow uw $
##"""
##m11 = """
##^ aa uw ow ih uw ae ah ey $
##"""
m11 = ["this super double cheese burger",
       "this is what you want",
       "this is what you tell me about"]
r11 = """
130 16 16 16 16 8 8 8 8 4 4 8 8 4 2
"""
pattern_11 = "ABACA"
scale = 1
tempo_11_A = 55
tempo_11_B = 100
tempo_11_C = 70
N = 20
stem1 = ' '.join("\n".join(list(map(translate_s, [m11[0]]))).split(' '))
stem2 = ' '.join("\n".join(list(map(translate_s, [m11[1]]))).split(' '))
stem3 = ' '.join("\n".join(list(map(translate_s, [m11[2]]))).split(' '))
m11 = "\n".join(list(map(translate_s, m11)))

S_11_A = [(stem1,
           "130 16 16 16",
           m11,r11,tempo_11_A)]
S_11_B = [(stem2,
           "130 16 16 16",
           m11,r11,tempo_11_B)]
S_11_C = [(stem3,
           "130 16 16 16",
           m11,r11,tempo_11_C)]
S_11 = S_11_A + S_11_B + S_11_C

flag4 = True
if flag4:
    fn_save_11 = "svm_model1-004.mid" 
    svm.demo9(
          fn_save_11,
          pattern = pattern_11,
          S = S_11,
          length = 30,
          I = 5,
          )
    os.system(fn_save_11)
