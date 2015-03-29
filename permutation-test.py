import permutation
import math


def per_to_str(perm):
    result=""
    for el in perm:
        result+=str(el)
    return result
    
perms={}
    
for i in range(120000):
    perm0=permutation.ran_perm(5)
    perm = per_to_str(perm0)
    if perm in perms:
        perms[perm]+=1
    else:
        perms[perm]=1
    
kk=perms.keys()
kk.sort()
print len(kk)

sum=0
for kkk in kk:
    sum+=perms[kkk]

average=sum/len(kk)

var=0
for kkk in kk:
    var+=((perms[kkk]-average)*(perms[kkk]-average))


sigma=math.sqrt(var/len(kkk))

print average, sigma
