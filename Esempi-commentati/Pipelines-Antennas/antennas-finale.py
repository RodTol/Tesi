# Autore: Rodolfo Tolloi

# Con questo programma voglio creare un codice che, dato un grafo
# qualsiasi, trovi il suo maximum indipendet set, ossia il numero
# massimo di nodi non connessi all'interno del grafo.
# Per fare ciò, andrà per prima cosa creata una QUBO che abbia
# come obbiettivo quello di individuare con la minima energia il set
# indipendete più grande.
# Succesivamente faro del sampling usato uno dei sample del D-wawe,
# che può essere sia quantistico che classico, trovando quindi
# il risultato migliore statisticamente.
# Infine riconverirò il risultato migliore da una list a un
# grafo che proietterò sopra a quello orginale. 
# Per creare questo procedimento ho modificato la funzione
# dnx.maximum_independent_set dal pacchetto dwawe_networkx.
#
# Per fare ciò usero varie librerie:
# - Il pacchetto dwave_networkx.algorithms.independent_set ha
#   al suo interno la funzione  maximum_weighted_independent_set_qubo
#   che crea la QUBO richiesta
# - networkx per creare visualizzare e modificare i grafi
# - il pacchetto matplotlib.pyplot per graficare
# - l'inspector della d-wawe da dwawe.inspector
# - Uno dei sampler da dwawe.system.sampler
# - Un embedder da dwave.system.composites

# Importo questo pacchetto perche devo ricreare la funzione
# dnx.maximum_independent_set a mano in modo da avere il sampleset
# e analizzarlo. La funziona da pacchetto infatti mi restituisce 
# automaticamente il risultato migliore!
from dwave_networkx.algorithms.independent_set import maximum_weighted_independent_set_qubo

# Importo il pacchetto per modificare i grafi
import networkx as nx

# Importo la libreria per graficare i grafi
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

# Importo l'analizzatore
import dwave.inspector

# Selezioni il sampler che useremo. Voglio un metodo quantistico,
# quindi uso il DwaweSampler ma avrò bisogno di librerie per
# l'embedding
from dwave.system.samplers import DWaveSampler

# Importo quindi un embedder automatico veloce
from dwave.system.composites import EmbeddingComposite

# Preparo il sampler usando l'embedding scelto
sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))

# Creo un grafo vuoto
G = nx.Graph()

# Prendo un grafo da un file creato con un altro codice
# in modo da poter ripetere computazioni sullo stesso problema
grafo = open("grafo.txt", "rb")
G = nx.read_adjlist(grafo)

#Creo la QUBO usando la funzione di libreria estratta prima
Q = maximum_weighted_independent_set_qubo(G, weight = None, lagrange=2.0)

#Faccio l'annealing per 100 volte e creo dunque il mio sampleset
response = sampler.sample_qubo(Q, num_reads=200, label='Problema delle antenne')

# Visuliazziamo che tipo di risultati ho avuto
# print(response)

# COMMENTO: ricorda che la soluzione migliore è quella a
# a energia più bassa, ma noi vorremmo fosse anche quella
# che esce più volte.

# Seleziono il risultato con l'energi più bassa e lo visualizzo
sample = next(iter(response))
print(sample)

# I nodi che hanno spin up sono quelli presenti nel set minimo
# mentre quelli con spin nullo no. Creo quindi la mia lista di nodi
S = [node for node in sample if sample[node] > 0]

# Uso l'inspector sul mio sampleset
dwave.inspector.show(response)

# Visualizzo il risultato ottenuto
print('Maximum independent set size found is', len(S))
print(S)

# Vado a creare il grafo con i nodi trovati dalla soluzione
k = G.subgraph(S)
notS = list(set(G.nodes()) - set(S))
othersubgraph = G.subgraph(notS)
pos = nx.spring_layout(G)
plt.figure()

# Salvo e stampo una immagine con il grafo originale
original_name = "antenna_plot_original.png"
nx.draw_networkx(G, pos=pos, with_labels=True)
plt.savefig(original_name, bbox_inches='tight')

# Salvo la soluzione e la stampo
# NOTA: i nodi in rosso sono quelli che fanno parte del mio maximum set,
# quelli in blu no
solution_name = "antenna_plot_solution.png"
nx.draw_networkx(k, pos=pos, with_labels=True, node_color='r', font_color='k')
nx.draw_networkx(othersubgraph, pos=pos, with_labels=True, node_color='b', font_color='w')
plt.savefig(solution_name, bbox_inches='tight')

print("I plot sono salvati in {} e {}".format(original_name, solution_name))