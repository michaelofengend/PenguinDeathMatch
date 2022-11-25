from starter import *
import random
from networkx.utils import py_random_state
import heapq

def swap(G, window, k):
    baseline = G
    counter = 0
    swaps = BinaryHeap()
    while counter < window:
        swap_node = random.randint(0, len(G.nodes) - 1)
        team_i = G.nodes[swap_node]['team']
        team_j = random.randint(1, k)
        if team_i != team_j:
            new_score = swap_score_change(G, swap_node, team_i, team_j, k)
            

# Use this function ONLY when k is constant
def swap_score_change(G, v, i, j, k):
    """
    Paramters:
    G : Graph to be updated
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
    b, b2 = G.team_vec       # TODO: MAKE team_vec FIELD FOR G: a tuple of (array, norm)
    new_C_p, new_norm = C_p_update(G, b, b2, i, j)
    new_C_w = C_w_update(G.edge_cost, v, i, j)   # TODO: MAKE edge_cost FIELD FOR G
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
def C_w_update(C_w, v, i, j):
    """
    Parameters:
    C_w : FLOAT
        Original C_w value (intra-team conflict cost)
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
        if G[w]['team'] == i:
            C_w -= adj_list[w]['weight']
        elif G[w]['team'] == j:
            C_w += adj_list[w]['weight']
    return C_w