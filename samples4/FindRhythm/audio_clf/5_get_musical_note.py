import scipy.io as si
import parselmouth as pm
from collections import namedtuple

from math import log

import os
import fnmatch
import os.path

def piano_freq(note):
    val = 440*2**((note-49)/12.)
    return val
def piano_note(freq):
    n = int(12 * log(freq/440.0)/log(2) + 49)
    return n
def piano_note_name(n):
    names = ["A","A#","B","C","C#","D",
             "D#","E","F","F#","G","G#"]
    idx = (12+n-1)%12
    octave = int((n-1)/12 + 1)
    name = names[idx]+str(octave)
    return name

def ListFiles(folder,pattern):
    L = []
    for root, dire, files in os.walk(folder):
        for fn in fnmatch.filter(files, pattern):
            try:
                root = root.replace('\\','/')
                fn = fn.replace('\\','/')
                filename = root + '/' + fn
                mtime = int(os.path.getmtime(filename))
                ctime = int(os.path.getctime(filename))
                L.append((ctime,mtime,root,fn))
            except:
                continue
    return L

def DisplayVowels(L,N=2):
    #sr,x = si.wavfile.read(fn)
    for tup in L:
        secs1,secs2,root_t,fn_t = tup
        fn = root_t + fn_t
        print(f"fn = \"{fn}\"")
        snd = pm.Sound(fn)
        f = snd.to_formant_burg()
        dur = snd.duration
        dt = dur/N
        for i in range(1,N):
            F1 = f.get_bandwidth_at_time(1,i*dt)
            V1 = f.get_value_at_time(1,i*dt)
            F2 = f.get_bandwidth_at_time(2,i*dt)
            V2 = f.get_value_at_time(2,i*dt)
            F3 = f.get_bandwidth_at_time(3,i*dt)
            V3 = f.get_value_at_time(3,i*dt)
            F1,V1,F2,V2,F3,V3 = list(map(round,\
                [F1,V1,F2,V2,F3,V3]))
            nt1 =piano_note_name(piano_note(F1))
            nt2 =piano_note_name(piano_note(F2))
            nt3 =piano_note_name(piano_note(F3))
            notes = [nt1,nt2,nt3]
            s_notes = ' '.join(notes)
            rec = Ftup(*[F1,V1,F2,V2,F3,V3])
            print(f"  {i*dt},\"{s_notes}\",\"{rec}\"")
        print()
    print("="*20)
    return

Ftup = namedtuple("Ftup",["F1","V1","F2","V2",
                          "F3","V3"])

##C:\Users\jerry>cd c:\_Python312-64-tf
##c:\_Python312-64-tf>.\python -m pip install praat-parselmouth
##c:\_Python312-64-tf>.\python -m pip install seaborn

root = r"C:/Users/jerry/Desktop/AUDIO/"
root2 = root + "JGE_parker_vowels/"
L = ListFiles(root2,"*.wav")

DisplayVowels(L,N=2)

DisplayVowels(L,N=4)
