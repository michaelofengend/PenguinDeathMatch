from starter import *
import networkx as nx
from networkx.utils import py_random_state
import random
from heapq import heappop, heappush
from itertools import count
import time
from math import isnan
import matplotlib.pyplot as plt
import functools
import numpy
import sklearn.cluster
from sklearn.cluster import SpectralClustering
import scipy.sparse

"""
IDEA:
Large is a sparse graph (1000 nodes with 10000 edges), so we do the following
Get MAXIMAL INDEPENDENT SET (NOT maximum; ideally you would want maximum, but maximum I.S. is NP-C)
Form a team with this maximal independent set
Remove these nodes from consideration when forming the next set
Continuously perform this until we have a fixed number of teams
PSEUDOCODE:
S = {all nodes}
Repeat for i from 1 to k:
    Get maximal independent set I from S
    Form team i with nodes in I
    Remove I from S
TODO: Balance the teams
"""
def msi_approx(G):
    teams = []
    G_copy = G.copy()
    average = 0
    while G_copy.number_of_nodes() > average * 0.8:   # Continuously removes M.I.S. from the graph
        curr_msi = nx.maximal_independent_set(G_copy)
        G_copy.remove_nodes_from(curr_msi)
        teams.append(set(curr_msi))
        average = sum(len(t) for t in teams) / len(teams)
    s = G_copy.nodes()
    G.remove_nodes_from(s)
    i = 0
    for team in teams:
        for n in team:
            G.nodes[n]['team'] = i
        i += 1
    # TODO: BALANCE THE TEAMS BY MOVING/SWAPPING
    return

"""
Incomplete greedy solution
"""
# INCOMPLETE
def greedy(G):
    n = G.number.of.nodes()
    G_copy = nx.complete_graph(n)
    edges = G.edges(data=True)
    edges.sort(lambda x: x['weight'])
    team_size = n / k
    remainder = n - team_size
    while nx.number_connected_components(G) > k:
        longest_edge = edges.pop()
        G.remove_edge(longest_edge)

"""
Solution for planar graphs
If bipartitite, use special solution
Description:
    Mutates G such that its nodes have field 'team' according to their coloring
NOTE: THE TEAMS ARE NOT NECESSARILY BALANCED
"""
def planar_solution(G):
    if not nx.is_planar(G):
        raise Exception("G is not planar")
    if nx.is_bipartite(G):
        def sets(G):
            c = nx.bipartite.color(G)
            X = {n for n, is_top in c.items() if is_top}
            Y = {n for n, is_top in c.items() if not is_top}
            return (X, Y) # Returns bi-partition of the graph
        a, b = sets(G)
        for n in a:
            G.nodes[n]['team'] = 1
        for n in b:
            G.nodes[n]['team'] = 2
        return G
    else:
        colors = nx.equitable_color(G, 4)
        for c in colors.keys():
            G.nodes[c]['team'] = colors[c]

"""
Coloring solution:
SPECIALIZED FOR SPARSE GRAPHS
Find a maximum spanning tree of the graph.
2-Color each Mst and add them to existing teams in a balanced way.
"""
def sets(G):
        c = nx.bipartite.color(G)
        X = {n for n, is_top in c.items() if is_top}
        Y = {n for n, is_top in c.items() if not is_top}
        return (X, Y) # Returns bi-partition of the graph

def two_coloring_solution(G):
    max_st = nx.maximum_spanning_tree(G)
    cc_list = nx.connected_components(max_st) # Connected components in G and MST are the same
    t1_total = 0
    t2_total = 0
    for component in cc_list:
        cc_graph = max_st.subgraph(list(component))
        left, right = sets(cc_graph)
        # Spaghetti code start: keep the teams balanced
        if t1_total <= t2_total:
            if len(left) >= len(right):
                for a in left:
                    G.nodes[a]['team'] = 1
                    t1_total += 1
                for b in right:
                    G.nodes[b]['team'] = 2
                    t2_total += 1
            else:
                for a in left:
                    G.nodes[a]['team'] = 2
                    t2_total += 1
                for b in right:
                    G.nodes[b]['team'] = 1
                    t1_total += 1
        elif t1_total > t2_total:
            if len(left) < len(right):
                for a in left:
                    G.nodes[a]['team'] = 1
                    t1_total += 1
                for b in right:
                    G.nodes[b]['team'] = 2
                    t2_total += 1
            else:
                for a in left:
                    G.nodes[a]['team'] = 2
                    t2_total += 1
                for b in right:
                    G.nodes[b]['team'] = 1
                    t1_total += 1

