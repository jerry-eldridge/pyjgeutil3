import simple_vowel_model as svm
import os

#[1] @book{Parker86,
#author = "Parker, Frank",
#title = "Linguistics for Non-Linguists",
#publisher = "College-Hill",
#year = "1986"
#}

# JGE speaks the parker words for phonology
p = {}
p["ae"] = "D6 A5 C5" # sad
p["eh"] = "D#4 A5 F#5" # said
p["ey"] = "A6 G#6 C#5" # say
p["iy"] = "A2 B4 E4" # seat
p["ow"] = "E5 A6 A#6" # sewed
p["ay"] = "G#3 E5 A#5" # sight
p["ih"] = "A6" # sit
p["aa"] = "G5 F#5 E5" # sod
p["uh"] = "C5 C#5 A#6" # soot
p["ao"] = "C#4 D#5 G#4" # sought
p["aw"] = "C5 F#6 F#5" # south
p["oy"] = "G#6 A6 F#6" # soy
p["ah"] = "D#3 E2 A4" # suds
p["uw"] = "G#2 F4 G#4" # suit

m11 = """
^ ae ae ow ow ao ao uw eh iy eh iy ow uw $"
"""
r11 = """
130 4 4 4 4 140
130 8 8 8 8 8 8 8 8 140
130 8 4 8 4 8 4 140
"""
pattern_11 = "ABACA"
scale = 2
tempo_11_A = 100*scale
tempo_11_B = 120*scale
tempo_11_C = 105*scale
S_11_A = [("^ ow ow ao","130 5.0 5.0 5.0",
           m11,r11,tempo_11_A)]
S_11_B = [("^ ao uw","7.5 5.0 7.5 5.0",
           m11,r11,tempo_11_B)]
S_11_C = [("^ eh iy eh iy","5.0 5.0 5.0 5.0",
           m11,r11,tempo_11_C)]
S_11 = S_11_A + S_11_B + S_11_C

flag4 = True
if flag4:
    fn_save_11 = "svm_model1-002.mid" 
    svm.demo9(
          fn_save_11,
          pattern = pattern_11,
          S = S_11,
          length = 10,
          I = 3,
          )
    os.system(fn_save_11)
