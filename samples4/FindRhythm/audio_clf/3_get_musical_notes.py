import scipy.io as si
import parselmouth as pm
from collections import namedtuple

from math import log

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

Ftup = namedtuple("Ftup",["F1","V1","F2","V2",
                          "F3","V3"])

##C:\Users\jerry>cd c:\_Python312-64-tf
##c:\_Python312-64-tf>.\python -m pip install praat-parselmouth
##c:\_Python312-64-tf>.\python -m pip install seaborn

root = r"./audio/"
fn = root + "hae.wav"

#sr,x = si.wavfile.read(fn)
snd = pm.Sound(fn)
f = snd.to_formant_burg()
dur = snd.duration
N = 10
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
    print(f"{i*dt},\"{s_notes}\",\"{rec}\"")
