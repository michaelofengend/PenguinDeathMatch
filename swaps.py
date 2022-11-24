from starter import *
import random

def swap(name, window):
    G = read_input(name)
    baseline = G
    it = 0
    while it < window:
        n1ind = random.randint(0, len(G.nodes) - 1)
        n1 = G.nodes[n1ind] # need way to pass to deep reference
        #think of better way to randomly get from not same team, possibly get list of nodes in teams
        n2ind = random.randint(0, len(G.nodes) - 1)
        n2 = G.nodes[n2ind]
        if n1['team'] != n2['team']:
            n1team = n1['team']
            n1['team'] = n2['team']
            n2['team'] = n1team
            Gcopy = G.copy()
            Gcopy.nodes[n1ind] = n1
            Gcopy.nodes[n2ind] = n2
            #inefficient score calc, use hw alg
            G = Gcopy
            if score(Gcopy) > score(baseline):
                baseline = Gcopy
                it = 0
            else:
                it += 1
swap("small.in", 0)


# Use this function ONLY when k is constant
def swap_score_update(G, v, i, j, k):  # FIXME: FIND ALL ARGUMENTS
    """
    Paramters:
    G : Graph to be updated
    v : INTEGER
        node to be updated
    i : INTEGER
        Original team of v
    j : INTEGER
        New team of v
    k : INTEGER
        Number of teams (Should remain constant)
    Description:
    Returns new score of the swap.
    """
    new_C_p, new_norm = C_p_update(G, b, b2, i, j)
    # TODO: Store new norm
    new_C_w = C_w_update(C_w, t_arr, v, i, j)
    return new_C_w + 100 * math.exp(k/2) + new_C_p

# Returns updated score of C_p (team evenness cost)
def C_p_update(G: nx.Graph, b, b2, i, j):
    """
    Parameters:
    G : Graph to be updated
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
def C_w_update(C_w, t_arr, v, i, j):
    """
    Parameters:
    C_w : FLOAT
        Original C_w value (intra-team conflict cost)
    t_arr : ARRAY
        Team ASSIGNMENT vector: t_arr[i] gives the team of node i
    v : INTEGER
        Node to be swapped
    i : INTEGER
        Original team of vertex to be swapped
    j : INTEGER
        New team of vertex to be swapped

    Description:
    Returns the new C_w.
    """
    adj_list = G[v]
    for w in adj_list.keys():
        if t_arr[w] == i:
            C_w -= adj_list[w]['weight']
        elif t_arr[w] == j:
            C_w += adj_list[w]['weight']
    return C_w