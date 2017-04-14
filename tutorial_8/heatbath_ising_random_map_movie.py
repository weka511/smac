import random, math, os, pylab
from matplotlib.patches import FancyArrowPatch

output_dir = 'snapshots'
if not os.path.exists(output_dir): os.makedirs(output_dir)
def plot_many_configurations(conf, filename, L, colors={}):
    pylab.figure(figsize=(6 * len(conf), 6))
    s = 1.0 / L
    for i_c in range(len(conf)):
        c = conf[i_c]
        pylab.subplot(1, len(conf), i_c + 1)
        for l in range(L ** 2):
            x, y = ((l // L) + 0.5) * s, ((l - (l // L) * L) + 0.5) * s
            dy = c[l] * 0.85 / float(L)
            arrow = FancyArrowPatch((x, y - 0.5 * dy), (x, y + 0.5 * dy), \
                    fc=colors[l], color='.2', lw=0, alpha=.8, \
                    arrowstyle="Simple, head_length=" + str(0.9 * 150 * s) \
                    + ", head_width=" + str(0.9 * 150 * s) + ", tail_width=" \
                    + str(0.9 * 40 * s))
            pylab.gca().add_patch(arrow)
        pylab.axis('scaled')
        pylab.axis([0, 1, 0, 1])
        pylab.gca().set_xticks([])
        pylab.gca().set_yticks([])
        [pylab.axhline(y=(i * s), ls='--', c='.2', lw=0.5) for i in range(L)]
        [pylab.axvline(x=(j * s), ls='--', c='.2', lw=0.5) for j in range(L)]
    pylab.tight_layout()
    pylab.savefig(output_dir + '/' + filename)
    pylab.clf()

L = 6
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N) \
                                    for i in range(N)}
filename = 'data_L%i.txt' % L
if os.path.isfile(filename):
    f = open(filename, 'r')
    S1 = [int(i) for i in f.read().split()]
    f.close()
    if len(S1) != N: exit('wrong input')
    print 'initial config read from', filename
else:
    S1 = [random.choice([-1, 1]) for i in range(N)]
    print 'random initial config'
S2 = [1] * N
nsteps = 10000
nskip  = 10     # plot a snapshot every nskip steps
beta = 0.4
random.seed('abcde')
for step in range(nsteps):
    k = random.randint(0, N - 1)
    Upsilon = random.uniform(0.0, 1.0)
    h1 = sum(S1[nn] for nn in nbr[k])
    S1[k] = -1
    if Upsilon < 1.0 / (1.0 + math.exp(-2.0 * beta * h1)): S1[k] = 1
    h2 = sum(S2[nn] for nn in nbr[k])
    S2[k] = -1
    if Upsilon < 1.0 / (1.0 + math.exp(-2.0 * beta * h2)): S2[k] = 1
    if S1 == S2:
        print 'step %i: coupling' % step
        plot_many_configurations([S1, S2], 'snap_%06i.png' % step, L, {j : 'g' for j in range(N)})
        break
    else:
        print 'step %i: no coupling yet, %i different spins' % (step, sum(S1[ii] != S2[ii] for ii in range(N)))
    # begin graphic output
    # colormap: green for equal spins, red for different spins, blue for site k
    if step % nskip == 0:
        colors = {j : (S1[j] == S2[j]) * 'g' + (S1[j] != S2[j]) * 'r' for j in range(N)}
        colors[k] = 'b'
        plot_many_configurations([S1, S2], 'snap_%06i.png' % step, L, colors)
