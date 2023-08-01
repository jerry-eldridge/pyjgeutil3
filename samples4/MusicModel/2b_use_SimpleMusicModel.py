import os
import simple_language_model as slm

from midiutil import MIDIFile

# [1] Alfred's Basic Adult Theory Piano Book,
# Level One, Willard A. Palmer, Morton Manus,
# Amanda Vick Lethco, 1983

def process1(s):
    s2 = s.replace('\n',' ')
    s3 = s2.strip()
    return s3

def create_song1(L):
    degs = [60,62,64,65,67,69,71,72]
    track = 0
    channel = 0
    time = 0
    duration = 1 # beats
    tempo = 80
    volume = 120 # 0-127    
    m = MIDIFile(1)
    m.addTempo(track, time, tempo)
    d = {}
    for i in range(len(degs)):
        d[i+1] = degs[i]
    for i in range(len(L)):
        v = L[i]
        if v == 13 or v == 14:
            pitch = d[1]
            vol = 0
            m.addNote(track,channel,pitch,
                time+i, duration, vol)
        if v in range(1,12+1):
            pitch = d[v]
            vol = volume
            m.addNote(track,channel,pitch,
                time+i, duration, vol)
    with open("tmp-1234-1.mid","wb") as f:
        m.writeFile(f)
    #os.system("tmp-1234.mid")
    return

def demo1(s):
    N0 = 3
    M = slm.SimpleLanguageModel(N=N0)
    s2 = process1(s)
    M.train(s2)
    I = 5
    stem = "13 1 1" # must be length N0 words
    music = []
    for i in range(I):
        si = M.predict(stem,nwords=10)
        song = list(map(int,si.split(' ')))
        print(song)
        music = music + song
        print()
    print()
    print(music)
    create_song1(music)
    return

def process2(s):
    s2 = s.replace('\n',' ')
    song = list(map(int,s2.strip().split(' ')))
    ctl = [13,14]
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
    return s3

def create_song2(L):
    degs = [60,62,64,65,67,69,71,72]
    track = 0
    channel = 0
    time = 0
    duration = 0.5 # beats
    tempo = 140
    volume = 120 # 0-127    
    m = MIDIFile(1)
    m.addTempo(track, time, tempo)
    d = [0]*len(degs)
    for i in range(len(degs)):
        d[i] = degs[i]
    memory = [0]
    memory[0] = 1
    ctl = [13,14]
    for i in range(len(L)):
        v = L[i]
        if v in ctl:
            pitch = 60
            vol = 0
            m.addNote(track,channel,pitch,
                time+i, duration, vol)
            continue
        pitch = d[(memory[0] + v + len(d))%len(d)]
        memory[0] = v
        vol = volume
        #print((track,channel,pitch,
        #    time+i, duration, vol))
        m.addNote(track,channel,pitch,
            time+i, duration, vol)
    with open("tmp-1234-2.mid","wb") as f:
        m.writeFile(f)
    #os.system("tmp-1234-2.mid")
    return

def demo2(s):
    N0 = 3
    M = slm.SimpleLanguageModel(N=N0)
    s2 = process2(s)
    M.train(s2)
    I = 5
    stem = "13 0 2" # must be length N0 words
    music = []
    for i in range(I):
        si = M.predict(stem,nwords=10)
        song = list(map(int,si.split(' ')))
        print(song)
        music = music + song
        print()
    print()
    print(music)
    create_song2(music)
    return

def process3(m,r):
    s = m
    s2 = s.replace('\n',' ')
    song = list(map(int,s2.strip().split(' ')))
    ctl = [13,14]
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

def create_song3(L):
    degs = [60,62,64,65,67,69,71,72]
    track = 0
    channel = 0
    time = 0
    duration0 = 4 # beats
    tempo = 140
    volume = 120 # 0-127    
    m = MIDIFile(1)
    m.addTempo(track, time, tempo)
    d = [0]*len(degs)
    for i in range(len(degs)):
        d[i] = degs[i]
    memory = [0]
    memory[0] = 1
    ctl = [13,14]
    for i in range(len(L)):
        tup = L[i]
        #print(i, tup)
        v,dur = tup
        if dur in ctl:
            duration = duration0
        else:
            duration = duration0*(1.0/dur)
        if v in ctl:
            pitch = 60
            vol = 0
            m.addNote(track,channel,pitch,
                time, duration, vol)
            time = time + duration
            continue
        pitch = d[(memory[0] + v + len(d))%len(d)]
        memory[0] = v
        vol = volume
        print((track,channel,pitch,
            time, duration, vol))
        m.addNote(track,channel,pitch,
            time, duration, vol)
        time = time + duration
    with open("tmp-1234-3.mid","wb") as f:
        m.writeFile(f)
    os.system("tmp-1234-3.mid")
    return

def demo3(m,r,
        stem1 = "13 0 2", nstem1 = 3,
        stem2 = "2 2 4 4", nstem2 = 4,
        length = 10,
        I = 5,
          ):
    m2,r2 = process3(m,r)
    
    N01 = nstem1
    M1 = slm.SimpleLanguageModel(N=N01)
    M1.train(m2)
    
    N02 = nstem2
    M2 = slm.SimpleLanguageModel(N=N02)
    M2.train(r2)
    
    melody = []
    rhythm = []
    for i in range(I):
        si = M1.predict(stem1,nwords=length)
        song = list(map(int,si.split(' ')))
        melody = melody + song
        si = M2.predict(stem2,nwords=length)
        song = list(map(float,si.split(' ')))
        rhythm = rhythm + song
        mus = list(zip(melody,rhythm))
        #print(mus)
        #print()

    print()
    #print(f"melody = {melody}")
    #print(f"rhythm = {rhythm}")
    music = list(zip(melody,rhythm))
    #print(f"music = {music}")
    create_song3(music)
    return

m = """
13 1 3 3 5 5 6 7 6 5 5 1 3 3 5 6 5 6 5 1 1 1 14
13 1 1 5 5 7 7 5 5 1 1 14
"""
r = """
13 1 2 4 4 1 2 4 4 1 3 4 14
13 4 4 4 8 8 4 4 8 8 4 4 2 14
"""
# demo1 works on note numbers for melody m and stem1
#demo1(m)

# demo2 works using intervals for stem1 except
# for the control begin 13 and end 14.
#demo2(m)

# demo3 works using intervals like demo2 except it
# adds a rhythm r.
demo3(m,r,
        stem1 = "13 0 4 0", nstem1 = 4,
        stem2 = "13 4 4 4", nstem2 = 4,
        length = 30,
        I = 10)
