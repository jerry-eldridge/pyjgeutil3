import pyvista as pv
from pyvistaqt import BackgroundPlotter
import numpy as np
import time

from math import pi,sin

##c:\_Python312-64-tf>.\python -m pip install PyQt6
##c:\_Python312-64-tf>.\python -m pip install pyvista
##c:\_Python312-64-tf>.\python -m pip install pyvistaqt

BIGDATA = r"C:/JGE_Universes/obj/"

fn_save = BIGDATA+"Bed-01.obj"

root = BIGDATA
root_render = r"C:/JGE_Universes/render3/"

# Load the .obj file
barstool = pv.read(fn_save)

# Set up the plotter
plotter = BackgroundPlotter()
green_screen = [0,177,64] # R,G,B
plotter.set_background(green_screen)
# Add the mesh to the plotter
texture_barstool = pv.read_texture(root+"Image_1.png")
actor_barstool = plotter.add_mesh(barstool,
        texture=texture_barstool,
        smooth_shading=True)

# Set up camera and plotter details
plotter.show()

thetax = 0
dthetax = 1
dt = 15/1000
freq = 1/2
tmin = 0
tmax = 1
t = tmin
s = t
c = 0
frames_per_second = 30
ds = 1/frames_per_second
while t < tmax:
    tx = 2*sin(2*pi*freq*t)
    T = [tx,0,0]
    R = [thetax,0,0]
    S = [1,1,1]
    actor_barstool.SetPosition(*T)
    actor_barstool.SetOrientation(*R)
    actor_barstool.SetScale(*S)
    plotter.update()
    plotter.render()
    if abs(s - t) < dt:
        plotter.screenshot(\
            f"{root_render}frame_{c:05d}.png")
        s = s + ds
        c = c + 1
    time.sleep(dt)
    thetax = thetax + dthetax
    t = t + dt

plotter.close()


