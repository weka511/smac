'''Direct sampling of disks in box, tabula rasa'''

from random import uniform
from math   import sqrt

def direct_disks_box(N, sigma = 0.2):
    generatedLegal = False
    while not generatedLegal:
        L = [(uniform(sigma, 1.0 - sigma), uniform(sigma, 1.0 - sigma))]
        for k in range(1, N):
            a = (uniform(sigma, 1.0 - sigma), uniform(sigma, 1.0 - sigma))
            min_dist = min(sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2) for b in L)
            if min_dist < 2.0 * sigma:
                generatedLegal = False
                break
            else:
                L.append(a)
                generatedLegal = True
    return L

print (direct_disks_box(4, sigma = 0.2))
