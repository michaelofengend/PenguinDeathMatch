from starter import *
import networkx as nx
import matplotlib.pyplot as plt 
import sys


# num = File Number
# size = File Size


def draw(size, num):
    G = read_input('./inputs/' + f'{size}' + f'{num}' + '.in' )
    subax1 = plt.subplot(121)
    pos = nx.spring_layout(G)
    nx.draw(G, with_labels=True, font_weight='bold')
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
    plt.show()

if __name__ == '__main__':
    args = sys.argv
    draw(args[1], args[2])