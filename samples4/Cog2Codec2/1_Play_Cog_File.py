import cog2_codec as cog2
import play_audio_data as pad

root = r"./"
wavroot = r"./"
fn_wav = wavroot + "demo-1a.wav"
fn_cog = root + "demo-1.cog2" # created from record audio
fn_tmp_wav = root + "20221220-tmp-512405.wav"

chunk = 1024
f_c = 1000 # Recommended: 1000,2000,4000,etc.
zlib_level = 1

create_cog = False
if create_cog:
    y_l,y_r,sampling_rate = cog2.Wav2Cog2Bytes(\
        fn_wav,chunk,f_c,zlib_level)
    cog2.SaveCog2(fn_cog,y_l,y_r,sampling_rate,chunk)

y_l2,y_r2,sampling_rate2,chunk2 = cog2.ReadCog2(\
    fn_cog)
data2 = cog2.Cog2Bytes2Audio(y_l2,y_r2,chunk2)
cog2.SaveAudio2Wav(fn_tmp_wav,sampling_rate2,data2)
pad.PlayAudio(fn_tmp_wav)

