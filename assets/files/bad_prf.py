import numpy as np
import matplotlib.pyplot as plt
import random
from collections import Counter
import matplotlib.pyplot as plt
import os

GENERATE_NEW = not os.path.exists('data.npy')

P = 4294967087

def rand():
    return random.randint(1, P - 2)

gen = 2

def beta(x):
    return x > P//2

def bad_prf(k, x):
    y = k ^ x
    return pow(gen, y, P) << 1 | beta(y)

LIMIT = 1e6

MAX_EXP = 24

def run_attack():
    # The true key.
    k = rand()
    F0 = bad_prf(k, 0)

    c = Counter()
    t = Counter()

    zR = F0 & 1
    zL = F0 >> 1

    next_print = 1

    for j in range(int(LIMIT)):
        # A random x to look at
        x = random.randint(1, 2 ** MAX_EXP)
        # The rand() below is a random key. `guess` is our guess for k & x 
        guess = rand() & x

        newL = (zL * pow(gen, x - 2 * guess, P)) % P
        newR = zR ^ beta(x)
        
        guess = (newL << 1 | newR)

        ####
        ## secret section
        true_value = bad_prf(k, x)
        is_correct = true_value == guess
        #####

        hw = x.bit_count()

        c[hw] += is_correct
        t[hw] += 1

        if j > next_print:
            print(j)
            next_print *= 1.2 + 1

    ratios = [0] * P.bit_length()

    for i in c.keys():
        ratios[i] = c[i] / t[i]

    print(ratios)

    np.save('data', ratios)

if GENERATE_NEW:
    run_attack()

data = np.load('data.npy')

h = np.arange(np.max(np.where(data)) + 2)

plt.plot(np.log10(data), '.-', label="Simulation")
plt.plot(h, -h * np.log10(2), '--', label="Theoretical")
plt.ylabel("log Pr")
plt.xlabel("hamming weight of guess")
plt.legend()
plt.title("$G(k\oplus x)$ PRF attack")

plt.show()