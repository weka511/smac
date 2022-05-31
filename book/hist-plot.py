from matplotlib.pyplot import hist, show

Xs = []
burn = 10000
for line in open('md/history.csv'):
    if burn==0:
        fields = line.strip().split(',')
        Xs.append(float(fields[0]))
    else:
        burn-=1
hist(Xs,bins=100)
show()
