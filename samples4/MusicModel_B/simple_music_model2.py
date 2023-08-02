import os
import simple_language_model as slm

from midiutil import MIDIFile

# [1] "Alfred's Basic Adult Theory Piano Book,
# Level One", Willard A. Palmer, Morton Manus,
# Amanda Vick Lethco, Alfred's, 1983
# [2] "Melody in Songwriting: Tools and Techniques
# for Writing Hit Songs", Jack Perricone,
# Berklee Press, 2000

# demo1 works on note numbers for melody m and stem1
#demo1(m) [1]

# demo2 works using intervals for stem1 except
# for the control begin 13 and end 14.
#demo2(m)

# demo3 works using intervals like demo2 except it
# adds a rhythm r.

# demo5 adds section patterns. [2]

def process7(m,r):
    s = m
    s2 = s.replace('\n',' ')
    song = list(map(int,s2.strip().split(' ')))
    ctl = [130,140]
    song2 = []
    memory = [1] # key
    for i in range(len(song)):
        v = song[i]
        if v in ctl:
            song2.append(v)
            continue
        if v in range(1,12+1):
            w = v - memory[0]
            memory[0] = v
            song2.append(w)
    s3 = ' '.join(list(map(str,song2)))

    s = r
    s4 = s.replace('\n',' ')
    return s3,s4

def create_song7(L, fn_save):
    degs = [60,62,64,65,67,69,71,72]
    track = 0
    channel = 0
    time = 0
    duration0 = 4 # beats
    volume = 120 # 0-127    
    m = MIDIFile(1)
    tempo = 55
    m.addTempo(track, time, tempo)
    d = [0]*len(degs)
    for i in range(len(degs)):
        d[i] = degs[i]
    memory = [0]
    memory[0] = 1
    ctl = [130,140]
    for i in range(len(L)):
        tup = L[i]
        #print(i, tup)
        q,v,dur = tup
        if q == "T":
            tempo = v
            m.addTempo(track, time, tempo)
            continue
        if dur in ctl:
            duration = duration0
        else:
            duration = duration0*(1.0/dur)
        if v in ctl:
            pitch = 60
            vol = 0
            duration = 1/8
            m.addNote(track,channel,pitch,
                time, duration, vol)
            time = time + duration
            continue
        pitch = d[(memory[0] + v + len(d))%len(d)]
        memory[0] = v
        vol = volume
        #print((q,track,channel,pitch,
        #    time, duration, vol))
        m.addNote(track,channel,pitch,
            time, duration, vol)
        time = time + duration
    with open(fn_save,"wb") as f:
        m.writeFile(f)
    return

def demo7(fn_save,
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
        stem1,stem2 = process7(stem1,stem2)
        d_music[P[i]] = [("T",tempo,tempo)]
        m2,r2 = process7(m,r)
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
            melody = list(map(int,si1.split(' ')))
            si2 = M2.predict(stem2,nwords=nstem2)
            rhythm = list(map(float,si2.split(' ')))
            pat = [P[i]]*len(melody)
            if rhythm_fixed is None:
                rhythm_fixed = rhythm            
            mus = list(zip(pat,melody,rhythm))
            d_music[P[i]] = d_music[P[i]] + mus
            #print()
    print()
    music = []
    for q in Q:
        music = music + d_music[q]
    create_song7(music,fn_save)
    return

def process8(m,r):
    s = m
    s2 = s.replace('\n',' ')
    song = list(map(int,s2.strip().split(' ')))
    ctl = [130,140]
    song2 = []
    memory = [1] # key
    for i in range(len(song)):
        v = song[i]
        if v in ctl:
            song2.append(v)
            continue
        if v in range(1,12+1):
            w = v - memory[0]
            memory[0] = v
            song2.append(w)
    s3 = ' '.join(list(map(str,song2)))

    s = r
    s4 = s.replace('\n',' ')
    return s3,s4

def create_song8(L, fn_save):
    degs = [60,62,64,65,67,69,71,72]
    track = 0
    channel = 0
    time = 0
    duration0 = 4 # beats
    volume = 120 # 0-127    
    m = MIDIFile(1)
    tempo = 55
    m.addTempo(track, time, tempo)
    d = [0]*len(degs)
    for i in range(len(degs)):
        d[i] = degs[i]
    memory = [0]
    memory[0] = 1
    ctl = [130,140]
    for i in range(len(L)):
        tup = L[i]
        #print(i, tup)
        q,v,dur = tup
        if q == "T":
            tempo = v
            m.addTempo(track, time, tempo)
            continue
        if dur in ctl:
            duration = duration0
        else:
            duration = duration0*(1.0/dur)
        if v in ctl:
            pitch = 60
            vol = 0
            duration = 1/8
            m.addNote(track,channel,pitch,
                time, duration, vol)
            time = time + duration
            continue
        pitch = d[(memory[0] + v + len(d))%len(d)]
        memory[0] = v
        vol = volume
        #print((q,track,channel,pitch,
        #    time, duration, vol))
        m.addNote(track,channel,pitch,
            time, duration, vol)
        time = time + duration
    with open(fn_save,"wb") as f:
        m.writeFile(f)
    return

def demo8_f(fn_save,
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
        stem1,stem2 = process8(stem1,stem2)
        d_music[P[i]] = [("T",tempo,tempo)]
        m2,r2 = process8(m,r)
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
            melody = list(map(int,si1.split(' ')))
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
    create_song8(music,fn_save)
    return
