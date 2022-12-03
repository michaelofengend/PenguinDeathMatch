from starter import *
import algorithms as alg

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
        print(best_score, best_func)