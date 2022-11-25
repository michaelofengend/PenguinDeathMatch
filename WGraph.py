from starter import *
class WGraph:
    def __init__(self, G):
        self.graph = G
        self.teams = {}
        for n in self.graph.nodes:
            if n['team'] not in self.graph.teams:
                self.teams[n['team']] = [n]
            self.teams[n['team']].append(n)
        self.cost = score(G)
        self.bnorm = 0 # figure out for cost update
    
    def updateNode(self, n, team):
        self.teams[self.graph.nodes[n]['team']].pop(n)
        self.graph.nodes[n]['team'] = team
        self.teams[team].append(n)
        self.updateCost() #fix here
    
    def updateCost(self):
        return 0