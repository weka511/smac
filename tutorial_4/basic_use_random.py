import random

print 'random seed'
random.seed('MOOC-SMAC')
for i in range(4):
    print random.uniform(0.0, 1.0)
print
random.seed('MOOC-SMAC')
for i in range(4):
    print random.uniform(0.0, 10.0)
print
print 'random integers'
random.seed(12315)
for i in range(10):
    print random.randint(0, 4)
print 'random permuation of elements that are not all numbers'
L = [1, 2, 'MOOC-SMAC', [1.1, 2.1]]
for i in range(10): 
    random.shuffle(L)
    print L 
    print random.choice(L)
print 'read the documentation of the module "random" in Python'
