import pylab
from matplotlib.patches import FancyArrowPatch

def plot_spin(c, filename, L):
    s = 1.0 / L
    for i in range(L):
        for j in range(L):
            x, y, dy = (i + 0.5) * s, (j + 0.5) * s, 0.85 * s * c[i][j]
            arrow = FancyArrowPatch((x, y - 0.5 * dy), (x, y + 0.5 * dy),
                    color='.2', lw=0, alpha=.8, arrowstyle="Simple" +
                    ", head_length=" + str(1.3 * 150 * s) +
                    ", head_width=" + str(1.3 * 150 * s) +
                    ", tail_width=" + str(1.3 * 40 * s))
            pylab.gca().add_patch(arrow)
    pylab.axis('scaled')
    pylab.axis([0, 1, 0, 1])
    pylab.gca().set_xticks([])
    pylab.gca().set_yticks([])
    [pylab.axhline(y=(i * s), ls='--', c='.2') for i in range(L)]
    [pylab.axvline(x=(j * s), ls='--', c='.2') for j in range(L)]
    pylab.savefig(filename)
    pylab.clf()

def gray_flip(t, N):
    k = t[0]
    if k > N: return t, k
    t[k - 1] = t[k]
    t[k] = k + 1
    if k != 1: t[0] = 1
    return t, k

L = 2
N = L * L
site_dic = {(j // L, j - (j // L) * L) : j for j in range(N)}
S = [-1] * N
plot_spin([[S[site_dic[(a, b)]] for a in range(L)] for b in range(L)], 'spin_config_%04i.png' % 0, L)
tau = range(1, N + 2)
for i in range(1, 2 ** N):
    tau, k = gray_flip(tau, N)
    S[k - 1] *= -1
    plot_spin([[S[site_dic[(a, b)]] for a in range(L)] for b in range(L)], 'spin_config_%04i.png' % i, L)
