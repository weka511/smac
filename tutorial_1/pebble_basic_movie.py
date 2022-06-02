'''Move pebble using neighbour table from Table 1.3'''
from random            import randint
from matplotlib.pyplot import axis, Circle, clf, gca, plot, savefig, title,  xticks, yticks

sigma    = 0.4  # sigma and s_map are needed for the graphical output
s_map    = [(1.0, 1.0), (2.0, 1.0), (3.0, 1.0),
            (1.0, 2.0), (2.0, 2.0), (3.0, 2.0),
            (1.0, 3.0), (2.0, 3.0), (3.0, 3.0)]
neighbor =  [[1, 3, 0, 0], [2, 4, 0, 1], [2, 5, 1, 2],
             [4, 6, 3, 0], [5, 7, 3, 1], [5, 8, 4, 2],
             [7, 6, 6, 3], [8, 7, 6, 4], [8, 8, 7, 5]]
site     = 8
N_runs   = 10

for run in range(N_runs):
    gca().add_patch(Circle(s_map[site], radius=sigma, fc='r'))
    plot([0.5, 3.5], [1.5, 1.5], 'b')
    plot([0.5, 3.5], [2.5, 2.5], 'b')
    plot([1.5, 1.5], [0.5, 3.5], 'b')
    plot([2.5, 2.5], [0.5, 3.5], 'b')
    title(f't={run:02d}')
    axis('scaled')
    axis([0.5, 3.5, 0.5, 3.5])
    xticks([])
    yticks([])
    savefig(f'pebble_basic_movie_{run:02d}.png', transparent=False)
    clf()
    site = neighbor[site][randint(0, 3)]
