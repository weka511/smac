import random,operator,functools,scipy.stats

N = 5
statistics = {}
L = [l for l in range(N)]
nsteps = 10000000
k=functools.reduce(operator.mul, list(range(1,N+1)),1)
expected = nsteps/k

for step in range(nsteps):
    i = random.randint(0, N - 1)
    j = random.randint(0, N - 1)
    L[i], L[j] = L[j], L[i]
    if tuple(L) in statistics: 
        statistics[tuple(L)] += 1
    else:
        statistics[tuple(L)] = 1

for item in statistics:
    print (item, statistics[item])

f_obs = [statistics[item] for item in statistics]

s = scipy.stats.chisquare(f_obs)
print ('M={}, k={}, nsteps={}, Chi square={:.1f}, p-value={:.2g}'.format(N,k, nsteps, s.statistic, s.pvalue))
