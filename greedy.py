from starter import *
import networkx as nx
from networkx.algorithms import approximation

# INCOMPLETE
def greedy(G, k):
    n = G.number.of.nodes()
    G_copy = nx.complete_graph(n)
    edges = G.edges(data=True)
    edges.sort(lambda x: x['weight'])
    team_size = n / k
    remainder = n - team_size
    while nx.number_connected_components(G) > k:
        longest_edge = edges.pop()
        G.remove_edge(longest_edge)
    
    

G = read_input('./inputs/small1.in')
edges = G.edges(data=True)
