import random, pylab

random.seed('1234')
sigma = 0.4
epsilon = 0.4  # probability to switch from red to blue pebble, and vice versa
pylab.figure()
s_map_red =  [(1.0, 1.0), (2.0, 1.0), (3.0, 1.0), 
              (1.0, 2.0), (2.0, 2.0), (3.0, 2.0), 
              (1.0, 3.0), (2.0, 3.0), (3.0, 3.0)] 
offset = 3.0
s_map_blue = [(x+offset,y-offset) for (x,y) in s_map_red]
neighbor =  [[1, 3, 0, 0], [2, 4, 0, 1], [2, 5, 1, 2],
             [4, 6, 3, 0], [5, 7, 3, 1], [5, 8, 4, 2],
             [7, 6, 6, 3], [8, 7, 6, 4], [8, 8, 7, 5]]
color = 'red'  #chose 'red' or 'blue'
site = 8
tmax = 240
for iter in range(tmax):
    period = 4
    if (iter%period) == 0:
	# Begin of graphical output
        maxlength = len(str(tmax-1))
        number_string = str(iter).zfill(maxlength)
        if color == 'red':  cir = pylab.Circle(s_map_red[site],  radius=sigma, fc='r')
        if color == 'blue': cir = pylab.Circle(s_map_blue[site], radius=sigma, fc='b')
	pylab.figure()
        pylab.gca().add_patch(cir)
        pylab.plot([0.5, 3.5], [0.5, 0.5], 'r')
        pylab.plot([0.5, 3.5], [1.5, 1.5], 'r')
        pylab.plot([0.5, 3.5], [2.5, 2.5], 'r')
        pylab.plot([1.5, 1.5], [0.5, 3.5], 'r')
        pylab.plot([2.5, 2.5], [0.5, 3.5], 'r')
        pylab.plot([3.5, 3.5], [0.5, 3.5], 'r')
        pylab.plot([0.5+offset, 3.5+offset], [1.5-offset, 1.5-offset], 'b')
        pylab.plot([0.5+offset, 3.5+offset], [2.5-offset, 2.5-offset], 'b')
        pylab.plot([0.5+offset, 3.5+offset], [3.5-offset, 3.5-offset], 'b')
        pylab.plot([0.5+offset, 0.5+offset], [0.5-offset, 3.5-offset], 'b')
        pylab.plot([1.5+offset, 1.5+offset], [0.5-offset, 3.5-offset], 'b')
        pylab.plot([2.5+offset, 2.5+offset], [0.5-offset, 3.5-offset], 'b')
        pylab.title('t = '+ number_string)
        pylab.axis('scaled')
        pylab.axis([0.5, 6.5, -2.5, 3.5])
        pylab.xticks([])
        pylab.yticks([])
        number_string_filename = str(iter/period).zfill(3)
        pylab.savefig('pebble_dual_movie_epsilon_'+number_string_filename+'.png', transparent=True)
        pylab.clf()
        pylab.close()
	# End of graphical output
    newsite = neighbor[site][ random.randint(0, 3)]
    newcolor = color
    if (color == 'red') and (site == 2) and (newsite == 2):
        if random.random() < epsilon:
            newcolor = 'blue'
            newsite = 6
            print "transition red->blue at time = ", iter
    if (color == 'blue') and (site == 6) and (newsite == 6):
        if random.random() < epsilon:
            newcolor = 'red'
            newsite = 2
            print "transition blue->red at time = ", iter
    site = newsite
    color = newcolor
