def energy(S, N, nbr):
    E = 0.0
    for k in range(N):
        E -=  S[k] * sum(S[nn] for nn in nbr[k])
    return 0.5 * E

L = 2
nbr = [[1, 2], [3, 0], [3, 0], [2, 1]]
S = [1, 1, -1, 1]
print S, energy(S, L * L, nbr)
