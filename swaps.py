from starter import *
import random
from networkx.utils import py_random_state, BinaryHeap
import WGraph

def swap(G: WGraph, window, k):
    """
    Returns: (n, j)
    Where swapping node n to team j results in a reduction in score.
    """
    baseline = G
    counter = 0
    swaps = BinaryHeap()
    while counter < window:
        swap_node = random.randint(0, len(G.nodes) - 1)
        team_i = G.nodes[swap_node]['team']
        team_j = random.randint(1, k)
        if team_i != team_j:
            new_score = swap_score_change(G, swap_node, team_i, team_j, k) # Calculates new score without mutating the object
            if new_score > G.cost:
                continue
            swaps.insert(new_score, (swap_node, team_j)) # Pushes tuple (swap_node, team_j) with value new_score to heap swaps
            counter += 1
    try:
        best_score, best_swap = swaps.min()
        return best_score, best_swap
    except nx.NetworkXError:
        return None # No improvement found; in this current implementation, will not return None

"""
Adam's swap
def swap(G, window):
    currCost = cost(G)
    lastG = G
    globalMin = lastG
    it = 0
    while it < window:
        n1ind = random.randint(0, len(lastG.nodes) - 1)
        n1 = lastG.nodes[n1ind] # need way to pass to deep reference
        #think of better way to randomly get from not same team, possibly get list of nodes in teams
        n2ind = random.randint(0, len(lastG.nodes) - 1)
        n2 = lastG.nodes[n2ind]
        if n1['team'] != n2['team']:
            n1team = n1['team']
            n1['team'] = n2['team']
            n2['team'] = n1team
            nextG = lastG.copy()
            nextG.nodes[n1ind] = n1
            nextG.nodes[n2ind] = n2
            #inefficient score calc, use hw alg
            lastG = nextG
            currCost =
            if score(lastG) > score(globalMin):
                globalMin = lastG
                it = 0
            else:
                it += 1
"""

# Use this function ONLY when k is constant
def swap_score_change(G, v, i, j, k):
    """
    Paramters:
    G : WGraph to be updated
    v : INTEGER
        node to be updated
    b : ARRAY
        Vector describing team sizes
    i : INTEGER
        Original team of v
    j : INTEGER
        New team of v
    k : INTEGER
        Number of teams (Should remain constant)
    Description:
    Returns new score of the swap.
    """
    b, b2 = G.b, G.bnorm
    new_C_p, new_norm = C_p_update(G, b, b2, i, j)
    new_C_w = C_w_update(G, v, i, j)   # TODO: MAKE edge_cost FIELD FOR G
    return new_C_w + 100 * math.exp(k/2) + new_C_p

# Returns updated score of C_p (team evenness cost)
def C_p_update(G: WGraph, b, b2, i, j):
    """
    Parameters:
    G : WGraph to be updated
    b : ARRAY
        Vector describing team sizes
    b2 : FLOAT
        Norm of the current team size vector
    i : INTEGER
        Original team of vertex to be swapped
    j : INTEGER
        New team of vertex to be swapped
    Description:
    Returns the new C_p and the new norm of the team vector.
    """
    n = G.number_of_nodes
    new_b_i = b[i] - 1 / n
    new_b_j = b[j] - 1 / n
    new_norm = math.sqrt(
        b2^2 - (b[i])^2 - (b[j])^2 + new_b_i^2 + new_b_j^2
    )
    new_C_p_score = math.exp(70*new_norm)
    return new_C_p_score, new_norm

# Returns updated score of C_w (intra-team conflict cost)
def C_w_update(WG: WGraph, v, i, j):
    """
    Parameters:
    WG : WGraph object
        Solution instance
    v : INTEGER
        Node to be swapped
    i : INTEGER
        Original team of vertex to be swapped
    j : INTEGER
        New team of vertex to be swapped
    Description:
    Returns the new C_w.
    """
    C_w = WG.C_w
    G = WG.graph
    adj_list = G[v]
    for w in adj_list.keys():
        if G[w]['team'] == i:
            C_w -= adj_list[w]['weight']
        elif G[w]['team'] == j:
            C_w += adj_list[w]['weight']
    return C_w