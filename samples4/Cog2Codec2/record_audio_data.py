import cog2_codec as cog2
import record_audio_data as rad

import sounddevice as sd

def listen(sampling_rate=16000):
    secs = input("Input number Seconds to Listen> ")
    secs = float(secs)
    print("Listening for secs=",secs,"seconds")
    q = input("Enter to listen> ")
    rate = sampling_rate
    data2 = sd.rec(int(secs*rate),samplerate=rate,
             channels=2, dtype='int16')
    sd.wait()
    return data2, sampling_rate
