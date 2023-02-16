import simple_language_model as slm

s = """
Bob likes apple pie. Apple cheddar sour is sometimes
fun to eat. John likes to eat cheese. Sometimes
people like to eat oranges. Oranges are fun. They
are spherical shaped like a ball. Fun cheese is
sometimes something to throw.
"""

N0 = 2
M = slm.SimpleLanguageModel(N=N0)
M.train(s)
I = 5
stem = "Oranges are" # must be length N0 words
for i in range(I):
    si = M.predict(stem,nwords=5)
    print(f"{i}: si = '{si}'")
