'''Model Monte Carlo simulation as a transfer matrix; subtract equilibrium value to show speed of convergence'''

from matplotlib.pyplot import legend, plot, show
from numpy             import dot, log10, zeros
from scipy.stats       import linregress

neighbor =  [[1, 3, 0, 0], [2, 4, 0, 1], [2, 5, 1, 2],
             [4, 6, 3, 0], [5, 7, 3, 1], [5, 8, 4, 2],
             [7, 6, 6, 3], [8, 7, 6, 4], [8, 8, 7, 5]]

transfer = zeros((9, 9))
ys       = []

for k in range(9):
    for neigh in range(4): transfer[neighbor[k][neigh], k] += 0.25
position    = zeros(9)
position[8] = 1.0
for t in range(100):
    ys.append(log10(max(position-1/9)))
    deviations = ', '.join(f'{v-1/9:.5f}' for v in position)
    print (f'{t:2d}: {deviations}')
    position = dot(transfer, position)

slope, intercept, r, p, se = linregress(range(len(ys[2:])), ys[2:])

plot(ys, label='Monte Carlo')
plot([intercept + slope * (t-2) for t in range(len(ys))], label=f'Slope = {slope:.5f} ({log10(3/4):.5f})' )
legend()
show()
