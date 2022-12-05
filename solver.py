from starter import *
import algorithms as alg
import WGraph
from swaps import *

# for every input
# Call every algorithm on G
for size in ['small', 'medium', 'large']:
    for i in range(1, 261):
        G = read_input('./inputs/' + size + str(i) + '.in')
        all_funcs = alg.functions
        best_score = float('inf')
        best_assignment = None
        best_func = ""
        for func in all_funcs:
            init_func = getattr(alg, func)
            init_func(G)
            new_score = score(G)
            if new_score < best_score:
                best_score = new_score
                best_func = func
        print(size + str(i), best_score, best_func)
"""
G = read_input('./inputs/small1.in')
alg.read_partition(G)
# Sample swap
print('before', score(G))
a = WGraph.WGraph(G)
for _ in range(1):
    swap(a, 10000)
print('after', score(a.graph))
"""
