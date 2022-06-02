'''Direct sampling of disks in box, tabula rasa: investigate success rate'''

from direct_disks_box import direct_disks_box

if __name__=='__main__':
    sigma  = 0.15
    del_xy = 0.10

    for n_runs in [10000,100000,1000000]:
        conf_a         = ((0.30, 0.30), (0.30, 0.70), (0.70, 0.30), (0.70,0.70))
        conf_b         = ((0.20, 0.20), (0.20, 0.80), (0.75, 0.25), (0.75,0.75))
        conf_c         = ((0.30, 0.20), (0.30, 0.80), (0.70, 0.20), (0.70,0.70))
        configurations = [conf_a, conf_b, conf_c]
        hits           = {conf_a: 0, conf_b: 0, conf_c: 0}
        for run in range(n_runs):
            x_vec = direct_disks_box(4, sigma)
            for conf in configurations:
                condition_hit = True
                for b in conf:
                    condition_b = min(max(abs(a[0] - b[0]), abs(a[1] - b[1])) for a in x_vec) < del_xy
                    condition_hit *= condition_b
                if condition_hit:
                    hits[conf] += 1

        print (n_runs)
        for conf in configurations:
            print (conf, hits[conf])
