import vowel_synthesis as vs

flag_vowel = True

dur_secs = 1 # seconds
# Formants, M
M1 = [370,3200,3700] # [i], child
M2 = [430, 1150, 3250] # [u], child
M3 = [917, 1678, 765] # [e], JGE
if flag_vowel:
##    vs.create_sound(dur_secs, M1,dB0=14,
##                 fn_save="IY-20230809.wav",
##                 plot=True,
##                 create=True)
##    vs.create_sound(dur_secs, M2,dB0=14,
##                 fn_save="UW-20230809.wav",
##                 plot=True,
##                 create=True)
    vs.create_sound(dur_secs, M1 = [917, 1678, 765],
                    dB0=14,
                 fn_save="JGE-EY-20230809.wav",
                 freq = 124,
                 plot=False,
                 create=True)
    vs.create_sound(dur_secs, M1 =[323,464,765],
                 dB0=14,
                 fn_save="JGE-EH-20230809.wav",
                 freq = 124,
                 plot=False,
                 create=True)    
    vs.create_sound(dur_secs, M1 =[58,250,330],
                 dB0=14,
                 fn_save="JGE-IY-20230809.wav",
                 freq = 124,
                 plot=False,
                 create=True)
