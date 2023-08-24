import nltk
import re
import numpy as np

import matplotlib.pyplot as plt
import scipy.fft as sf
import scipy.io as si

import vowel_synthesis2 as vs
import consonant_synthesis as cs

x_cmudict = nltk.corpus.cmudict.dict()

txt1 = """
"./JGE/spectrum_JGE_B.txt",1,1395.254484882309,"bandpass"
"./JGE/spectrum_JGE_CH.txt",1.0457392145330344,1994.6283512629952,"bandpass"
"./JGE/spectrum_JGE_D.txt",1,1207.7722102012685,"bandpass"
"./JGE/spectrum_JGE_F.txt",1,970.5970724145966,"bandpass"
"./JGE/spectrum_JGE_G.txt",1,1216.8177284664625,"bandpass"
"./JGE/spectrum_JGE_HH.txt",1,897.7904949775287,"bandpass"
"./JGE/spectrum_JGE_JH.txt",1.0882622402906446,1858.6337125583336,"bandpass"
"./JGE/spectrum_JGE_K.txt",1,1369.1662067509903,"bandpass"
"./JGE/spectrum_JGE_L.txt",1,435.17186148815733,"bandpass"
"./JGE/spectrum_JGE_M.txt",1.5903347631184808,205.7281698226592,"bandpass"
"./JGE/spectrum_JGE_N.txt",1,217.4447729885244,"bandpass"
"./JGE/spectrum_JGE_NG.txt",1,1474.1801136223119,"bandpass"
"./JGE/spectrum_JGE_OW.txt",1,710.2733875487825,"bandpass"
"./JGE/spectrum_JGE_P.txt",1,1508.4747931593663,"bandpass"
"./JGE/spectrum_JGE_R.txt",1,228.97096824715678,"bandpass"
"./JGE/spectrum_JGE_S.txt",1,1859.2555793716692,"bandpass"
"./JGE/spectrum_JGE_SH.txt",1,1524.9553639614296,"bandpass"
"./JGE/spectrum_JGE_T.txt",1,1286.9637847626257,"bandpass"
"./JGE/spectrum_JGE_THen.txt",1,786.7768075143558,"bandpass"
"./JGE/spectrum_JGE_THin.txt",1,739.4977088667066,"bandpass"
"./JGE/spectrum_JGE_V.txt",1,579.035092798433,"bandpass"
"./JGE/spectrum_JGE_W.txt",1.62007685105744,139.72280828981678,"bandpass"
"./JGE/spectrum_JGE_Y.txt",1,404.3560199746313,"bandpass"
"./JGE/spectrum_JGE_Z.txt",1,327.4279987363461,"bandpass"
"./JGE/spectrum_JGE_ZH.txt",1,1435.41373781936,"bandpass"
"./JGE/spectrum_JGE_B.txt",1,3.1438415965988074,"bandstop"
"./JGE/spectrum_JGE_CH.txt",1.7862709733538504,103.42347258779942,"bandstop"
"./JGE/spectrum_JGE_D.txt",1,3.1438415965988074,"bandstop"
"./JGE/spectrum_JGE_F.txt",1.8508248584089209,93.11045917505706,"bandstop"
"./JGE/spectrum_JGE_G.txt",1.8519261637048836,86.25077585104228,"bandstop"
"./JGE/spectrum_JGE_HH.txt",1.852595522896869,85.31311072582567,"bandstop"
"./JGE/spectrum_JGE_JH.txt",1.8510152932571762,89.94716711393171,"bandstop"
"./JGE/spectrum_JGE_K.txt",1.8493649893332165,90.32389235452737,"bandstop"
"./JGE/spectrum_JGE_L.txt",1,3.1438415965988074,"bandstop"
"./JGE/spectrum_JGE_M.txt",203.73318331805004,1999.0,"bandstop"
"./JGE/spectrum_JGE_N.txt",210.66705860618643,1999.0,"bandstop"
"./JGE/spectrum_JGE_NG.txt",1,3.144152440180208,"bandstop"
"./JGE/spectrum_JGE_OW.txt",1,3.1438415965988074,"bandstop"
"./JGE/spectrum_JGE_P.txt",1,3.1438415965988074,"bandstop"
"./JGE/spectrum_JGE_R.txt",1,1420.2902049619065,"bandstop"
"./JGE/spectrum_JGE_S.txt",1,1364.2144645274434,"bandstop"
"./JGE/spectrum_JGE_SH.txt",1,1371.014003830197,"bandstop"
"./JGE/spectrum_JGE_T.txt",1,3.1438415965988074,"bandstop"
"./JGE/spectrum_JGE_THen.txt",1,3.1438415965988074,"bandstop"
"./JGE/spectrum_JGE_THin.txt",1.8214536315145646,109.75007844874116,"bandstop"
"./JGE/spectrum_JGE_V.txt",1,3.1438415965988074,"bandstop"
"./JGE/spectrum_JGE_W.txt",137.32408802436498,1999.0,"bandstop"
"./JGE/spectrum_JGE_Y.txt",80.571573828125,1680.7809551751748,"bandstop"
"./JGE/spectrum_JGE_Z.txt",49.809083201661224,1731.4977309076326,"bandstop"
"./JGE/spectrum_JGE_ZH.txt",1,3.1438415965988074,"bandstop"
"""

