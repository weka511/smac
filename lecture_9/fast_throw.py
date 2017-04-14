import random, math

log_lambda = math.log(5.0 / 6.0)
t_max = 10000
t = 0
while t < t_max:
    Upsilon = random.uniform(0.0, 1.0)
    delta_t = 1 + int(math.log(Upsilon) /
              log_lambda)
    t += delta_t
    print t, 'flip'