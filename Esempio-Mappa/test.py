from pyqubo import Array
from pyqubo import Binary, UserDefinedExpress
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

import networkx as nx
from cProfile import label

array = Array.create('bc', shape=4, vartype='BINARY')
#print(array)


risultato={'ab[0]': 0, 'ab[1]': 1, 'ab[2]': 0, 'ab[3]': 0, 'bc[0]': 0,
 'bc[1]': 0, 'bc[2]': 0, 'bc[3]': 1, 'mb[0]': 0, 'mb[1]': 1, 'mb[2]': 0,
  'mb[3]': 0, 'nb[0]': 0, 'nb[1]': 1, 'nb[2]': 0, 'nb[3]': 0, 'nl[0]': 0,
   'nl[1]': 0, 'nl[2]': 0, 'nl[3]': 1, 'ns[0]': 1, 'ns[1]': 0, 'ns[2]': 0,
    'ns[3]': 0, 'nt[0]': 1, 'nt[1]': 0, 'nt[2]': 0, 'nt[3]': 0, 'nu[0]': 0,
     'nu[1]': 0, 'nu[2]': 0, 'nu[3]': 1, 'on[0]': 1, 'on[1]': 0, 'on[2]': 0,
      'on[3]': 0, 'pe[0]': 0, 'pe[1]': 0, 'pe[2]': 1, 'pe[3]': 0, 'qc[0]': 0,
       'qc[1]': 0, 'qc[2]': 1, 'qc[3]': 0, 'sk[0]': 0, 'sk[1]': 0, 'sk[2]': 1,
        'sk[3]': 0, 'yt[0]': 0, 'yt[1]': 0, 'yt[2]': 1, 'yt[3]': 0}
#print(risultato)

#graficare la soluzione
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

color_labels = [k for k, v in risultato.items() if v == 1]
#print(type(color_labels[1]))
#print(color_labels[1][:2])
#print(color_labels[1][3])
#giulia=(color_labels[1].split('_'))
#print(giulia)

for i in range(len(color_labels)):
        name = color_labels[i][:2]
        color = color_labels[i][3]
        G.nodes[name]["color"] = color

color_map = [color for name, color in G.nodes(data="color")]

print(color_map[4].replace('0','red'))

for i in range(13):
    print(color_map[i])
    color_map[i]=color_map[i].replace('0','red')
    color_map[i]=color_map[i].replace('1','blue')
    color_map[i]=color_map[i].replace('2','green')
    color_map[i]=color_map[i].replace('3','violet')
    print(color_map[i])
print(color_map)

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
                     node_color=color_map, font_color="w", node_size=400)

# Save graph
filename = "/workspace/Tesi/Esempio-Mappa/graph.png"
plt.savefig(filename)
print("The graph is saved in '{}'.".format(filename))