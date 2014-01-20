from random import uniform

def direct_pi(N):
    n_hits = 0
    for i in range(N):
        x, y = uniform(-1.0, 1.0), uniform(-1.0, 1.0)
        if x ** 2 + y ** 2 <= 1.0:
            n_hits += 1
    return n_hits

n_trials = 10000
for attempt in range(10):
    print attempt, 4 * direct_pi(n_trials)/float(n_trials)
