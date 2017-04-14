m = 134456
n = 8121
k = 28411
idum = 1000
for iteration in xrange(200000):
    idum = (idum *  n + k) % m
    ran = idum / float(m)
    print idum, ran, iteration
