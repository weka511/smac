'''Generate histogram of x positions by direct sampling of disks in box, tabula rasa'''

from direct_disks_box import direct_disks_box
from math             import pi
from os.path          import splitext, split
from pylab            import grid, hist,  savefig, show, title, xlabel, ylabel

def figure_path(ext='png'):
    root,_ = splitext(split(__file__)[-1])
    return '{0}.{1}'.format(root,ext)


if __name__=='__main__':
    N          = 4
    sigma      = 0.1197
    n_runs     = 1000000
    histo_data = []
    V          = 1
    eta        = sigma**2 *pi * N/V # Krauth, Section 2.2.2

    for run in range(n_runs):
        pos = direct_disks_box(N, sigma=sigma)
        for k in range(N):
            histo_data.append(pos[k][0])

    hist(histo_data, bins=100, density=True)
    xlabel('x')
    ylabel('frequency')
    title(f'Direct sampling: x coordinate histogram (density eta={eta:3f})\nProduced by {split(__file__)[-1]}')
    grid()
    savefig(figure_path())
    show()
