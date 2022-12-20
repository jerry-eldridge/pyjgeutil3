import cog2_codec as cog2
import record_audio_data as rad
import play_audio_data as pad

root = r"./"
wavroot = r"./"
fn_cog = root + "demo-1.cog2"

# we use a .wav file as the tmp file for use
# when script / program is running
fn_tmp_wav = root + "20221220-tmp-512405.wav"

chunk = 1024
f_c = 1000 # Recommended: 1000,2000,4000,etc.
zlib_level = 1
sampling_rate0 = 44100

# Record audio and save as Cog2
print("Starting to listen...")
data1, sampling_rate1 = rad.listen(\
    sampling_rate=sampling_rate0)
print("Done listening...")

print("Audio data to Cog2")
y_l1,y_r1 = cog2.Data2Cog2Bytes(data1,sampling_rate1,
        chunk,f_c,zlib_level)

print("Saving Cog2 to Cog2 file, fn_cog =",fn_cog)
cog2.SaveCog2(fn_cog,
            y_l1,y_r1,sampling_rate1,chunk)

# Play back cog file
print("Reading Cog2 file, fn_cog =", fn_cog)
y_l2,y_r2,sampling_rate2,chunk2 = cog2.ReadCog2(\
    fn_cog)
print("Cog2 to Audio data")
data2 = cog2.Cog2Bytes2Audio(y_l2,y_r2,chunk2)
print("Saving Audio data to Wav file")
cog2.SaveAudio2Wav(fn_tmp_wav,sampling_rate2,data2)
print("Playing Wav file")
pad.PlayAudio(fn_tmp_wav)



