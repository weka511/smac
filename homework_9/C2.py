import random, math, pylab

def dist(x, y):
    return math.sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def tour_length(cities, N):
    return sum(dist(cities[k + 1], cities[k]) for k in range(N - 1)) + dist(cities[0], cities[N - 1])

def propose(N,cities,cuttoff1=0.2,cutoff2=0.6):
    'Propose a new tour'
    p = random.uniform(0.0, 1.0)
    if p  < cuttoff1:  # randomly reverse part of cities
        i = random.randint(0, N / 2)
        cities = cities[i:] + cities[:i] #change starting point of cycle
        i = random.randint(0, N / 2)
        a = cities[:i]                   # head (random length)
        a.reverse()                      
        new_cities =  a + cities[i:]     # head is reverses
    elif p < cutoff2:                        # randomly move one city
        new_cities = cities[:]
        i = random.randint(1, N - 1)
        a = new_cities.pop(i)
        j = random.randint(1, N - 2)
        new_cities.insert(j, a)
    else:                               # randomly swap two cities
        new_cities = cities[:]
        i = random.randint(1, N - 1)
        j = random.randint(1, N - 1)
        new_cities[i] = cities[j]
        new_cities[j] = cities[i]
    new_energy =  tour_length(new_cities, N)
    return (new_cities,new_energy)

N = 100
random.seed(54321)
cities = [(random.uniform(0.0, 1.0), random.uniform(0.0, 1.0)) for i in range(N)]
random.seed()
random.shuffle(cities)
beta = 1.0
n_accept = 0
best_energy = float('inf')
energy =  tour_length(cities, N)
for step in range(100000000):
    if n_accept == 100:
        beta *=  1.0005
        n_accept = 0    
    (new_cities,new_energy)=propose(N,cities)
    # accept - NB if new_energy < energy, probability=1
    if random.uniform(0.0, 1.0) < math.exp(- beta * (new_energy - energy)):
        n_accept += 1
        energy = new_energy
        cities = new_cities[:]
        if energy < best_energy:
            best_energy = energy
            best_tour = cities[:]
    if step % 100000 == 0:
        print ('{0} {1:,d} {2}'.format(energy, step, 1.0 / beta))
        
cities = best_tour[:]
for i in range(1, N):
    pylab.plot([cities[i][0], cities[i - 1][0]],
               [cities[i][1], cities[i - 1][1]],
               'bo-')
pylab.plot([cities[0][0], cities[N - 1][0]],
           [cities[0][1], cities[N - 1][1]],
           'bo-')
pylab.title(str(best_energy))
pylab.axis('scaled')
pylab.axis([0.0, 1.0, 0.0, 1.0])
pylab.savefig('plot_tsp_simulated_annealing_N_{0}_energy_{1}.png'.format(N,best_energy))
pylab.show()