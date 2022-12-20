import pyaudio
import wave

# [1] https://people.csail.mit.edu/hubert/pyaudio/docs/
def PlayAudio(fn_wav2):
    wf = wave.open(fn_wav2,'rb')

    chunk = 1024
    
    p = pyaudio.PyAudio()

    nchannels = wf.getnchannels()
    fmt = p.get_format_from_width(wf.getsampwidth())
    sampling_rate = wf.getframerate()
    stream = p.open(format=fmt,
                    channels=nchannels,
                    rate=sampling_rate,
                    output=True)

    data = wf.readframes(chunk)
    while len(data):
        stream.write(data)
        data = wf.readframes(chunk)
        
    stream.stop_stream()
    stream.close()

    p.terminate()
    return
