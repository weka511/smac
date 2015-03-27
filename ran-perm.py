import random

def ran_perm(K):
    perm = range(K)
    for k in range(K):
        l=random.randint(k,K-1)
        perm[k],perm[l]=perm[l],perm[k]
    return perm

def ran_combination(K,M):
    perm = range(K)
    for k in range(M):
        l=random.randint(k,K-1)
        perm[k],perm[l]=perm[l],perm[k]
    return perm[0:2]    
    
for i in range(100):
    print ran_combination(4,2)
