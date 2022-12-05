from starter import *
import algorithms as alg
import WGraph
from swaps import *
import warnings

warnings.filterwarnings("ignore")

# for every input
# Call every algorithm on G

for size in ['large']:
    for i in range(229, 261):
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
                best_assignment = [G.nodes[v]['team'] for v in range(G.number_of_nodes())]
        print(size + str(i), best_score, best_func)
        with open('./outputs/' + size + str(i) + '.out', 'w') as fp:
            json.dump(best_assignment, fp)
