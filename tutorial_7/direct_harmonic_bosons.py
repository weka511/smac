import math, random

def z(k, beta):
    return (1.0 - math.exp(- k * beta)) ** (-3)

def canonic_recursion(N, beta):
    Z = [1.0]
    for M in range(1, N + 1):
        Z.append(sum(Z[k] * z(M - k, beta) \
                     for k in range(M)) / M)
    return Z

def make_pi_list(Z, M):
   pi_list = [0.0] + [z(k, beta) * Z[M - k] / Z[M] / M \
                              for k  in range(1, M + 1)]
   pi_cumulative = [0.0]
   for k in range(1, M + 1):
      pi_cumulative.append(pi_cumulative[k - 1] + pi_list[k])
   return pi_cumulative

def naive_tower_sample(pi_cumulative):
    eta = random.uniform(0.0, 1.0)
    for k in range(len(pi_cumulative)):
        if eta < pi_cumulative[k]: break
    return k

def levy_harmonic_path(dtau, N): 
   beta = N * dtau
   x_N = random.gauss(0.0, 1.0 / math.sqrt(2.0 * math.tanh(beta / 2.0)))
   x = [x_N]
   for k in range(1, N):
      dtau_prime = (N - k) * dtau
      Upsilon_1 = 1.0 / math.tanh(dtau) + \
                  1.0 / math.tanh(dtau_prime)
      Upsilon_2 = x[k - 1] / math.sinh(dtau) + \
                  x_N / math.sinh(dtau_prime)
      x_mean = Upsilon_2 / Upsilon_1
      sigma = 1.0 / math.sqrt(Upsilon_1)
      x.append(random.gauss(x_mean, sigma))
   return x

### main program starts here ###
N = 8
T_star = 0.1
beta = 1.0 / N ** (1.0 / 3.0) / T_star
n_steps = 1000
Z = canonic_recursion(N, beta)
for step in range(n_steps):
    N_tmp = N
    x_config = []
    y_config = []
    z_config = []
    while N_tmp > 0:
       pi_sum = make_pi_list(Z, N_tmp)
       k = naive_tower_sample(pi_sum)
       x_config += levy_harmonic_path(beta, k)
       y_config += levy_harmonic_path(beta, k)
       z_config += levy_harmonic_path(beta, k)
       N_tmp -= k
