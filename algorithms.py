from starter import *
import networkx as nx
import random
from heapq import heappop, heappush
from itertools import count
import multiprocessing as mp
import time
from math import ceil
import matplotlib.pyplot as plt
import functools
import numpy
import sklearn.cluster
from sklearn.cluster import SpectralClustering
import scipy.sparse
import itertools
import pandas as pd

functions = ["mis_approx", "two_coloring_solution", "color_MST", "random_color", "read_partition"]
random_funcs = ["mis_approx", "color_MST", "random_color"]

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
def mis_approx(G):
    teams = []
    G_copy = G.copy()
    average = 0
    while G_copy.number_of_nodes() > average * 0.8:   # Continuously removes M.I.S. from the graph
        curr_msi = nx.maximal_independent_set(G_copy)
        G_copy.remove_nodes_from(curr_msi)
        teams.append(set(curr_msi))
        average = sum(len(t) for t in teams) / len(teams)
    s = G_copy.nodes()
    teams.append(s)
    i = 1
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
    pass

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
    for _ in range(50):
        max_st = nx.maximum_spanning_tree(G, algorithm='prim')
        highest_degree = (max(max_st.degree(), key = lambda x:x[1]))[1]
        colors = nx.coloring.equitable_color(max_st, highest_degree + 1)
        for c in colors.keys():
            G.nodes[c]['team'] = colors[c] + 1
        new_score = score(G)


def random_color(G):
    best = float('inf')
    best_coloring = None
    colors = nx.coloring.greedy_color(G, strategy = 'random_sequential', interchange=True)
    for c in colors.keys():
        G.nodes[c]['team'] = colors[c]
        new_score = score(G)
        if new_score < best:
            best = new_score
            best_coloring = colors
    for c in best_coloring.keys():
        G.nodes[c]['team'] = best_coloring[c]

def read_partition(G):
    name = G.name
    best = None
    best_score = float('inf')
    for k in range(2, 18):
        path = "./sample_partition_3/" + name + "_part" + str(k) + ".in"
        with open(path) as fp:
            arr = json.load(fp)
        size = arr[-1]["nodeId"] - arr[0]["nodeId"]
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
                if not G.has_edge(u,v):
                    G.add_edge(u,v, weight=0)
    return G

def MST(G):
    preprocessforMST(G)
    return nx.minimum_spanning_tree(G)

def prim_mst_edges(G, k, weight="weight"):
    push = heappush
    pop = heappop

    nodes = set(G)
    c = count()

    nodesInMST = []
    while nodes:
        u = nodes.pop()
        frontier = []
        visited = {u}
        for v, d in G.adj[u].items():
            wt = d.get(weight, 1)
            push(frontier, (wt, next(c), u, v, d))
        
        while nodes and frontier:
            W, _, u, v, d = pop(frontier)
            if v in visited or v not in nodes:
                continue
            if u not in nodesInMST:
                nodesInMST.append(u)
            if v not in nodesInMST:
                nodesInMST.append(v)
            yield u, v, d
            #if len(list(G.nodes)) < k:
            #if len(list(G.nodes)) < 2*k and len(list(G.nodes)) > k and not len(list(G.nodes)) == len(nodesInMST):
            #    continue
            if len(nodesInMST) == k or len(list(G.nodes)) == len(nodesInMST):
                for i in nodesInMST:
                    G.remove_node(i)
                return
            

            # update frontier
            visited.add(v)
            nodes.discard(v)
            for w, d2 in G.adj[v].items():
                if w in visited:
                    continue
                new_weight = d2.get(weight, 1)
                push(frontier, (new_weight, next(c), v, w, d2))

def MST3(G, k):
    extra_count = len(list(G.nodes)) % k - 1
    
    edges = prim_mst_edges(G, k, weight="weight")

    edges = list(edges)
    
    l = 0
    while l != len(edges):
        l = len(edges)
        edges.extend(list(prim_mst_edges(G, k, weight="weight")))
    
    extra_nodes = []
    if extra_count != -1:
        extra_edges = edges[-extra_count:]
        edges = edges[0:-extra_count]
        for edge in extra_edges:
            for node in edge[0:2]:
                if node not in extra_nodes:
                    extra_nodes.append(node)
    
    edges = iter(edges)
    
    T = G.__class__()  # Same graph class as G
    T.graph.update(G.graph)
    T.add_nodes_from(G.nodes.items())
    T.add_edges_from(edges)
    T.remove_nodes_from(extra_nodes)
    return T, extra_nodes

