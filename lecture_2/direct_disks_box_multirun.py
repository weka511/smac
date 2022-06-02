'''Direct sampling of disks in box, tabula rasa, multiple runs'''

from direct_disks_box import direct_disks_box

N = 4
n_runs = 100
for run in range(n_runs):
    print (run, direct_disks_box(N))
