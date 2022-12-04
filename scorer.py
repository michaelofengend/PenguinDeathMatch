from starter import *
import networkx as nx
from networkx.algorithms import approximation
import algorithms

"""
IGNORE THIS FILE
Jacob's file to check scores returned by some algorithms.
"""
"""
for i in range(1, 261):
    G = read_input('./inputs/large' + str(i) + '.in')
    n = nx.number_connected_components(G)
    print(i, "has", n, "connected components")
    cc_list = nx.connected_components(G)
    print([len(cc) for cc in cc_list])
    try:
        print(nx.find_cycle(G, orientation='ignore'))
    except:
        print("No cycle")
            
G = read_input('./inputs/large218.in')
n = nx.number_connected_components(G)
print("218 has", n, "connected components")
cc_list = nx.connected_components(G)

print([len(cc) for cc in cc_list])
try:
    print(nx.find_cycle(G, orientation='ignore'))
except:
    print("No cycle")
"""
"""
def read_partition(G):
    name = G.name
    best = None
    best_score = float('inf')
    best_k = 0
    for k in range(2, 13):
        path = "./sample_partition_2/" + name + "_part" + str(k) + ".in"
        with open(path) as fp:
            arr = json.load(fp)
        for i in range(len(arr)):
            team = arr[i]["communityId"] + 1
            G.nodes[i]['team'] = team
        if score(G) <= best_score:
            best = arr
            best_score = score(G)
            best_k = k
            
    for i in range(len(best)):
        team = best[i]["communityId"] + 1
        G.nodes[i]['team'] = team
    print(k)
    return G

def color_MST(G):
    colors = nx.coloring.greedy_color(G, strategy = 'random_sequential', interchange=True)
    for c in colors.keys():
        G.nodes[c]['team'] = colors[c]

best = float('inf')
best_G = None
for _ in range(100):
    G = read_input('./inputs/large1.in')
    color_MST(G)
    a = score(G)
    if a < best:
        best = a
        best_G = G

print(best)
print([G.nodes[i]['team'] for i in range(len(G.nodes))])
"""

G = read_input('./inputs/small1.in')
post = algorithms.runRandom(G)
print(score(post))

"""
def min_clique_cover(G):
    v_set = set()
    G_comp = nx.complement(G)
    for c in nx.find_cliques(G_comp):
        print(c)

G = read_input('./inputs/large1.in')
min_clique_cover(G)



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