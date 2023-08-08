import sys
desktop = r"C:/Users/jerry/Desktop/"
root1 = desktop + "FindRhythm/"
sys.path.insert(0,root1)
import cog2_codec as cog2
import record_audio_data as rad
import play_audio_data as pad
import find_rhythm as fir
import DCT
import FFT

import scipy.io as si
import numpy as np

import heapq # heap queue / priority queue

# [1] https://docs.python.org/3/library/heapq.html
# [2] https://scikit-learn.org/stable/modules/neural_networks_supervised.html

def create_segments(sampling_rate,data,
            seq, mmax, h_num,
                    create=True):
    chunk = 1024
    f_c = 2000
    zlib_level = 1
    I = [int(x/dt) for x in seq]
    D = []
    for i in range(len(I)-1):
        a = I[i]
        b = I[i+1]
        data_i = data[a:b,:]
        fn_save = f"./audio/audio-1234-{i:03d}.wav"
        if create:
            si.wavfile.write(fn_save, sampling_rate,
                data_i.astype(np.int16))

        sh = data_i.shape
        sz = sh[0]
        m = int(sz/chunk)
        fv = []
        # compute frequency domain signal Y of sample j of x
        eps = 100
        n0 = FFT.Get_idx(chunk,sampling_rate)(2*f_c,eps)
        for j in range(m):
            x = data_i[:,0].flatten()
            # audio signal x, encode sample j of size chunk
            F = list(map(FFT.fft_freq(chunk,sampling_rate),
                         range(chunk)))
            y = FFT.sample(x,j,chunk)

            N = chunk

            Y = list(y)
            if len(Y) < chunk:
                Y2 = list(Y)
                Y3 = [0]*(chunk-n0)
                Y = np.array(Y2+Y3,dtype=np.int16)
            Y2 = DCT.DCT(Y,n=n0)
            # frequency domain signal for chunk
            z = Y2[:n0]
            h = []
            for k in range(len(z)):
                heapq.heappush(h, (z[k],k))
            S = []
            for k in range(h_num):
                val = heapq.heappop(h)
                S.append(val[1]) # val_k

            z2 = []
            maxz = np.max(np.abs(z))
            for k in range(len(z)):
                if k in S:
                    val = (1+z[k]/maxz)/2.0 # in [0,1]
                    z2.append(val)
                else:
                    z2.append(0)

            fv.append(z2)
        #print(len(fv))
        for j in range(m,mmax):
            fv.append([0]*n0)
        #print(len(fv))
        D.append(fv)
    X = np.array(D)

    verbose = False
    if verbose:
        for i in range(X.shape[0]):
            print('-'*30)
            for j in range(X.shape[1]):
                v = ''.join(map(str,
                    list(X[i,j,:].flatten())))
                print(v)
    return X

root2 = desktop + "AUDIO/"
fn_wav = root2 + "ah-ah-uw-ow-001.wav"
fn_wav = root2 + "happy_birthday_0001.wav"
fn_wav = root2 + "JGE_parker_vowels-01.wav"
root3 = "./" 
sampling_rate,data = si.wavfile.read(fn_wav)
dt = 1/sampling_rate
# this works but it was difficult finding chunk=2048
# and avg_threshold=500
seq = fir.segment_audio(fn_wav,chunk=2048,
                avg_threshold=500)

X = create_segments(sampling_rate,
        data,seq,mmax=120,
        h_num = 5,
        create=False)
print(f"seq = {seq}")
flag0 = True
if flag0:
    r = fir.find_rhythm(fn_wav, beat=4, quanta=8,
                chunk=2048,
                avg_threshold=500,
                flag_reciprocal=True)
    print(f"r = {r}")
flag1 = True
if flag1:
    from sklearn.neural_network import MLPClassifier
    sh = X.shape
    y0 = ["silence","ah","ah","uw","ow"]
    y0 = ["silence","hae","pi","hae","pi","bIr",
          "bIr","bIr","de"]
    I = [0,1,2,3,4,5,8]
    Y = np.zeros((len(I),sh[1]*sh[2]))
    for i in range(len(I)):
        idx = I[i]
        Y[i,:] = X[idx,:,:].flatten()
    y = ["silence","hae","pi","hae","pi","bIr","de"]
    clf = MLPClassifier(solver='lbfgs',
            alpha=1e-5,
            hidden_layer_sizes = (100,100),
            random_state=1)
    clf.fit(Y,y)
    def predict(x):
        y = clf.predict([list(x.flatten())])
        c = y[0]
        return c
    for i in range(X.shape[0]):
        print(i, predict(X[i]))
    
