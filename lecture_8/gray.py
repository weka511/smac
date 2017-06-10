# Recursive algorithm for k-bit Gray code, from
# http://cacs.usc.edu/education/phys516/01-4AdvancedMC.pdf
def gray(N):
    k = 1
    g=[[0],[1]]
    while k < N:
        g = [[0] + gg for gg in g] + [[1] + gg for gg in g[::-1]]
        k+= 1
    return g

for gg in gray(4):
    print (gg)
