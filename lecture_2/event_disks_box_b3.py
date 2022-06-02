'''Algorithm 2.1: event-driven molecular dynamics for hard disks in a box. Repeat and generate histogram'''

from math             import pi, sqrt
from event_disks_box  import wall_time, pair_time
from os.path          import splitext, split
from pylab            import grid, hist,  savefig, show, title, xlabel, ylabel

def figure_path(ext='png'):
    '''Extract root of file name, so we can use it as name of plot'''
    root,_ = splitext(split(__file__)[-1])
    return '{0}.{1}'.format(root,ext)


del_xy           = 0.10
pos              = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
vel              = [[0.21, 0.12], [0.71, 0.18], [-0.23, -0.79], [0.78, 0.1177]]
singles          = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)]
pairs            = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
V                = 1    # volume of space
N                = len(pos)
eta              = 0.18
sigma            = sqrt(eta*V/(pi*N))
t                = 0.0
n_events         = 5000000
reassurance_time = 100000

xs               = []   # Accumulate x coordinates here

for event in range(n_events):
    if event % reassurance_time == 0:
        print ('{0:,d} Events'.format(event))

    wall_times = [wall_time(pos[k][l], vel[k][l], sigma) for k, l  in singles]
    pair_times = [pair_time(pos[k], vel[k], pos[l], vel[l], sigma) for k, l in pairs]
    next_event = min(wall_times + pair_times)
    t_previous = t

#   sample positions if the gap between next event and its predecessor
#   is large enough (we sample at integer times)

    for inter_times in range(int(t + 1), int(t + next_event + 1)):
        del_t = inter_times - t_previous
        for k, l in singles:
            pos[k][l] += vel[k][l] * del_t
        t_previous = inter_times
        # we'll accumulate x's here, since we are in the loop that iterates
        # through regularly spaces times
        for p in pos:
            xs.append(p[0])

    t += next_event
    del_t = t - t_previous

    for k, l in singles:
        pos[k][l] += vel[k][l] * del_t
    if min(wall_times) < min(pair_times):
        collision_disk, direction = singles[wall_times.index(next_event)]
        vel[collision_disk][direction] *= -1.0
    else:
        a, b   = pairs[pair_times.index(next_event)]
        del_x  = [pos[b][0] - pos[a][0], pos[b][1] - pos[a][1]]
        abs_x  = sqrt(del_x[0] ** 2 + del_x[1] ** 2)
        e_perp = [c / abs_x for c in del_x]
        del_v  = [vel[b][0] - vel[a][0], vel[b][1] - vel[a][1]]
        scal   = del_v[0] * e_perp[0] + del_v[1] * e_perp[1]
        for k in range(2):
            vel[a][k] += e_perp[k] * scal
            vel[b][k] -= e_perp[k] * scal


hist(xs, bins=100, density=True)
xlabel('x')
ylabel('frequency')
title(f'Event Disks: x coordinate histogram (density eta={eta:3f})\nProduced by {split(__file__)[-1]}')
grid()
savefig(figure_path())
show()
