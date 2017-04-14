import random, pylab, os

output_dir = 'random_sequential_discrete_movie'
if not os.path.exists(output_dir): os.makedirs(output_dir)
def show_rods(red_rod, blue_rod, run, trial, frame):
    fig, ax = pylab.subplots()
    ax.set_xticks([0, 1, 2, 3, 4])
    ax.set_yticks([])
    height = 1.0
    redrect = pylab.Rectangle((red_rod - 1.5, 0.0), 3.0, 1.1 * height,  fc = 'r')
    pylab.gca().add_patch(redrect)
    bluerect = pylab.Rectangle((blue_rod-1.5,0.0), 3.0, height,  fc = 'b')
    pylab.gca().add_patch(bluerect)
    pylab.axis('scaled')
    pylab.axis([-1.5, 5.5, 0.0, 2.5*height])
    pylab.xlabel("x")
    if abs(red_rod - blue_rod) > 2:
        pylab.title('run %d, trial %d (ACCEPTED!)' % (run, trial))
    else:
        pylab.title('run %d, trial %d (REJECTED!)' % (run, trial))
    pylab.savefig(output_dir+'/random_sequential_discrete_frame%04i.png' % (frame))
    pylab.close()

configurations = {(0, 3): 'a', (0, 4): 'b', (1, 4): 'c', 
                  (3, 0): 'd', (4, 0): 'e', (4, 1): 'f'}
counts = {'a': 0, 'b': 0, 'c': 0, 'd': 0, 'e': 0, 'f': 0}
n_runs = 10
frame = 0
trial = 0
for run in range(n_runs):
    red_rod = random.randint(0, 3)
    if red_rod >= 2: red_rod += 1
    trial = 0
    while True:
        blue_rod = random.randint(0, 4)
        show_rods(red_rod, blue_rod, run, trial, frame)
        trial += 1
        frame += 1
        if abs(red_rod - blue_rod) > 2: break
    conf = configurations[(red_rod, blue_rod)]
    counts[conf] += 1
for conf in counts:
    print (conf, counts[conf] / float(n_runs))
