import random, math, pylab

def show_spins(S0, S1, L, label):
    pylab.set_cmap('hot')
    conf0 = [[0 for x in range(L)] for y in range(L)]
    conf1 = [[0 for x in range(L)] for y in range(L)]
    for k in range(N):
        y = k // L
        x = k - y * L
        conf0[x][y] = S0[k]
        conf1[x][y] = S1[k]
    pylab.subplot(1, 2, 1)
    pylab.imshow(conf0, extent=[0, L, 0, L], interpolation='nearest')
    pylab.title('S0 ' + label)
    pylab.subplot(1, 2, 2)
    pylab.imshow(conf1, extent=[0, L, 0, L], interpolation='nearest')
    pylab.title('S1 ' + label)
    pylab.tight_layout()
    pylab.savefig('plot_' + label + '.png')
    pylab.close()

def label(step,L,T):
    return 'C2_Step_{0}_L_{1}_T_{2}'.format(step,L,T)

L = 32
N = L * L
nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N) \
                                    for i in range(N)}

T = 3.0
beta = 1.0 / T
S0 = [1] * N
S1 = [-1] * N
step = 0
while True:
    step += 1
    k = random.randint(0, N - 1)
    Upsilon = random.uniform(0.0, 1.0)
    h = sum(S0[nn] for nn in nbr[k])
    S0[k] = -1
    if Upsilon < 1.0 / (1.0 + math.exp(-2.0 * beta * h)):
        S0[k] = 1
    h = sum(S1[nn] for nn in nbr[k])
    S1[k] = -1
    if Upsilon < 1.0 / (1.0 + math.exp(-2.0 * beta * h)):
        S1[k] = 1
    if step % N == 0:
        n_diff = sum(abs(S0[i] - S1[i]) for i in range(N))
        if n_diff == 0:
            t_coup = step / N
            print ('coupling time: {0}'.format( t_coup))
            break
        if step % 10 ==0:
            print (step, n_diff)
            show_spins(S0, S1, L, label(step,L,T))
            
show_spins(S0, S1, L, label(step,L,T))