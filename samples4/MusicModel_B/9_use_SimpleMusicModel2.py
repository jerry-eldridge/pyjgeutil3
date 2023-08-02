import simple_music_model2 as smm
import os

m10 = """
130 1 1 2 2 3 3 4 3 3 4 4 5 5 5 140
130 1 1 1 1 3 3 3 3 5 5 5 5 7 9 11 12 11 9 7 7 7 7 140
130 1 2 1 2 1 2 1 2 1 2 5 5 7 7 9 11 12 140
"""
r10 = """
130 4 4 8 8 4 4 4 8 8 4 2 2 4 8 8 4 4 140
"""
pattern_10 = "ABACA"
tempo_10_A = 55
tempo_10_B = 75
tempo_10_C = 100
S_10_A = [("130 1 3 5","13 4 8 8 4 4",
           m10,r10,tempo_10_A)]
S_10_B = [("130 1 3 3 1","4 8 4 8 4",
           m10,r10,tempo_10_B)]
S_10_C = [("130 1 3 2 2 1","4 4 4 4",
           m10,r10,tempo_10_C)]
S_10 = S_10_A + S_10_B + S_10_C

flag4 = True
if flag4:
    fn_save_10 = "model10_f-001.mid" 
    smm.demo8_f(
          fn_save_10,
          pattern = pattern_10,
          S = S_10,
          length = 10,
          I = 3,
          )
    os.system(fn_save_10)
