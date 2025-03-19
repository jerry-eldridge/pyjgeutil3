README_mathematics_song.txt

The script 7_play_synth_music.py was run in python3
with audio in  root_A or the ./audio2/ subfolder
of me singing "Mathematics built this song. 
Mathematics is so very interesting. Mathematics
built this song.". The result is in root_B two
files for each .wav file in root_A (with a pause
of a matplotlib plot between each song so close the
plot window to iterate to next song). A 
mathematics_built_this_song2.txt a .txt version of
the sung .wav file and a synthesized song-0000.wav
version which uses the number of files in root_A
to index so one needs to manually rename these
song-nnnn.wav to a name in between code run.

All songs in the songs folders are .txt files which
I just improvised.

The lyrics for songs:

happy.wav - JGE singing lyrics "happy birthday to you. 
happy birthday to you." 

which is me seeing the classic song but all other songs
were originals.

song1.wav - JGE improving on the piano

mathematics_built_this_song.wav - JGE singing "Mathematics
built this song. Mathematics its so very interesting.
Mathematics built this song.".

planting_flowers.wav - JGE singing lyrics "I hope you had fun 
planting flowers." another original lyrics and song.

planting_flowers2.wav - JGE sing

song-0000-01.wav - JGE mathematics song synth
song-0000-02.wav - JGE mathematics song synth with Audacity
Reverb applied

Audacity was used for recording speech on a webcam microphone
and then for the "mathematics built this song" song, I applied
a tempo change to slowed down the song somewhat so that
the python3 script mentioned below could better recognize
the notes, and after synth, I shortened the tempo, and then
applied a Reverb effect on the audio.

The python libraries used are 

$ cd <python_root>
$ ./python -m pip install numpy scipy matplotlib
sounddevice seaborn praat-parselmouth

or any other ones indicated.

root = r"./audio2/"
root_A = root
root1 = r"./songs1/"
root2 = r"./songs2/"
root3 = r"./songs3/"
root_B = root3
L = ListFiles(root_A,"*.wav")
n = 1
for fn in L:
    fn_save = root_B+f"tmptmp-{n:04d}.txt"
    ## uncomment to create tmptmp-nnnn.txt files
    ## from .wav files in ./audio/ folder.
    
    #DisplayVowels(fn_save,[fn],N=10)
    
    n = n + 1
N = len(L)
N = 2
L2 = ListFiles(root_B,"*.txt")
for n in range(len(L2)):
     tup = L2[n]
     fn = tup[2]+tup[3]
     print(fn)
     fn_audio_save = root_B+f"song-{n:04d}.wav"
     song_array(fn,sr,fn_audio_save)

and one needs to change "#DisplayVowel(...)" to
"DisplayVowel(...)" by uncommenting the "#" to
create the files .txt and .wav from the original
sung or piano played .wav file.