def postprocessMST3(T, G, extra_nodes):
    """
    teams = list(nx.connected_components(T))
    for node in extra_nodes:
        scores = []
        i = 0
        for t in teams:
            for v in t:
                if len(scores) <= i:
                    scores.append(G[node][v]['weight'])
                else:
                    scores[i] += G[node][v]['weight']
            scores[i] = {scores[i]: [list(t)[0],i]}
            i += 1
        key = float('inf')
        val = float('inf')
        t = float('inf')
        for i in range(len(scores)):
            x = list(scores[i].keys())[0]
            y = list(scores[i].values())[0][0]
            z = list(scores[i].values())[0][1]
            if key >= x:
                key = x
                val = y
                t = z
        teams[t].add(val)
        
        T.add_edge(node, val, weight = G[node][val]['weight'])
    """
    ######################################################################

    teams = list(nx.connected_components(T))
    for i in range(len(teams)):
        for v in teams[i]:
            G.nodes[v]['team'] = i + 1

    for node in extra_nodes:
        potential_penalty = [0] * len(teams)
        
        for neighbor in G.neighbors(node):
            if G.nodes[neighbor].get('team'):
                neighbor_team = G.nodes[neighbor]['team']
                potential_penalty[neighbor_team - 1] += G[node][neighbor]['weight']
        
        best_team = np.argmin(potential_penalty)
        G.nodes[node]['team'] = best_team + 1
    
    return G


def team_assign(T, G):
    team_number = 1
    for t in list(nx.connected_components(T)):
        for i in t:
            G.nodes[i]['team'] = team_number
        team_number += 1
    return score(G), G

def runRandom(randomG):
    """
    randomG = nx.complete_graph(15)
    for i in range(10):
        x = random.randint(1, 10)
        y = random.randint(1, 10)
        if x != y and randomG.has_edge(x, y):
            randomG.remove_edge(x,y)
    for (u, v) in randomG.edges():
        randomG[u][v]['weight'] = random.randint(1, 10)
    """
    graph = preprocessforMST(randomG)
    graph_copy = graph.copy()
    tree, extra_nodes = MST3(graph, 24)
    post = postprocessMST3(tree, graph_copy, extra_nodes)
    print(post)
    """
    pos=nx.spring_layout(post)
    nx.draw_networkx(post, pos)
    labels = nx.get_edge_attributes(post, 'weight')
    nx.draw_networkx_edge_labels(post, pos, edge_labels=labels)
    plt.show()
    """
    return post

def makeGraphs(jim):
    for i in range(1, 261):
        inputG2 = read_input('./inputs/small' + str(i) + '.in')
        inputG = preprocessforMST(inputG2)
        make_copy = inputG.copy()
        tree, extra_nodes = MST3(inputG, jim)
        if extra_nodes:
            tree = postprocessMST3(tree, make_copy, extra_nodes)
        #pos=nx.spring_layout(tree2)
        #nx.draw_networkx(tree2, pos)
        #labels = nx.get_edge_attributes(tree2, 'weight')
        #nx.draw_networkx_edge_labels(tree2, pos, edge_labels=labels)
        inputG1 = read_input('./inputs/small' + str(i) + '.in')
        sc, graph = team_assign(tree, inputG1)
        write_output(graph, './mst_take3/small' + str(i) + 'part' + str(jim) + '.out')
    print('done' + str(jim))

def mst_stop1(G):
    best_score = float('inf')
    best = 0
    for i in range(5, 61):
        read_output(G, './mst_take1/' + G.name + 'part' + str(i) + '.out')
        if score(G) < best_score:
            best_score = score(G)
            best = i
    read_output(G, './mst_take1/' + G.name + 'part' + str(best) + '.out')

def mst_stop2(G):
    best_score = float('inf')
    best = 0
    for i in range(5, 61):
        read_output(G, './mst_take2/' + G.name + 'part' + str(i) + '.out')
        if score(G) < best_score:
            best_score = score(G)
            best = i
    read_output(G, './mst_take2/' + G.name + 'part' + str(best) + '.out')

def mst_stop3(G):
    best_score = float('inf')
    best = 0
    for i in range(5, 61):
        read_output(G, './mst_take3/' + G.name + 'part' + str(i) + '.out')
        if score(G) < best_score:
            best_score = score(G)
            best = i
    read_output(G, './mst_take3/' + G.name + 'part' + str(best) + '.out')

def runMultiProcess():
    pool = mp.Pool(mp.cpu_count())
    pool = mp.Pool()
    res = pool.map(makeGraphs, [i for i in range(5, 61)])
    pool.close()
    pool.join()

def scoreAll():
    best = pd.read_csv('bestscores.csv')
    id = best['Graph']
    sc = best['Score']
    sizes = ['small', 'medium', 'large']
    dic = {}
    for i in range(1, 261):
        G = read_input('./inputs/small' + str(i) + '.in')
        ls= []
        for j in range(5, 61):
            newG = read_output(G, './mst_take3/small' + str(i) + 'part' + str(j) + '.out')
            ls.append(score(newG))
        dic['small' + str(i)] = min(ls)
    coun = 0
    for k in range(260):
        if id[k] == list(dic.keys())[k]:
            print(id[k], sc[k], list(dic.values())[k])
            if sc[k] * 1.2 >= list(dic.values())[k]:
                coun += 1
    print(coun)

if __name__ == '__main__':
    scoreAll()


        
            
#print(F(tree, 2, 0, len(list(tree.neighbors(0)))-1, len(list(tree.nodes)), None))



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

def min_clique_cover(G):
    G_comp = nx.complement(G)
    for c in nx.find_cliques(G):
        print(len(c))