"""
General coloring solution
"""
def color_MST(G):
    max_st = nx.maximum_spanning_tree(G, algorithm='prim')
    highest_degree = (max(max_st.degree(), key = lambda x:x[1]))[1]
    colors = nx.coloring.equitable_color(max_st, highest_degree + 1)
    for c in colors.keys():
        G.nodes[c]['team'] = colors[c]


def read_partition(G):
    name = G.name
    best = None
    best_score = float('inf')
    for k in range(2, 27):
        path = "./sample_partition_2/" + name + "_part" + str(k) + ".in"
        with open(path) as fp:
            arr = json.load(fp)
        size = arr[-1]["nodeId"] - arr[0]["nodeId"]
        if size != 99 and size != 299 and size != 999:
            print(path + "IS BADLY FORMED")
        for i in range(len(arr)):
            team = arr[i]["communityId"] + 1
            G.nodes[i]['team'] = team
        if score(G) < best_score:
            best = arr
            best_score = score(G)
    for i in range(len(best)):
        team = best[i]["communityId"] + 1
        G.nodes[i]['team'] = team
    return G

def simm_anneal(G, k):
    t = 2
    while t <= k:
        #split teams in half simply based on lowest cost
        t*=2

def swap_heuristic(G):
    return 0

def preprocessforMST(G):
    for u in G.nodes:
        for v in G.nodes:
            if u != v:
                G.add_edge(u,v)

def MST(G):
    preprocessforMST(G)
    return nx.minimum_spanning_tree(G)

def prim_mst_edges(G, k, minimum, weight="weight", keys=True, data=True, ignore_nan=False):
    """Iterate over edges of Prim's algorithm min/max spanning tree.

    Parameters
    ----------
    G : NetworkX Graph
        The graph holding the tree of interest.

    minimum : bool (default: True)
        Find the minimum (True) or maximum (False) spanning tree.

    weight : string (default: 'weight')
        The name of the edge attribute holding the edge weights.

    keys : bool (default: True)
        If `G` is a multigraph, `keys` controls whether edge keys ar yielded.
        Otherwise `keys` is ignored.

    data : bool (default: True)
        Flag for whether to yield edge attribute dicts.
        If True, yield edges `(u, v, d)`, where `d` is the attribute dict.
        If False, yield edges `(u, v)`.

    ignore_nan : bool (default: False)
        If a NaN is found as an edge weight normally an exception is raised.
        If `ignore_nan is True` then that edge is ignored instead.

    """
    push = heappush
    pop = heappop

    nodes = set(G)
    c = count()

    sign = 1 if minimum else -1
    it = 0
    while nodes:
        u = nodes.pop()
        frontier = []
        visited = {u}
        for v, d in G.adj[u].items():
            wt = d.get(weight, 1) * sign
            push(frontier, (wt, next(c), u, v, d))
        while nodes and frontier:
            W, _, u, v, d = pop(frontier)
            if v in visited or v not in nodes:
                continue
            it += 1
            if it % k != 0:
                yield u, v, d
            # update frontier
            visited.add(v)
            nodes.discard(v)
            for w, d2 in G.adj[v].items():
                if w in visited:
                    continue
                new_weight = d2.get(weight, 1) * sign
                push(frontier, (new_weight, next(c), v, w, d2))
ALGORITHMS = {
    "prim": prim_mst_edges,
}

