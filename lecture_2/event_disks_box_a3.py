'''Algorithm 2.1: event-driven molecular dynamics for hard disks in a box'''

from math import sqrt
from event_disks_box import wall_time, pair_time

conf_a           = ((0.30, 0.30), (0.30, 0.70), (0.70, 0.30), (0.70,0.70))
conf_b           = ((0.20, 0.20), (0.20, 0.80), (0.75, 0.25), (0.75,0.75))
conf_c           = ((0.30, 0.20), (0.30, 0.80), (0.70, 0.20), (0.70,0.70))
configurations   = [conf_a, conf_b, conf_c]
hits             = {conf_a: 0, conf_b: 0, conf_c: 0}
del_xy           = 0.10
pos              = [[0.25, 0.25], [0.75, 0.25], [0.25, 0.75], [0.75, 0.75]]
vel              = [[0.21, 0.12], [0.71, 0.18], [-0.23, -0.79], [0.78, 0.1177]]
singles          = [(0, 0), (0, 1), (1, 0), (1, 1), (2, 0), (2, 1), (3, 0), (3, 1)]
pairs            = [(0, 1), (0, 2), (0, 3), (1, 2), (1, 3), (2, 3)]
sigma            = 0.10
t                = 0.0
n_events         = 5000000
reassurance_time = 100000      # Frequency of letting user know what is happening

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
        for conf in configurations:
            condition_hit = True
            for b in conf:
                condition_b = min(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a in pos) < del_xy
                condition_hit *= condition_b
            if condition_hit:
                hits[conf] += 1
    t += next_event
    del_t = t - t_previous

    for k, l in singles:
        pos[k][l] += vel[k][l] * del_t

    if min(wall_times) < min(pair_times):
        collision_disk, direction = singles[wall_times.index(next_event)]
        vel[collision_disk][direction] *= -1.0
    else:
        a, b = pairs[pair_times.index(next_event)]
        del_x = [pos[b][0] - pos[a][0], pos[b][1] - pos[a][1]]
        abs_x = sqrt(del_x[0] ** 2 + del_x[1] ** 2)
        e_perp = [c / abs_x for c in del_x]
        del_v = [vel[b][0] - vel[a][0], vel[b][1] - vel[a][1]]
        scal = del_v[0] * e_perp[0] + del_v[1] * e_perp[1]
        for k in range(2):
            vel[a][k] += e_perp[k] * scal
            vel[b][k] -= e_perp[k] * scal

print ('Elapsed time = {0:12.3f}'.format(t))
print('Variability for {0:,d} events is {1:5.3f}'.format(     \
    n_events,                                        \
    (max(hits[conf] for conf in configurations) -    \
     min(hits[conf] for conf in configurations)) /   \
    sum(hits[conf] for conf in configurations)))

for conf in configurations:
    print(conf,hits[conf])