consonants = []
lines = txt1.split('\n')
d_bandpass = {}
d_bandstop = {}
for line in lines:
    if len(line) == 0:
        continue
    toks = line.split(',')
    fn = toks[0]
    aa = float(toks[1])
    bb = float(toks[2])
    typ = toks[3].strip('\"')
    toks = fn.split('_')
    phoneme = toks[-1][:-5].upper()
    #print(phoneme,aa,bb,typ)
    if typ == "bandpass":
        d_bandpass[phoneme] = (aa,bb)
    if typ == "bandstop":
        d_bandstop[phoneme] = (aa,bb)
    if phoneme not in consonants:
        consonants.append(phoneme)

#print(d_bandpass)
#print(d_bandstop)

vowels = "ae eh ey iy ow ay ih aa uh ao aw oy ah uw".upper().split(' ')
#consonants = "hh p n v jh k r s m g l d".upper().split(' ')
silence = "space".upper().split(' ')
sounds = vowels + consonants + silence
print(f"sounds = {sounds}")

def F2(s):
    pat = "([A-Z]+)[0-9]*"
    val = re.match(pat,s).group(1)
    val = val.upper()
    return val

def translate(word):
    L = []
    if word in x_cmudict:
        L = list(map(F2,x_cmudict[word][0]))
    print(f"L = {L}")
    L = [L[i] for i in range(len(L)) if L[i] in sounds]
    return L

def translate_s2(sent):
    L = sent.split(" ")
    M = []
    for x in L:
        M = M + translate(x)
    return M

def Plot(c,key):
    root = "./txt/"
    if c == 0:
        root = r"./txt/"
        fn1 = root + r"20230810-vowel-U.txt"
        x1 = np.loadtxt(fn1)
        f1 = x1[:,0]
        A1 = x1[:,1]

        fn2 = root + r"20230810-vowel-R.txt"
        x2 = np.loadtxt(fn2)
        f2 = x2[:,0]
        A2 = x2[:,1]

        fn3 = root + r"20230810-vowel-T.txt"
        x3 = np.loadtxt(fn3)
        f3 = x3[:,0]
        A3 = x3[:,1]

        fn4 = root + r"20230810-vowel-V.txt"
        x4 = np.loadtxt(fn4)
        f4 = x4[:,0]
        A4 = x4[:,1] 
    elif c == 1:
        root = r"./txt/"
        fn1 = root + r"20230810-fricative-U.txt"
        x1 = np.loadtxt(fn1)
        f1 = x1[:,0]
        A1 = x1[:,1]

        fn2 = root + r"20230810-fricative-R.txt"
        x2 = np.loadtxt(fn2)
        f2 = x2[:,0]
        A2 = x2[:,1]

        fn3 = root + r"20230810-fricative-T.txt"
        x3 = np.loadtxt(fn3)
        f3 = x3[:,0]
        A3 = x3[:,1]

        fn4 = root + r"20230810-fricative-P.txt"
        x4 = np.loadtxt(fn4)
        f4 = x4[:,0]
        A4 = x4[:,1]

        fn5 = root + r"20230810-fricative-Z.txt"
        x5 = np.loadtxt(fn5)
        f5 = x5[:,0]
        A5 = x5[:,1]

        fn6 = root + r"20230810-fricative-V.txt"
        x6 = np.loadtxt(fn6)
        f6 = x6[:,0]
        A6 = x6[:,1] 

    flag = True
    if flag:
        import matplotlib.pyplot as plt
        N = 90
        if c == 0:
            plt.plot(f1[:N],A1[:N],'r',label='U')
            plt.plot(f2[:N],A2[:N],'b',label='R')
            plt.plot(f3[:N],A3[:N],'g',label='T')
            plt.plot(f4[:N],A4[:N],'c',label='V')
        elif c == 1:
            plt.plot(f1[:N],A1[:N],'r',label='U')
            plt.plot(f2[:N],A2[:N],'b',label='R')
            plt.plot(f3[:N],A3[:N],'g',label='T')
            plt.plot(f4[:N],A4[:N],'y',label='P')
            plt.plot(f5[:N],A5[:N],'k',label='Z')
            plt.plot(f6[:N],A6[:N],'c',label='V')
        plt.legend()
        plt.xlabel("Frequency")
        plt.ylabel("dBA Loudness")
        plt.title(f"Freq Spect key={key}")
        plt.show()

    I = lambda A: [i for i in range(1,len(list(A))-1) if A[i-1] < A[i] and A[i+1] < A[i]]
    F = lambda f,A: list([(f[i],A[i]) for i in I(A)])[:20]
    L = lambda f: list([f*n for n in range(1,12)])
    def D(L):
        for tup in L:
            print(tup)
        return

    #D(F(f1,A1))
    print()
    #D(F(f2,A2))
    #print()
    #D(F(f3,A3))

    def Overlap(A1,A2):
        from math import exp,log
        B1 = list(map(exp, list(A1)))
        B2 = list(map(exp, list(A2)))
        v = np.inner(B1,B2)
        w = log(v)
        return w
    #print((Overlap(A1,A2)))
    return
