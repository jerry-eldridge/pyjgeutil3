import simple_music_model2 as smm
import os

m11 = """
130 1 1 2 2 3 3 4 3 3 4 4 5 5 5 140
130 1 1 1 1 3 3 3 3 5 5 5 5 6 5 140
130 1 2 1 2 1 2 1 2 1 2 5 5 140
"""
r11 = """
130 5.0 5.0 5.0 5.0 5.0 5.0 2.143 5.0 2.5 140
130 5.0 1.5 5.0 7.5 5.0 7.5 5.0 5.0 2.5 15.0 15.0 140
130 15.0 7.5 7.5 5.0 5.0 140
"""
pattern_11 = "ABACA"
scale = 2
tempo_11_A = 100*scale
tempo_11_B = 120*scale
tempo_11_C = 105*scale
S_11_A = [("130 1 3 5 5 3","130 5.0 5.0 5.0",
           m11,r11,tempo_11_A)]
S_11_B = [("130 1 3 3 1","7.5 5.0 7.5 5.0",
           m11,r11,tempo_11_B)]
S_11_C = [("130 1 3 2 2 1","5.0 5.0 5.0 5.0",
           m11,r11,tempo_11_C)]
S_11 = S_11_A + S_11_B + S_11_C

flag4 = True
if flag4:
    fn_save_11 = "model11_f-001.mid" 
    smm.demo8_f(
          fn_save_11,
          pattern = pattern_11,
          S = S_11,
          length = 10,
          I = 3,
          )
    os.system(fn_save_11)
