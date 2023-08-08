import os
import re
from midiutil import MIDIFile
import simple_language_model_rlq as slm

notes = ["C","C#","D","D#",
         "E","F","F#","G","G#","A","A#","B"]
def convert(s):
    pat = ".*([A-G]+)([#]*)([-]*[0-9]+).*"
    res = re.match(pat, s)
    if res:
        x = res.group(1)
        y = res.group(2)
        z = res.group(3)
        sym = x + y
        idx = notes.index(sym)
        z = int(z)-1
        offset = 12*z + 4
        note = idx + offset
        midi = 20 + note
        return note,midi
    return None,None

def phoneme2midi(s):
    t = p[s]
    toks = t.split(' ')
    L = []
    for x in toks:
        note,midi = convert(x)
        L.append(midi)
    return L

# speaking parker's Linguistics for Non-linguists
# words for vowels. Recognizing the Formants F1,
# F2, and F3 for each word.
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

def process9(m,r):
    s = m
    s2 = s.replace('\n',' ')
    song = s2.strip().split(' ')
    ctl = ['^','$']
    song2 = []
    memory = [1] # key
    for i in range(len(song)):
        v = song[i]
        if v in ctl:
            song2.append(v)
            continue
        song2.append(v)
    s3 = ' '.join(list(map(str,song2)))

    s = r
    s4 = s.replace('\n',' ')
    return s3,s4

def create_song9(L, fn_save):
    track = 0
    channel = 0
    time = 0
    duration0 = 4 # beats
    volume = 120 # 0-127    
    m = MIDIFile(1)
    tempo = 55
    m.addTempo(track, time, tempo)
    ctl1 = ['^','$']
    ctl2 = [130,140]
    for i in range(len(L)):
        tup = L[i]
        print(tup)
        #print(i, tup)
        q,v,dur = tup
        if q == "T":
            tempo = v
            m.addTempo(track, time, tempo)
            continue
        if dur in ctl2:
            duration = duration0
        else:
            duration = duration0*(1.0/dur)
        if v in ctl1:
            pitch = 60
            vol = 0
            duration = 1/8
            m.addNote(track,channel,pitch,
                time, duration, vol)
            time = time + duration
            continue
        vol = volume
        P = phoneme2midi(v)
        for pitch in P:
            m.addNote(track,channel,pitch,
                time, duration, vol)
        time = time + duration
    with open(fn_save,"wb") as f:
        m.writeFile(f)
    return

def demo9(fn_save,
        pattern="AAAA",
        S = [],
        length = 10,
        I = 3,
          ):
    P = list(set(list(pattern)))
    P.sort()
    Q = list(pattern)
    if len(S) != len(P):
        print(f"|S| = {len(S)}, |P| = {len(P)}"+\
              f" must be equal.")
        print("Error: S must be provided a list of "+\
              "[....(stem1,stem2,m,r).]")
        return
    
    melody = []
    rhythm = []
    d_music = {}
    rhythm_fixed = None
    for i in range(len(P)):
        stem1,stem2,m,r,tempo = S[i]
        stem1,stem2 = process9(stem1,stem2)
        d_music[P[i]] = [("T",tempo,tempo)]
        m2,r2 = process9(m,r)
        nstem1 = len(stem1.split(' '))
        nstem2 = len(stem2.split(' '))
        N01 = nstem1
        M1 = slm.SimpleLanguageModel(N=N01)
        M1.train(m2)
        
        N02 = nstem2
        M2 = slm.SimpleLanguageModel(N=N02)
        M2.train(r2)
        for j in range(I):
            si1 = M1.predict(stem1,nwords=nstem1)
            melody = si1.split(' ')
            si2 = M2.predict(stem2,nwords=nstem2)
            rhythm = list(map(float,si2.split(' ')))
            pat = [P[i]]*len(melody)
            if rhythm_fixed is None:
                rhythm_fixed = rhythm            
            mus = list(zip(pat,melody,rhythm_fixed))
            d_music[P[i]] = d_music[P[i]] + mus
            #print()
    print()
    music = []
    for q in Q:
        music = music + d_music[q]
    create_song9(music,fn_save)
    return