d1 = {}
d1["AE"] = [[1204, 464, 547],14] # sad, poles
d1["EH"] = [[323, 464, 765],14] # said
d1["EY"] = [[917, 1678, 567],14] # say
d1["IY"] = [[58, 250, 330],14] # seat
d1["OW"] = [[694, 907, 939],14] # sewed
d1["AY"] = [[217, 698, 485],14] # sight
d1["IH"] = [[884, 930, 921],14] # sit
d1["AA"] = [[812, 772, 680],14] # sod
d1["UH"] = [[542, 559, 939],14] # soot
d1["AO"] = [[282, 654, 434],14] # sought
d1["AH"] = [[282, 654, 434],14] # sought
d1["AW"] = [[536, 1525, 761],14] # south
d1["OY"] = [[1758, 884, 1528],14] # soy
d1["OE"] = [[158, 87, 221],14] # suds, actually schwa
d1["UW"] = [[108, 351, 424],14] # suit
d1["CH"] = [[2000,4000],[125, 250,500,1000],30] # poles,zeros
d1["S"] =  [[2000,3000,4000],[261,936,1201],30] # poles,zeros
d1["TH"] =  [[700],[124],29] # poles,zeros
K = list(d1.keys())

dur_secs = 0.5 # seconds
# Formants, M
flag_vowel = True

##sent = "sat say"
##M = translate_s2(sent)
##M = ['S','IY','SPACE', 'S','EY','SPACE',
##     'CH','IY','SPACE', 'CH','EY','SPACE',
##     'TH','AE','SPACE', 'TH','UH']
##M = ['S','IY']
M = "K UH N G R AE D UW L EY SH UH N SPACE AE N D SPACE HH AE P IY SPACE AE N AH V EH S UH R IY".split(' ')
M = "HH AE P IY SPACE AE N AH V EH S UH R IY".split(' ')
speed = 2 # speed multiplier for dur
print(f"M = {M}")
root = r"./"
tenor = [125,4000] # freq = 131 is fundamental
vocal_range0,freq0 = tenor,131
flag_write_audio = True
if flag_vowel:
    song = None
    count = 0
    for key in M:
        print(key)
        fn_save_key = f"./tmp-20230809.wav"
        vowel_flag = key in vowels
        consonant_flag = key in consonants
        silence_flag = key in silence
        if vowel_flag:
            dur = 0.5/speed
            vs.create_sound(dur,
                 poles = d1[key][0],
                 dB0 = d1[key][1],
                 fn_save=fn_save_key,
                 freq = freq0,
                 vocal_range = vocal_range0,
                 fn_spec_save = "20230810-vowel",
                 plot=False,
                 create=True)
            #Plot(c=0,key=key)
        elif consonant_flag:
            # /s/
            dur = 0.125/speed
            try:
                bp = d_bandpass[key]
            except:
                bp = []
            try:
                bs = d_bandstop[key]
            except:
                bs = []
            print(f"key, bp = {bp}, bs = {bs}")
            H,X = cs.create_consonant_bp_bs(dur,
                    bp,bs,verbose=False)
            Y = H * X # apply filter
            y = sf.ifft(Y) # audio signal output
            y = [y[j].real for j in range(len(y))]
            #if i == 0:
            #    show_glottis = True
            #else:
            #    show_glottis = False
            #cs.Plot_XY(5+i*5,X,Y,phoneme,show_glottis)
            y2 = np.array(y,dtype=np.int16)
            data = np.zeros((len(y2),2),dtype=np.int16)
            data[:,0] = y2
            data[:,1] = y2
            si.wavfile.write(fn_save_key,
                    cs.sampling_rate,
                    data.astype(np.int16))
            #Plot(c=1,key=key)
        elif silence_flag:
            dur = 0.05
            y2 = np.zeros((int(cs.sampling_rate*dur)),dtype=np.int16)
            data = np.zeros((len(y2),2),dtype=np.int16)
            data[:,0] = y2
            data[:,1] = y2
            si.wavfile.write(fn_save_key,
                    cs.sampling_rate,
                    data.astype(np.int16))       
        count = count + 1
        if flag_write_audio:
            import pydub
            if song is None:
                if vowel_flag:
                    print(f"1. dur = {dur}, d1['{key}'] = {d1[key]}")
                if consonant_flag:
                    print(f"1. dur = {dur}, key = {key}")
                song = pydub.AudioSegment.from_wav(fn_save_key)
            else:
                if vowel_flag:
                    print(f"2. dur = {dur}, d1['{key}'] = {d1[key]}")
                if consonant_flag:
                    print(f"1. dur = {dur}, key = {key}")
                song0 = pydub.AudioSegment.from_wav(fn_save_key)
                song = song + song0
            if song is not None:
                song.export(root+"/speech_synth_03.mp3",format="mp3")

flag_plot_spec = True
if flag_plot_spec:
    c = 1
  
