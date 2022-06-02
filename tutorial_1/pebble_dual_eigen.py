'''Two games: Illustrate conversion of reducible matrix to irreducible, aperiodoc to make motion ergodic'''
from numpy        import zeros
from numpy.linalg import eig
neighbor =  [[1, 3, 0, 0], [2, 4, 0, 1], [2, 5, 1, 2],
             [4, 6, 3, 0], [5, 7, 3, 1], [5, 8, 4, 2],
             [7, 6, 6, 3], [8, 7, 6, 4], [8, 8, 7, 5]]
transfer = zeros((18, 18))
for k in range(9):
    for neigh in range(4):
        transfer[neighbor[k][neigh], k] += 0.25     # red pebble game
        transfer[neighbor[k][neigh]+9, k+9] += 0.25 # blue pebble game
# small transition epsilon between red 2 and blue 6
epsilon            = 0.04
transfer[6+9,2]    = transfer[2,6+9] = epsilon
transfer[2,2]     -= epsilon
transfer[6+9,6+9] -= epsilon
eigenvalues, eigenvectors = eig(transfer)
print (eigenvalues)


for iter in range(18):
    print (eigenvalues[iter])
    for i in range(18):
        print (eigenvectors[i][iter])
