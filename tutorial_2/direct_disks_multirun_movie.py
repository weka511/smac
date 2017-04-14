import random, math, pylab, os

def dist(x,y):
    d_x = abs(x[0] - y[0]) % 1.0
    d_x = min(d_x, 1.0 - d_x)
    d_y = abs(x[1] - y[1]) % 1.0
    d_y = min(d_y, 1.0 - d_y)
    return  math.sqrt(d_x**2 + d_y**2)
    
def direct_disks(N, sigma):
    n_iter = 0
    condition = False
    while condition == False:
        n_iter += 1
        L = [(random.random(), random.random())]
        for k in range(1, N):
            a = (random.random(), random.random())
            min_dist = min(dist(a, b) for b in L) 
            if min_dist < 2.0 * sigma: 
                condition = False
                break
            else:
                L.append(a)
                condition = True
    return n_iter, L

img = 0
output_dir = 'direct_disks_multirun_movie'
if not os.path.exists(output_dir): os.makedirs(output_dir)
def snapshot(pos, colors, border_color = 'k'):
    global img
    pylab.figure()
    pylab.axis([0, 1, 0, 1])
    [i.set_linewidth(2) for i in pylab.gca().spines.values()]
    [i.set_color(border_color) for i in pylab.gca().spines.values()]
    pylab.setp(pylab.gca(), xticks = [0, 1], yticks = [0, 1], aspect = 'equal')
    for (x, y), c in zip(pos, colors):
        circle = pylab.Circle((x, y), radius = sigma, fc = c)
        pylab.gca().add_patch(circle)
    pylab.savefig(output_dir+'/snapshot_%03i.png'%img)
    pylab.close()
    img += 1

def periodicize(config):
    images = [-1.0, 0.0, 1.0]
    return [(x + dx, y + dy) for (x,y) in config for dx in images for dy in images]

N = 16
eta = 0.28
sigma = math.sqrt(eta / N / math.pi)
n_runs = 8
colors = ['r' for i in range(8 * N)]
for run in range(n_runs):
    iterations, config =  direct_disks(N, sigma)
    print ('run',run)
    print (iterations - 1, 'tabula rasa wipe-outs before producing the following configuration')
    print (config)

    config_per = periodicize(config)
    snapshot(config_per, colors, border_color = 'k')
