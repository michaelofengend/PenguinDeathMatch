from starter import *
#import algorithms as alg
import WGraph
from swaps import *
import warnings
import multiprocessing as mp

warnings.filterwarnings("ignore")

# for every input
# Call every algorithm on G

def runSwaps(i):
        size = 'large' # Change to small and medium when needed
        G = read_input('./inputs/' + size + str(i) + '.in')
        G = read_output(G, './outputs/' + size + str(i) + '.out')
        best = WGraph.WGraph(G)
        orig_cost = best.cost
        best = swap(best, 20, 15)
        if orig_cost > best.cost:
            print(size + str(i), best.cost, orig_cost)
            write_output(best.graph, './outputs/' + size + str(i) + '.out', True)

if __name__ == '__main__':
    pool = mp.Pool(mp.cpu_count() - 2)
    pool = mp.Pool()
    res = pool.map(runSwaps, [i for i in range(1, 261)])
    pool.close()
    pool.join()