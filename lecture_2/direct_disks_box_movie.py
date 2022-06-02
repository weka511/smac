'''
Direct sampling of disks in box, tabula rasa, plotted as movie
'''

from os.path           import exists, join
from os                import makedirs
from matplotlib.pyplot import subplots_adjust, gca, Circle,gcf, axis, setp, savefig, close
from direct_disks_box  import direct_disks_box


def snapshot(pos, colors, img,
             output_dir = 'direct_disks_box_movie'):
    subplots_adjust(left=0.10, right=0.90, top=0.90, bottom=0.10)
    gcf().set_size_inches(6, 6)
    axis([0, 1, 0, 1])
    setp(gca(), xticks=[0, 1], yticks=[0, 1])
    for (x, y), c in zip(pos, colors):
        gca().add_patch(Circle((x, y), radius=sigma, fc=c))
    savefig(join(output_dir, '%d.png' % img), transparent=True)
    close()

if __name__=='__main__':
    N          = 4
    colors     = ['xkcd:red', 'xkcd:blue', 'xkcd:green', 'xkcd:orange']
    sigma      = 0.2
    n_runs     = 8
    output_dir = 'direct_disks_box_movie'

    if not exists(output_dir): makedirs(output_dir)

    for img in range(n_runs):
        snapshot(direct_disks_box(N, sigma), colors, img,
                 output_dir = output_dir)
