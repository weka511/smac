def gray_flip(t, N):
    k = t[0]
    if k > N: return t, k
    t[k - 1] = t[k]
    t[k] = k + 1
    if k != 1: t[0] = 1
    return t, k

L = 4
N = L * L 
# Neighbours, assuming table wrapped
#  0  1  2  3
#  4  5  6  7
#  8  9 10 11
# 12 13 14 15
# e.g. nbr[0] = (1, 4, 3, 12) - this doesn'mt match 5-2 in textbook

nbr = {i : ((i // L) * L + (i + 1) % L, (i + L) % N,
            (i // L) * L + (i - 1) % L, (i - L) % N)
                                    for i in range(N)}
S = [-1] * N
E = -2 * N
print (S, E)
tau = list(range(1, N + 2))
for i in range(1, 2 ** N):
    tau, k = gray_flip(tau, N)
    h = sum(S[n] for n in nbr[k - 1])
    E += 2 * h * S[k - 1] 
    S[k - 1] *= -1
    print (S, E)
