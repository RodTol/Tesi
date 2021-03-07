
from dwave.system import EmbeddingComposite, DWaveSampler
from dimod import BinaryQuadraticModel

sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))

import dwave.inspector

from pyqubo import Array, UserDefinedExpress
from pyqubo import Binary, WithPenalty

import pprint
pp = pprint.PrettyPrinter(indent=4)

import networkx as nx

# Importo la libreria per graficare i grafi
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

# Set up provinces
bc = Array.create('bc', shape=4, vartype='BINARY')   # British Columbia
ab = Array.create('ab', shape=4, vartype='BINARY')   # Alberta
sk = Array.create('sk', shape=4, vartype='BINARY')   # Saskatchewan
mb = Array.create('mb', shape=4, vartype='BINARY')   # Manitoba
on = Array.create('on', shape=4, vartype='BINARY')   # Ontario
qc = Array.create('qc', shape=4, vartype='BINARY')   # Quebec
nl = Array.create('nl', shape=4, vartype='BINARY')   # Newfoundland and Labrador
nb = Array.create('nb', shape=4, vartype='BINARY')   # New Brunswick
pe = Array.create('pe', shape=4, vartype='BINARY')   # Prince Edward Island
ns = Array.create('ns', shape=4, vartype='BINARY')   # Nova Scotia
yt = Array.create('yt', shape=4, vartype='BINARY')   # Yukon
nt = Array.create('nt', shape=4, vartype='BINARY')   # Northwest Territories
nu = Array.create('nu', shape=4, vartype='BINARY')   # Nunavut  


provinces = [bc, ab, sk, mb, on, qc, nl, nb, pe, ns, yt, nt, nu]


# Set up province neighbours (i.e. shares a border)
neighbours = [(bc, ab),
              (bc, nt),
              (bc, yt),
              (ab, sk),
              (ab, nt),
              (sk, mb),
              (sk, nt),
              (mb, on),
              (mb, nu),
              (on, qc),
              (qc, nb),
              (qc, nl),
              (nb, ns),
              (yt, nt),
              (nt, nu)]
#creo la funzione di scelta di un colore solo
class one_color(UserDefinedExpress):
 def __init__(self, a):
    express = (a[0]+a[1]+a[2]+a[3]-1)**2
    super().__init__(express)
#creo l'espressione da mettere nell'hamiltoniana
H1=one_color(provinces[len(provinces)-1])
for i in range(len(provinces)-1):
    H1=H1+one_color(provinces[i])

#qubo=H1.compile().to_qubo()
#pp.pprint(qubo)

#creo la funzione per penalizzare colori ugali tra vicini
class colori_diversi(UserDefinedExpress):
 def __init__(self, a, b):
    express = a[0]*b[0]+a[1]*b[1]+a[2]*b[2]+a[3]*b[3]
    super().__init__(express)
#creo l'espressione da mettere nell'Hamiltoniana
H2=colori_diversi(neighbours[len(neighbours)-1][0],neighbours[len(neighbours)-1][1])
for i in range(len(neighbours)-1):
    H2=H2+colori_diversi(neighbours[i][0],neighbours[i][1])

#qubo=H2.compile().to_qubo()
#pp.pprint(qubo)

#creo l'ham e la faccio diventare una BQM
model = H1+H2
bqm = model.compile().to_bqm()


#la embeddo e calcolo col sampler
chainstrenght= None
sampleset = sampler.sample(bqm, num_reads = 10, chain_strength=chainstrenght, label="Problema della mappa")
#risultati
#print(sampleset)

#uso l'inspector
dwave.inspector.show(sampleset)

risultato = sampleset.first.sample
#print(risultato)
#print(risultato[0])


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

for i in range(len(color_labels)):
        name = color_labels[i][:2]
        color = color_labels[i][3]
        G.nodes[name]["color"] = color

color_map = [color for name, color in G.nodes(data="color")]

#print(color_map[4].replace('0','red'))

for i in range(13):
    #print(color_map[i])
    color_map[i]=color_map[i].replace('0','red')
    color_map[i]=color_map[i].replace('1','blue')
    color_map[i]=color_map[i].replace('2','green')
    color_map[i]=color_map[i].replace('3','violet')
    #print(color_map[i])
#print(color_map)

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
filename = "/workspace/Tesi/Esempio-Mappa/mappa-colorata.png"
plt.savefig(filename)
print("The graph is saved in '{}'.".format(filename))

