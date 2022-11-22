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
