import math

def z(k, beta):
    return 1.0 / (1.0 - math.exp(- k * beta)) ** 3

def canonic_recursion(N, beta):
    Z = [1.0]
    for M in range(1, N + 1):
        Z.append(sum(Z[k] * z(M - k, beta) \
                     for k in range(M)) / M)
    return Z

N = 1000
beta = 1.0
Z = canonic_recursion(N, beta)
print N, Z[-1]
