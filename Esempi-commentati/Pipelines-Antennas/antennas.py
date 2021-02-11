
#Importo questo pacchetto perche devo ricreare la funzione dnx.maximum_independent_set
# a mano in modo da avere il sampleset e analizzarlo. La funziona da pacchetto infatti 
# mi restituisce automaticamente il risultato migliore!
from dwave_networkx.algorithms.independent_set import maximum_weighted_independent_set_qubo

# Import networkx for graph tools
import networkx as nx

# Import dwave_networkx for d-wave graph tools/functions
import dwave_networkx as dnx

# Import matplotlib.pyplot to draw graphs on screen
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

#importo l'analizzatore
import dwave.inspector

# Set the solver we're going to use
# Uso un metodo quantistico, quindi il DwaweSampler che pero fa uso di 
# librerie per l'embedding

from dwave.system.samplers import DWaveSampler

# Uso un embedder per mappare il mio problema per il mio sampler scelto

from dwave.system.composites import EmbeddingComposite

# Con questo comando preparo il sampler usando l'embedding scelto
sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))

# Create empty graph
G = nx.Graph()

#Mettiamo un grafo fisso in modo da controllare la bontà dei risultati
grafo = open("grafo.txt", "rb")
G = nx.read_adjlist(grafo)

#Creo la QUBO usando una funzione di libreria
Q = maximum_weighted_independent_set_qubo(G, weight = None, lagrange=2.0)

#Calcolo il sampleset
response = sampler.sample_qubo(Q, num_reads=200)

# visuliazziamo che tipo di risultati ho avuto
print(response)

# we want the lowest energy sample
sample = next(iter(response))

# quale ho scelto
print(sample)

# nodes that are spin up or true are exactly the ones in S.
# Creo la lista con i nodi del mio maximum indipendent set
S = [node for node in sample if sample[node] > 0]

# Uso l'inspector
dwave.inspector.show(response)
# Find the maximum independent set, S
# Sto usando un funzione nota che crea automaticamente la QUBO e poi sampla
# con il sampler da me scelto. Questa funzione mi da già il risultato migliore
# e non tutto il sampleset!
#   S = dnx.maximum_independent_set(G, sampler=sampler, num_reads=100)

# Print the solution for the user
print('Maximum independent set size found is', len(S))
print(S)

# Visualize the results
k = G.subgraph(S)
notS = list(set(G.nodes()) - set(S))
# Creo un sottografo con i nodi trovati dalla soluzione
othersubgraph = G.subgraph(notS)
pos = nx.spring_layout(G)
plt.figure()

# Save original problem graph
original_name = "antenna_plot_original.png"
nx.draw_networkx(G, pos=pos, with_labels=True)
plt.savefig(original_name, bbox_inches='tight')

# Save solution graph
# Note: red nodes are in the set, blue nodes are not
solution_name = "antenna_plot_solution.png"
nx.draw_networkx(k, pos=pos, with_labels=True, node_color='r', font_color='k')
nx.draw_networkx(othersubgraph, pos=pos, with_labels=True, node_color='b', font_color='w')
plt.savefig(solution_name, bbox_inches='tight')

print("Your plots are saved to {} and {}".format(original_name, solution_name))
