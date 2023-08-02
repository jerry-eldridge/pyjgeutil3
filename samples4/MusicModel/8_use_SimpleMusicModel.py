import simple_music_model as smm
import os

m1 = """
13 1 3 3 5 5 6 7 6 5 5 1 3 3 5 6 5 6 5 1 1 1 14
"""
r1 = """
13 1 2 4 4 1 2 4 4 1 3 4 14
13 4 4 4 8 8 4 4 8 8 4 4 2 14
"""
stem1_1 = "13 0 4 0"
stem2_1 = "13 4 4 4"
tempo_1 = 80
S_1 = [(stem1_1,stem2_1, m1,r1, tempo_1)]

m2 = """
13 1 3 3 5 5 6 7 6 5 5 1 3 3 5 6 5 6 5 1 1 1 14
13 1 1 5 5 7 7 5 5 1 1 14
"""
r2 = """
13 1 2 4 4 1 2 4 4 1 3 4 14
13 4 4 4 8 8 4 4 8 8 4 4 2 14
"""
stem1_2 = "13 0 4 0"
stem2_2 = "13 4 4 4"
tempo_2 = 140
S_2 = [(stem1_2,stem2_2, m2,r2,tempo_2)]

m3 = """
13 1 2 3 4 5 5 5 5 6 5 4 3 3 3 14
13 1 2 3 4 3 3 3 14
13 1 3 5 5 4 3 4 5 6 6 6 14
"""
r3 = """
13 4 4 4 8 8 4 4 8 8 4 4 2 14
13 4 4 4 4 14
"""
stem1_3 = "13 0 2 2 3 5"
stem2_3 = "13 4 8 8 2"
tempo_3 = 120
S_3 = [(stem1_3,stem2_3, m3,r3,tempo_3)]

m4 = """
13 1 3 3 4 4 5 1 14
13 1 3 3 5 6 7 8 8 8 9 7 6 5 5 5 14
"""
r4 = """
13 4 8 8 2.67 8 2.67 8 14
13 2.67 8 2.67 8 14
"""
stem1_4 = "13 0 2"
stem2_4 = "13 4 8 8"
tempo_4 = 120
S_4 = [(stem1_4,stem2_4, m4,r4,tempo_4)]

m5 = """
13 1 3 4 5 6 5 4 3 3 1 1 3 3 1 1 5 6 5 4 3 2 1 1 14
13 1 1 1 1 3 3 3 3 5 5 5 5 14
13 1 2 1 2 1 2 1 2 1 2 14
"""
r5 = """
13 4 4 4 4 8 8 8 8 8 8 8 8 16 16 16 16 14
13 4 2.67 8 2.67 8  8 2.67 8 2.67 8 16 14
"""
stem1_5 = "13 0 2"
stem2_5 = "13 4"
tempo_5 = 200
S_5 = [(stem1_5,stem2_5, m5,r5,tempo_5)]

m6 = """
13 1 3 4 5 6 5 4 3 3 1 1 3 3 1 1 5 6 5 4 3 2 1 1 14
13 1 1 1 1 3 3 3 3 5 5 5 5 14
13 1 2 1 2 1 2 1 2 1 2 14
"""
r6 = """
13 4 4 4 4 8 8 8 8 8 8 8 8 16 16 16 16 14
13 4 2.67 8 2.67 8  8 2.67 8 2.67 8 16 14
"""
stem1_6 = "13 0 2"
stem2_6 = "13 4"
tempo_6 = 120
S_6 = [(stem1_6,stem2_6, m6,r6,tempo_6)]

m7 = """
13 1 3 4 5 6 5 4 3 3 1 1 3 3 1 1 5 6 5 4 3 2 1 1 14
13 1 1 1 1 3 3 3 3 5 5 5 5 14
13 1 2 1 2 1 2 1 2 1 2 14
"""
r7 = """
13 4 4 4 4 8 8 8 8 8 8 8 8 16 16 16 16 14
13 4 2.67 8 2.67 8  8 2.67 8 2.67 8 16 14
"""
pattern_7 = "ABABACAA"
tempo_7_A = 120
tempo_7_B = 120
tempo_7_C = 120
S_7_A = [("13 1 3 4","13 4 4",m7,r7,tempo_7_A)]
S_7_B = [("13 1 1 1","2.67 8 2.67 8",m7,r7,
          tempo_7_B)]
S_7_C = [("13 1 2","4 4 8",m7,r7,tempo_7_C)]
# S_7 = A + B + C # alphabetic order
S_7 = S_7_A + S_7_B + S_7_C

pattern_8 = "ABABACAA"
# S_8 = A + B + C # alphabetic order
S_8_A = S_2
S_8_B = S_3
S_8_C = S_5
S_8 = S_8_A + S_8_B + S_8_C

flag1 = False
flag2 = False
if flag1:
    fn_save_8nf = "model8_nf-001.mid" 
    smm.demo7(
          fn_save_8nf,
          pattern = pattern_8,
          # stem1 is the melody stem and stem2 is
          # the rhythm stem.
          #(stem1,stem2) for each unique
          #letter in the pattern in order, A, B, C
          # where nstem1 is number of tokens in stem1
          # and nstem2 is number of tokens in stem2
          # where tokens are delimited by a single " "
          # space symbol.
          S = S_8,
          length = 10,
          I = 3,
          )
    #os.system(fn_save_8nf)
if flag2:
    fn_save_8f = "model8_f-001.mid" 
    smm.demo8_f(
          fn_save_8f,
          pattern = pattern_8,
          # stem1 is the melody stem and stem2 is
          # the rhythm stem.
          #(stem1,stem2) for each unique
          #letter in the pattern in order, A, B, C
          # where nstem1 is number of tokens in stem1
          # and nstem2 is number of tokens in stem2
          # where tokens are delimited by a single " "
          # space symbol.
          S = S_8,
          length = 10,
          I = 3,
          )
    #os.system(fn_save_8f)

m9 = """
13 1 1 2 2 3 3 4 3 3 4 4 5 5 5 14
13 1 1 1 1 3 3 3 3 5 5 5 5 14
13 1 2 1 2 1 2 1 2 1 2 14
"""
r9 = """
13 16 16 16 16 8 8 8 8 8 8 8 8 16 16 16 16 14
"""
pattern_9 = "ABACADA"
slow=50
tempo_9_A = 120-slow
tempo_9_B = 100-slow
tempo_9_C = 180-slow
tempo_9_D = 130-slow
S_9_A = [("13 1 1 3","13 16 16 8 8 4",m9,r9,tempo_9_A)]
S_9_B = [("13 1 3 3 1","4 8 4 8",m2,r9,
          tempo_9_B)]
S_9_C = [("13 1 2 1","4 4 8",m4,r9,tempo_9_C)]
S_9_D = [("13 1 1 2 2","8 8 8 8",m9,r9,tempo_9_D)]
# S_9 = A + B + C # alphabetic order
S_9 = S_9_A + S_9_B + S_9_C + S_9_D

flag3 = True
if flag3:
    fn_save_9 = "model9_f-001.mid" 
    smm.demo8_f(
          fn_save_9,
          pattern = pattern_9,
          # stem1 is the melody stem and stem2 is
          # the rhythm stem.
          #(stem1,stem2) for each unique
          #letter in the pattern in order, A, B, C
          # where nstem1 is number of tokens in stem1
          # and nstem2 is number of tokens in stem2
          # where tokens are delimited by a single " "
          # space symbol.
          S = S_9,
          length = 10,
          I = 3,
          )
    #os.system(fn_save_9)
