'''Show probability for reaching other cells after 0, 1, 2, ... moves'''
from random            import randint
from numpy             import histogram2d, sum
from matplotlib.pyplot import close, colorbar, imshow, savefig, title, xticks, yticks

xvec     = {1:3, 2:2, 3:1, 4:3, 5:2, 6:1, 7:3, 8:2, 9:1}
yvec     = {1:1, 2:1, 3:1, 4:2, 5:2, 6:2, 7:3, 8:3, 9:3}

neighbor = {1 : [2, 4, 1, 1], 2 : [3, 5, 1, 2], 3 : [3, 6, 2, 3],
            4 : [5, 7, 4, 1], 5 : [6, 8, 4, 2], 6 : [6, 9, 5, 3],
            7 : [8, 7, 7, 4], 8 : [9, 8, 7, 5], 9 : [9, 9, 8, 6]}

N_runs   = 10
for run in range(N_runs):
    list_vec = []

    for n_runs in range(100000):
        pos = 9
        for iter in range(run):
            pos = neighbor[pos][ randint(0, 3)]
        list_vec.append(pos)

    x = [xvec[k] for k in list_vec]
    y = [yvec[k] for k in list_vec]

    xticks([])
    yticks([])
    H, xedges, yedges = histogram2d(x, y,
                                    bins   = (3, 3),
                                    range  = [[1,3],[1,3]],
                                    normed = True)
    print (H)
    H /= sum(H)
    print (H)
    extent = [yedges[0], yedges[-1], xedges[-1], xedges[0]]
    histo  = imshow(H,
                    extent        = extent,
                    interpolation = 'nearest',
                    vmin          = 0,
                    vmax          = 1.00)
    histo.set_cmap('hot')
    colorbar()
    title(f't = {run}', fontsize=22)
    savefig(f'3x3_pebble_run_{run:02d}.png')
    close()
