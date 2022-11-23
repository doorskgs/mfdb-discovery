import math

import numpy as np
import eme

N = 3
D = 2

results: dict[tuple[int, int], float] = {}

def truncate(f, n):
    return str(math.floor(f * 10 ** n) / 10 ** n)


for N in range(1, 4):
    for D in range(1, 6):
        n1 = math.pow(10, N) + 0.1
        n2 = math.pow(10, N+1)-1 - 0.1

        min_eps = 0.0000001
        for eps in np.arange(0.01, min_eps, -min_eps):
            if truncate(n1-eps*n1, D) == truncate(n1+eps*n1, D) == truncate(n1,D):
                print(f'for N={N}, D={D}: eps={eps}    (N+D = {N+D})')
                results[N, D] = eps
                break

print(results)
