import random, math
n_trials = 400000
n_hits = 0
var = 0.0
sum_Obs=0.0
sum_Obs2=0.0
for iter in range(n_trials):
    x, y = random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)
    Obs = 0.0
    if x**2 + y**2 < 1.0:
        n_hits += 1
        Obs = 4.0
    sum_Obs+=Obs
    sum_Obs2+=Obs*Obs
mean=sum_Obs/n_trials
mean2=sum_Obs2/n_trials
var=mean2-mean*mean
print ('<Obs>={0:7.5f}, <Obs^2>={1:7.5f}, <Obs^2> - <Obs>^2={2:7.3f}, sqrt( <Obs^2> - <Obs>^2)={3:7.3f}'.format(mean,mean2,var,math.sqrt(var)))