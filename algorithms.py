from starter import *
import networkx as nx
from networkx.utils import py_random_state
import random

__all__ = ['msi_approx', 'greedy', 'planar_solution', 'coloring_solution'] # Not implemented yet

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
Same as M.I.S. solution.
If a graph can be equitably colored in some k colors, the penalty for edge weights is 0.
The only penalty would be 100 * exp(0.5k).
NOTE: This is not realistic, since k would need to be very large. M.I.S. is more realistic.
"""
def coloring_solution(G):
    for k in range(2, 27):
        try:
            colors = nx.coloring.equitable_color(G, k)
        except:
            continue
        for c in colors.keys():
            G.nodes[c]['team'] = colors[c]
        return

# CALL: read_partition(networkx object, filepath)
def read_partition(G):
    name = G.name
    best = None
    best_score = float('inf')
    for k in range(2, 27):
        path = "./sample_partition/" + name + "_part" + str(k) + ".in"
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
    
    for i in range(len(best)):
        team = arr[i]["communityId"] + 1
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
    sum = 0
    it = 0
    kids = list(G.neighbors(u))        

    #base case
    if l <= t:
        return -1*float('inf')
    
    if l == 1:
        #return weight of first r kids of u
        #might need to add parameter to store parent so it doesnt confuse itself
        for v in kids:
            if it < r and v != d:
                sum += G[u][v]['weight']
                it += 1
        return sum

    options = []
    if d:
        kids.remove(d)
    print(r)
    if r-1 not in kids:
        return 0
    currKid = kids[r-1]
    for i in range(1, l-1):
        print(i)
        #the last two parameters probably wrong
        options.append(kShatter(G,d,u,r-1,l-i,t,k)
        + kShatter(G,u,currKid,len(nx.neighbors(G,currKid))-1,i,t,k))
    option1 = max(options)

    options = []  
    for i in range(1,k):
        print(i)
        #again bounds here at end wrong
        options.append(kShatter(G,u,currKid,len(nx.neighbors(G,currKid))-1,i,t,k))
    option2 = kShatter(G,d,u,r-1,l,t,k)+G[u][currKid]['weight']+max(options)
    return max(option1, option2)

if __name__ == '__main__':
    randomG = nx.complete_graph(20)
    for (u, v) in randomG.edges():
        randomG[u][v]['weight'] = random.randint(1, 10)

    tree = MST(randomG)
    print(tree)
    print(kShatter(tree, None, 0, len(list(tree.neighbors(0))), len(tree.nodes), 5, 7))

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