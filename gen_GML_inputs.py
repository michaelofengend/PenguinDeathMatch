from starter import *
import networkx as nx

for i in range(1, 261):
    fn_s = "./inputs/small" + str(i) + ".in"
    fn_m = "./inputs/medium" + str(i) + ".in"
    fn_l = "./inputs/large" + str(i) + ".in"
    G_s = read_input(fn_s)
    G_m = read_input(fn_m)
    G_l = read_input(fn_l)
    nx.write_graphml(G_s, "./GMLinput/small" + str(i) + ".graphml")
    nx.write_graphml(G_m, "./GMLinput/medium" + str(i)+ ".graphml")
    nx.write_graphml(G_l, "./GMLinput/large" + str(i) + ".graphml")

