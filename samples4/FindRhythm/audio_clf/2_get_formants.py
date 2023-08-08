import scipy.io as si
import parselmouth as pm
from collections import namedtuple

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
    rec = Ftup(*[F1,V1,F2,V2,F3,V3])
    print(i*dt,rec)
