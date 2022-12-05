import algorithms
from starter import *
import multiprocessing as mp

sizes = ['small', 'medium', 'large']

def runIMP(i):
        size = 'medium'
        G = read_input('./inputs/' + size + str(i) + '.in')
        curr = read_output(G, './outputs/' + size + str(i) + '.out')
        curr_score = score(curr)

        all_randoms = algorithms.random_funcs
        best_score = float('inf')
        best_assignment = None
        for func in all_randoms:
            for _ in range(100):
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
            print('Overwrote', size, str(i), 'with', best_func, ':', best_score, 'Original:', curr_score)

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count() - 2)
    pool = mp.Pool()
    res = pool.map(runIMP, [i for i in range(1, 261)])
    pool.close()
    pool.join()