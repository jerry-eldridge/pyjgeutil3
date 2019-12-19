import matplotlib.pyplot as plt

fig = plt.figure()
ax = fig.add_subplot(111)
im = plt.imread("CircleLens.png")
ax.imshow(im)

poly = []
def onclick(event):
    global poly
    pt0 = [event.x, event.y]
    pt = [event.xdata, event.ydata]
    if event.button == 3: # Right Mouse Button
        print "poly=",poly
        poly = []
    if event.button == 1: # Left Mouse Button
        poly.append(pt)
        print len(poly),pt
        
cid = fig.canvas.mpl_connect('button_press_event', onclick)

plt.show()
