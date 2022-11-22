from starter import *

"""
Problem restatement:
    What is the optimal team assignment of n vertices into k teams,
    such that it minimizes the edges within the same team,
    while k is kept as low as possible, and teams are as even as possible?
Formulate the problem as a decision problem:
    Is there a team assignment of n vertices into a given number of k teams,
    such that total cost is less than t?
Cost function: C = sum(w_ij) + 100e^0.5k, e^(70*||p/|V|-1/k||)
Constraints: Fewer than 10000 edges, each at most weight 1000
"""


def main(path: str):
    best_score = float('inf')
    best_assignment = None
    t = 1
    for k in range(1, 29): # k cannot be any larger than 29; cost of partitioning exceeds cost of conflict edges
        G = read_input(str)
        if query(G, k, t):
            possible_score, possible_assignment = solve(k, t)
            if possible_score == -1:
                continue
            elif best_score >= possible_score:
                best_score = possible_score
                beset_assignment = possible_assignment
    return best_assignment


# IMPLEMENT:

def query(G, k, t):
    if #SOME CONDITION ON THE HEURISTIC IS SATISFIED:
        return True
    else:
        return False
    
def heuristic(G, k):
    return -1

def solve(G, k, t):
    return -1, None
