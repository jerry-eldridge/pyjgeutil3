# pyjgeutil3
Collection of Python3 Utility libraries utility tools relating to math, physics, computer science by Jerry Gerard Eldridge.

Download samples elsewhere and run pointing to Utility3 folder.
To use download the folder Utility into "c:\_PythonJGE\Utility3" and create a folder BIGDATA = r"C:\_BigData\_3D\my_scenes\"
where some .obj samples of 3D objects will be created. To install opencv-python do "pip install opencv-python" and
"pip install tripy" within path where Python3 is located. First, install Python3 from the python website.
https://www.python.org/downloads/ . The tripy library does simple polygon triangulation and opencv-python is used for
2D graphics and python3 is used to run the scripts via Run > Run Module in idle.bat in the Python3 folder. Preferably,
install python to a folder on C: instead of in a local apps folder where the files like python, its tools like pip,
and idle can be seen. The .obj file could be viewed with a model viewer or using Windows 10 Fall Creator's Update
for viewing 3D .obj files for 3D graphics.

Requirements

Windows 10 command shell for commands like: 'pip install opencv-python' and 'pip install tripy' by searching for
"cmd" in Windows 10 search box. Also, numpy and scipy is installed currently with
"pip install numpy scipy matplotlib ipython jupyter pandas sympy nose" or see numpy/scipy website for install instructions.

The Utility folder "C:\_PythonJGE\Utility3" is assumed to exist containing this library unzipped there by default
in the samples scripts. This is pointed to in commands "import sys" and "sys.path.insert(0,r"C:\_PythonJGE\Utility3")
in python scripts.

Then for example "import affine as aff" makes use of a script. The 3D .obj creating scripts
point to a folder "C:\_BigData\_3D\my_scenes" by defining
BIGDATA = r"C:/_BigData/_3D/my_scenes/" in those scripts and that folder should be
created or another and BIGDATA adjusted for change to save the created .obj files to
that common folder.

