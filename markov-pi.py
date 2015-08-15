# markov-pi.py

# Copyright (C) 2015 Greenweaves Software Pty Ltd

# This is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with GNU Emacs.  If not, see <http://www.gnu.org/licenses/>.

# Problem 1.2 from Werner Krauth, Statistical Mechanics, Algorithms & Computations

import random, math, matplotlib.pyplot as plt

def float_range(lower,upper,step):
    return [step*i for i in range(lower,upper+1)]

# Calculate normalized errors, uisng the maximum as our normalization.
# Normalized errors range from 0 to 1
def normalize(xs):
    m=max(xs)
    return [x/m for x in xs]

def perform_markov(n_trials,delta):
    x, y = 1.0, 1.0
    n_hits=0
    n_reject=0
    
    for i in range(n_trials):
        del_x, del_y = random.uniform(-delta, delta), random.uniform(-delta, delta)
        if abs(x + del_x) < 1.0 and abs(y + del_y) < 1.0:
            x, y = x + del_x, y + del_y
        else:
            n_reject+=1
        if x*x + y*y < 1.0: n_hits += 1
    
    return (4.0 * n_hits / float(n_trials), n_reject/ float(n_trials))

if __name__=='__main__':
    n=25
    errors=[]
    deltas=float_range(1,30,0.1)
    rejections=[]
    n_trials=400000
    for delta in deltas:
        sum_sq=0
        sum_reject=0
        for i in range(n):
            (result,reject)=perform_markov(n_trials,delta)
            error=result-math.pi
            sum_sq+=error*error
            sum_reject+=reject
        mean_sq=sum_sq/n
        mean_reject=sum_reject/n
        errors.append(mean_sq)
        rejections.append(mean_reject)
     
    plt.figure(1) 
    plt.subplot(211)
    plt.plot(deltas, normalize(errors), 'o', label='Errors')
    plt.plot(deltas, rejections,'+', label='Rejections')
    plt.xlabel('Delta')
    plt.ylabel('Error')
    plt.title('Error and rejection rate vs step size')
    legend = plt.legend(loc='upper center', shadow=True, fontsize='x-large')
    legend.get_frame().set_facecolor('#00FFCC')    

    plt.subplot(212)
    plt.plot(rejections[1:], errors[1:],'x')
    plt.xlabel('Rejection')
    plt.ylabel('Error')
    plt.title('Error vs rejection rate')
    plt.savefig('markov-pi.png')
    
    plt.show()