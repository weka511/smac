import math, random, pylab

sigma = 0.4
epsilon = 0.1
pylab.figure()
s_map = [(1.0, 1.0), (2.0, 1.0)] 
neighbor =  [[1], [0]]
pos = 0
tmax = 20
for iter in range(tmax):
    # Begin of the graphics output
    pylab.figure()
    number_string = str(iter).zfill(len(str(tmax)))
    cir = pylab.Circle(s_map[pos], radius=sigma, fc='r')
    pylab.gca().add_patch(cir)
    pylab.plot([1.5, 1.5], [0.5, 1.5], 'b')
    pylab.title('t = '+ number_string)
    pylab.axis('scaled')
    pylab.axis([0.5, 2.5, 0.5, 1.5])
    pylab.xticks([])
    pylab.yticks([])
    pylab.savefig('2x1pebble_epsilon'+number_string+'.png', transparent=True)
    pylab.close()
    # End of the graphics output
    newpos = neighbor[pos][0]
    if random.random() < epsilon:
        newpos = pos
    pos = newpos
