README.txt

Use hello-1b.cog2 in the "samples4\AudioCompress2\cog2\"
folder for "samples4\Cog2Codec2\" folder. Also one can
use 2_Record_Cog_File.py and save or rename the file for
later reading and playing it with 1_Play_Cog_File.py

Sound is sensed from environment -->
listen to microphone --> 
create cog2 y_l and y_r data --> 
save cog2 data to .cog2 file --> 
read .cog2 file --> 
get cog2 y_l and y_r data --> 
create audio data array data2 -->
save data2 array to .wav file --> 
play .wav file --> 
produce audio at speakers -->
Sound is actuated onto environment .

The required python3 libraries were previously installed using
"pip install <library>". Since I installed

I would open a command shell (Window Search for "cmd") and do:

(It uses python3 built-in libraries 'decimal' and 'wave' and 'zlib'
which likely do not need to be pip installed)

python -m pip install numpy
python -m pip install scipy
python -m pip install PyAudio
python -m pip install sounddevice --user

using wherever python is located.

