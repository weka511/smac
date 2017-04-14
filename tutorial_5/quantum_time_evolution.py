import numpy, pylab, os

def fourier_x_to_p(phi_x, dx):
    phi_p = [(phi_x * numpy.exp(-1j * p * grid_x)).sum() * dx for p in grid_p]
    return numpy.array(phi_p)

def fourier_p_to_x(phi_p, dp):
    phi_x = [(phi_p * numpy.exp(1j * x * grid_p)).sum() for x in grid_x]
    return numpy.array(phi_x) /  (2.0 * numpy.pi)

def time_step_evolution(psi0, potential, grid_x, grid_p, dx, dp, delta_t):
    psi0 = numpy.exp(-1j * potential * delta_t / 2.0) * psi0
    psi0 = fourier_x_to_p(psi0, dx)
    psi0 = numpy.exp(-1j * grid_p ** 2 * delta_t / 2.0) * psi0
    psi0 = fourier_p_to_x(psi0, dp)
    psi0 = numpy.exp(-1j * potential * delta_t / 2.0) * psi0
    psi0 /= (numpy.absolute(psi0 ** 2).sum() * dx)
    return psi0

def funct_potential(x):
    if x < -8.0:    return (x + 8.0) ** 2
    elif x <= -1.0: return 0.0
    elif x < 1.0:   return numpy.exp(-1.0 / (1.0 - x ** 2)) / numpy.exp(-1.0)
    else:           return 0.0

output_dir = 'snapshots_time_evolution'
if not os.path.exists(output_dir): os.makedirs(output_dir)
def show(x, psi, pot, time, timestep):
    pylab.plot(x, psi, 'g', linewidth = 2.0, label = '$|\psi(x)|^2$')
    pylab.xlim(-10, 15)
    pylab.ylim(-0.1, 1.15)
    pylab.plot(x, pot, 'k', linewidth = 2.0, label = '$V(x)$')
    pylab.xlabel('$x$', fontsize = 20)
    pylab.title('time = %s' % time)
    pylab.legend(loc=1)
    pylab.savefig(output_dir + '/snapshot_%05i.png' % timestep)
    timestep += 1
    pylab.clf()

steps = 800
x_min = -12.0
x_max = 40.0
grid_x = numpy.linspace(x_min, x_max, steps)
grid_p = numpy.linspace(x_min, x_max, steps)
dx  = grid_x[1] - grid_x[0]
dp  = grid_p[1] - grid_p[0]
delta_t = 0.05
t_max = 16.0

potential = [funct_potential(x) for x in grid_x]
potential = numpy.array(potential)
# initial state:
x0 = -8.0
sigma = .5
psi = numpy.exp(-(grid_x - x0) ** 2 / (2.0 * sigma ** 2) )
psi /= numpy.sqrt( sigma * numpy.sqrt( numpy.pi ) )
# time evolution
time = 0.0
timestep = 0
while time < t_max:
    if timestep % 4 == 0:
        show(grid_x, numpy.absolute(psi) ** 2.0, potential, time, timestep)
    print (time)
    time += delta_t
    timestep += 1
    psi = time_step_evolution(psi, potential, grid_x, grid_p, dx, dp, delta_t)
