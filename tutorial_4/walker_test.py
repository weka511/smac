import random, pylab
 
N = 5
pi = [[1.1 / 5.0, 0], [1.9 / 5.0, 1], [0.5 / 5.0, 2], [1.25 / 5.0, 3], [0.25 / 5.0, 4]]
x_val = [a[1] for a in pi]
y_val = [a[0] for a in pi]
pi_mean = sum(y_val) / float(N)
long_s = []
short_s = []
for p in pi:
    if p[0] > pi_mean:
        long_s.append(p)
    else:
        short_s.append(p)
table = []
for k in range(N - 1):
    e_plus = long_s.pop()
    e_minus = short_s.pop()
    table.append((e_minus[0], e_minus[1], e_plus[1]))
    e_plus[0] = e_plus[0] - (pi_mean - e_minus[0])
    if e_plus[0] < pi_mean:
        short_s.append(e_plus)
    else:
        long_s.append(e_plus)
if long_s != []: 
    table.append((long_s[0][0], long_s[0][1], long_s[0][1]))
else: 
    table.append((short_s[0][0], short_s[0][1], short_s[0][1]))
print (table)
samples = []
n_samples = 10000
for k in range(n_samples):
    Upsilon = random.uniform(0.0, pi_mean)
    i = random.randint(0, N-1)
    if Upsilon < table[i][0]:
        samples.append(table[i][1])
    else: samples.append(table[i][2])

pylab.figure()
pylab.hist(samples, bins=N, range=(-0.5, N-0.5), normed=True)
pylab.plot(x_val, y_val,'ro', ms=8)
pylab.title("Histogram using Walker's method for a discrete distribution\n\
             on $N=$"+str(N)+" choices ("+str(n_samples)+" samples)",fontsize=14)
pylab.xlabel('$k$',fontsize=20)
pylab.ylabel('$\pi(k)$',fontsize=20)
pylab.show()
