'''Model Monte Carlo simulation as a transfer matrix, but subtract equilibrium value'''
from numpy import dot, zeros

def get_deviation(v):
    return f'{v-1/9:.5f}'

neighbor =  [[1, 3, 0, 0], [2, 4, 0, 1], [2, 5, 1, 2],
             [4, 6, 3, 0], [5, 7, 3, 1], [5, 8, 4, 2],
             [7, 6, 6, 3], [8, 7, 6, 4], [8, 8, 7, 5]]

transfer = zeros((9, 9))
for k in range(9):
    for neigh in range(4): transfer[neighbor[k][neigh], k] += 0.25
position = zeros(9)
position[8] = 1.0
for t in range(100):
    deviations = ', '.join(f'{v-1/9:.5f}' for v in position)
    print (f'{t:2d}: {deviations}')
    position = dot(transfer, position)
