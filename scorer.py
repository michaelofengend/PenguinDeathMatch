from starter import *
import networkx as nx
from networkx.algorithms import bipartite
import random

"""
IGNORE THIS FILE
Jacob's file to check scores returned by some algorithms.
"""
"""
best = float('inf')
G = read_input('./inputs/small5.in')
for i in range(2, 27):
    read_partition(G, './sample_partition_2/small5_part' + str(i) + '.in')
    curr_score = score(G)
    best = min(curr_score, best)
print(best)
"""
"""
count = 0
for size in ['small', 'medium', 'large']:
    for i in range(1, 261):
        G = read_input('./inputs/' + size + str(i) + '.in')
        if nx.is_bipartite(G):
            print(size, i, ' is bipartite')
            count += 1

print(count, ' large graphs are bipartite')

def sets(G):
    c = bipartite.color(G)
    X = {n for n, is_top in c.items() if is_top}
    Y = {n for n, is_top in c.items() if not is_top}
    return (X, Y)

G = read_input('./inputs/small206.in')
a, b = sets(G)
print(len(a))
print(len(b))

for n in a:
    G.nodes[n]['team'] = 1
for n in b:
    G.nodes[n]['team'] = 2
print(score(G))

fn_l = "./inputs/large1.in"
G_l = read_input(fn_l)
G = nx.complete_graph(1000)
nx.set_edge_attributes(G, 0, 'weight')
labels = nx.get_edge_attributes(G_l, 'weight')
nx.set_edge_attributes(G, labels, 'weight')
nx.write_graphml(G, "./GMLinputComplete/large1.graphml")


fin = open("./GMLinputComplete/large1.graphml", "rt")
data = fin.read()
data = data.replace('<data key="d0">', '<data key="d1">A</data><data key="d0">')
fin.close()

import k_partition
for k in range (2, 30): # FROM k = 2 to 29
    k_partition.main('large', 1, k)
"""

import networkx.utils.heaps
print(networkx.utils.heaps.__file__)