'''Model Monte Carlo simulation as a transfer matrix, illustrating speed of convergence'''
from numpy import dot, zeros

neighbor =  [[1, 3, 0, 0], [2, 4, 0, 1], [2, 5, 1, 2],
             [4, 6, 3, 0], [5, 7, 3, 1], [5, 8, 4, 2],
             [7, 6, 6, 3], [8, 7, 6, 4], [8, 8, 7, 5]]
transfer = zeros((9, 9))
for k in range(9):
    for neigh in range(4): transfer[neighbor[k][neigh], k] += 0.25
position    = zeros(9)
position[8] = 1.0
for t in range(100):
    print (t,'  ',["%0.5f" % i for i in position])
    position = dot(transfer, position)
