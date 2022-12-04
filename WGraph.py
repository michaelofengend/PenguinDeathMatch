from starter import *
import algorithms

class WGraph:
    def __init__(self, G, init_method = ""):
        """
        Parameters:
        G : networkx Graph object
            Needs to be initialized first
        init_method : String
            Name of method used to initialize team assignments
        """
        self.graph = G
        self.teams = []
        if init_method:
            init_func = getattr(algorithms, init_method)
            init_func(G)
            output = [G.nodes[v]['team'] for v in range(G.number_of_nodes())]
            teams, counts = np.unique(output, return_counts=True)
            k = np.max(teams)
            self.k = k
            b = np.array((counts / G.number_of_nodes()) - 1 / k)
            C_w = sum(d for u, v, d in G.edges(data='weight') if output[u] == output[v])
            self.C_w = C_w
            self.cost = score(G)
            self.b = b
            self.bnorm = np.linalg.norm(b, 2)
        else:
            self.cost = score(G)
            self.b = None
            self.bnorm = 0

    def updateSwap(self, n, team_j, new_cost): # These parameters can be obtained from swaps.swap
        self.graph.nodes[n]['team'] = team_j
        self.cost = new_cost

    def updateNode(self, n, team):
        self.teams[self.graph.nodes[n]['team']].pop(n)
        self.graph.nodes[n]['team'] = team
        self.teams[team].append(n)
        self.updateCost() #fix here
    
    def updateCost(self):
        return 0