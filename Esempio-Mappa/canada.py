from pyqubo import Array
from pyqubo import Binary, UserDefinedExpress
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

import networkx as nx
from cProfile import label



G = nx.Graph()

nodes=[ 'bc',
        'ab',
        'sk',
        'mb',
        'on',
        'qc',
        'nl',
        'nb',
        'pe',
        'ns',
        'yt',
        'nt',
        'nu']

edges =     [('bc', 'ab'),
              ('bc', 'nt'),
              ('bc', 'yt'),
              ('ab', 'sk'),
              ('ab', 'nt'),
              ('sk', 'mb'),
              ('sk', 'nt'),
              ('mb', 'on'),
              ('mb', 'nu'),
              ('on', 'qc'),
              ('qc', 'nb'),
              ('qc', 'nl'),
              ('nb','ns'),
              ('yt', 'nt'),
              ('nt', 'nu')]
G.add_nodes_from(nodes)
G.add_edges_from(edges)

node_positions = {"bc": (0, 1),
                  "ab": (2, 1),
                  "sk": (4, 1),
                  "mb": (6, 1),
                  "on": (8, 1),
                  "qc": (10, 1),
                  "nb": (10, 0),
                  "ns": (12, 0),
                  "pe": (12, 1),
                  "nl": (12, 2),
                  "yt": (0, 3),
                  "nt": (2, 3),
                  "nu": (6, 3)}


nx.draw_networkx(G, pos=node_positions, with_labels=True,
                      font_color="w", node_size=400)

# Save graph
filename = "/workspace/Tesi/Esempio-Mappa/Canada.png"
plt.savefig(filename)
print("The graph is saved in '{}'.".format(filename))