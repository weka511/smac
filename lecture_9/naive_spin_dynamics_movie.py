import random, math, pylab, matplotlib.image, os

up   = matplotlib.image.imread('spin_up.png')
down = matplotlib.image.imread('spin_down.png')
img = 0
if not os.path.isdir('output'): os.mkdir('output')
def snapshot(state, T, t):
    global img
    fig = pylab.figure(frameon=False, figsize=(260 / 100., 270 / 100.), dpi=100)
    ax = pylab.Axes(fig, [0, -0.05, 1., float(241) / float(270) -0.05])
    ax.set_axis_off()
    fig.add_axes(ax)
    if state == 1:
        ax.imshow(up, aspect='auto')
    elif state == -1:
        ax.imshow(down, aspect='auto')
    pylab.text(0.1, 1.05, 'T = ' + str(T), horizontalalignment='left', verticalalignment='bottom',
                transform=ax.transAxes, fontsize=20, color = '#700000', fontweight='bold')
    pylab.text(0.12, 0.94, 't = ' + str(t), horizontalalignment='left', verticalalignment='bottom',
                transform=ax.transAxes, fontsize=20, color = '#202157', fontweight='bold')
    fig.savefig('output/%03d.png' % img, transparent=True)
    img += 1
    pylab.close(fig)

h = 1.0
T = 3.
p = math.exp(- 2.0 * h / T)
tmax = 10
sigma = 1
for t in range(tmax):
    print t
    snapshot(sigma, T, t)
    if sigma == -1:
        sigma = 1
    elif random.uniform(0.0, 1.0) < p:
        sigma = -1
