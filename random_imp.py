import algorithms
from starter import *

sizes = ['small', 'medium', 'large']

for size in sizes:
    for i in range(70, 261):
        G = read_input('./inputs/' + size + str(i) + '.in')
        try:
            curr = read_output(G, './outputs/' + size + str(i) + '.out')
            curr_score = score(curr)
        except:
            with open('./outputs/' + size + str(i) + '.out') as fp:
                l = json.load(fp)
                nx.set_node_attributes(G, {v: l[v] + 1 for v in G}, 'team')
            curr_score = score(G)

        all_randoms = algorithms.random_funcs
        best_score = float('inf')
        best_assignment = None
        for func in all_randoms:
            for _ in range(50):
                init_func = getattr(algorithms, func)
                init_func(G)
                new_score = score(G)
                if new_score < best_score:
                    best_score = new_score
                    best_func = func
                    best_assignment = [G.nodes[v]['team'] for v in range(G.number_of_nodes())]
        
        if best_score < curr_score:
            with open('./outputs/' + size + str(i) + '.out', 'w') as fp:
                json.dump(best_assignment, fp)
            print('Overwrote', size, str(i), 'with', best_func, ':', best_score)