def minimum_spanning_edges(G, k, algorithm="prim", weight="weight", keys=True, data=True, ignore_nan=False):

    try:
        algo = ALGORITHMS[algorithm]
    except KeyError as err:
        msg = f"{algorithm} is not a valid choice for an algorithm."
        raise ValueError(msg) from err
    return algo(
        G, k, minimum=True, weight=weight, keys=keys, data=data, ignore_nan=ignore_nan
    )


def ms3(G, k, weight="weight", algorithm="prim", ignore_nan=False):

    edges = minimum_spanning_edges(G, k, algorithm, weight, keys=True, data=True, ignore_nan=ignore_nan)
    T = G.__class__()  # Same graph class as G
    T.graph.update(G.graph)
    T.add_nodes_from(G.nodes.items())
    T.add_edges_from(edges)
    return T

#Inputs:
#G = the graph
#d = parent node
#u = root node
#r = num kids
#l = current k
#t = upper bound of k
#global k
#issues to deal with rn
#will only return max weight cut, not the actual nodes to cut
#the boundaries and base cases are flat out wrong





def kShatter(G, d, u, r, l, t, k):
    
    it = 0
    kids = list(G.neighbors(u))        

    #base case
    if l <= t:
        print("this works")
        return -1*float('inf')
    
    if l == 1:
        #return weight of first r kids of u
        #might need to add parameter to store parent so it doesnt confuse itself
        sum = 0
        for v in kids:
            if it < r and v != d:
                sum += G[u][v]['weight']
                it += 1
        return sum

    if r == 0:
        return 0
    currKid = kids[r - 1]

    options = []
    opts = []  

    for i in range(1, l-1):
        options.append(kShatter(G,d,u,r-1,l-i,t,k) + kShatter(G,u,currKid,len(list(nx.neighbors(G,currKid)))-1,i,t,k))
    
    for i in range(1,k):
        opts.append(kShatter(G,u,currKid,len(list(nx.neighbors(G,currKid)))-1,i,t,k))
    
    option1 = max(options)
    option2 = kShatter(G,d,u,r-1,l,t,k)+G[u][currKid]['weight']+max(opts)
    return max(option1, option2)

@functools.cache
def F(G, k, u, r, l, prev):
    kids = list(G.neighbors(u))
    if prev:
        kids.remove(prev)
        
     # Base case
    sum = 0
    if l == 1:
        for i in kids:
            sum += G[u][i]["weight"]
        return sum

    print(kids, r)
    if r == 0: return float('inf')
    v = kids[r-1]
    print(u, v, r, l, prev)
    cv = len(list(G.neighbors(v)))-1
    option1 = []
    for m in range(1, l):
        option1.append(F(G, k, u, r-1, l-m, prev) + F(G, k, v, cv, m, u))
    if not option1:
        o1 = float('inf')
    else:
        o1 = min(option1)
    option2 = []
    for s in range(1, k + 1):
        option2.append(F(G,k,v,cv,s,u))
    o2 = min(option2) + F(G, k, u, r-1, l, prev) + G[u][v]['weight']
    return min(o1,o2)


"""
#if __name__ == '__main__':
randomG = nx.complete_graph(20)
for (u, v) in randomG.edges():
    randomG[u][v]['weight'] = random.randint(1, 10)
print(randomG)

tree2 = MST(randomG)
print(tree2)
nx.draw(tree2, with_labels = True)
plt.show()
print(F(tree2, 2, 0, len(list(tree2.neighbors(0)))-1, len(list(tree2.nodes)), None))

"""
def MSTStop(G):
    return -1
def TSPapprox(G):
    return -1

def Heuristic():
    return -1

def teamDissolve(self, team):
    return team

def Genetic(G):
    return -1

def spectral(G, k):
    adj_matrix = nx.to_numpy_matrix(G)
    highest = adj_matrix.max()
    n = adj_matrix.shape
    x = numpy.empty(n)
    x.fill(highest)
    adj_matrix = x - adj_matrix
    np.fill_diagonal(adj_matrix, 0)
    adj_matrix[adj_matrix == highest] = 10000000000000
    model = SpectralClustering(n_clusters=k, 
        affinity='precomputed').fit(adj_matrix)
    return model.labels_
