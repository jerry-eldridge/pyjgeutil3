import simple_music_model as smm
import os

m = """
13 1 3 4 5 6 5 4 3 3 1 1 3 3 1 1 5 6 5 4 3 2 1 1 14
13 1 1 1 1 3 3 3 3 5 5 5 5 14
13 1 2 1 2 1 2 1 2 1 2 14
"""
r = """
13 4 4 4 4 8 8 8 8 8 8 8 8 16 16 16 16 14
13 4 2.67 8 2.67 8  8 2.67 8 2.67 8 16 14
"""
fn_save = "model7-001.mid" 
smm.demo6(m,r,
      fn_save,
      pattern = "ABABACA",
      tempo= 200,
      # stem1 is the melody stem and stem2 is
      # the rhythm stem.
      #(stem1,stem2) for each unique
      #letter in the pattern in order, A, B, C
      # where nstem1 is number of tokens in stem1
      # and nstem2 is number of tokens in stem2
      # where tokens are delimited by a single " "
      # space symbol.
      S = [("13 1 3 4","13 4 4"), # A
           ("13 1 1 1","2.67 8 2.67 8"), # B
           ("13 1 2","4 4 8"), # C
           ],
      length = 10,
      I = 3,
      )
#os.system(fn_save)
