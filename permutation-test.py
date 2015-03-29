import permutation



def per_to_str(perm):
    result=""
    for el in perm:
        result+=str(el)
    return result
    
perms={}
    
for i in range(10):

    perm0=permutation.ran_perm(5)
#    print perm0
    perm = per_to_str(perm0)
#    print perm                 
    if perm in perms:
        print perm, "A"
        perms[perm]+=1
    else:
        print perm, "B"
        perms[perm]=1
    
kk=perms.keys()
print len(kk)

for kkk in kk:
    print kkk,perms[kkk]
        
