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
fn_save = "model6-001.mid" 
smm.demo5(m,r,
      fn_save,
      pattern = "ABABACAABA",
      tempo= 200,
        stem1 = "13 0 2", nstem1 = 3,
        stem2 = "13 4", nstem2 = 2,
        length = 10,
        I = 3,
        )
os.system(fn_save)
