from starter import *
import random
import WGraph

def swap(WG: WGraph, window, depth):
    """
    Returns: score, (n, j)
    Where swapping node n to team j results in a reduction in score.
    """
    if depth == 0:
        return WG
    counter = 0
    best = WG
    while counter < window:
        G = WG.graph
        swap_node = random.randint(0, len(G.nodes) - 1)
        team_i = G.nodes[swap_node]['team']
        team_j = random.randint(1, WG.k)
        if team_i != team_j:
            new_WG = WG.copy()
            swap_update(new_WG, swap_node, team_i, team_j)
            if new_WG.cost < best.cost:
                best = new_WG
                counter = 0
            counter += 1
    return swap(best, window, depth - 1)

# Use this function ONLY when k is constant
def swap_update(WG: WGraph, v, i, j):
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
    Description:
    Returns new score of the swap, the new C_w score, and the new norm.
    """
    new_C_p = C_p_update(WG, i, j)
    new_C_w = C_w_update(WG, v, i, j)
    WG.C_w = new_C_w
    WG.cost = new_C_p + new_C_w + 100 * math.exp(K_EXP * WG.k)
    WG.graph.nodes[v]['team'] = j

# Returns updated score of C_p (team evenness cost)
def C_p_update(WG: WGraph, i, j):
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
    n = WG.graph.number_of_nodes()
    b = WG.b
    b2 = WG.bnorm
    new_b_i = b[i - 1] - 1 / n
    new_b_j = b[j - 1] - 1 / n
    new_norm = math.sqrt(
        b2**2 - (b[i - 1])**2 - (b[j - 1])**2 + new_b_i**2 + new_b_j**2
    )
    WG.b[i - 1] = new_b_i
    WG.b[j - 1] = new_b_j
    WG.bnorm = new_norm
    new_C_p_score = math.exp(70*new_norm)
    return new_C_p_score

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
        if G.nodes[w]['team'] == i:
            C_w -= adj_list[w]['weight']
        elif G.nodes[w]['team'] == j:
            C_w += adj_list[w]['weight']
    return C_w


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
