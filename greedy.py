from starter import *
import networkx as nx
from networkx.utils import py_random_state
import random

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

@py_random_state(3)
def modified_msi(G, k, nodes=None, seed=None):
    if not nodes:
        nodes = {seed.choice(list(G))}
    else:
        nodes = set(nodes)
    if not nodes.issubset(G):
        raise nx.NetworkXUnfeasible(f"{nodes} is not a subset of the nodes of G")
    neighbors = set.union(*[set(G.adj[v]) for v in nodes])
    if set.intersection(neighbors, nodes):
        raise nx.NetworkXUnfeasible(f"{nodes} is not an independent set of G")
    indep_nodes = list(nodes)
    available_nodes = set(G.nodes()).difference(neighbors.union(nodes))
    while available_nodes:
        node = seed.choice(list(available_nodes))
        indep_nodes.append(node)
        available_nodes.difference_update(list(G.adj[node]) + [node])
    return indep_nodes


def msi_approx(G):
    teams = []
    G_copy = G.copy()
    average = 0
    while G_copy.number_of_nodes() > average * 0.8:
        curr_msi = modified_msi(G_copy, 100)
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
    # TODO: BALANCE THE TEAMS BY SWAPPING
    return

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


