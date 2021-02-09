# Questo è un piccolo tool per generare grafi e stamparli come
# lista di adiacenza su un file txt
# Author: Rodolfo Tollois

# Import networkx for graph tools
import networkx as nx

# Importo il generatore di grafi
from networkx.generators.random_graphs import erdos_renyi_graph
# Genero un grafo con N nodi e una probabilità che creino collegamenti P
n = 30
p = 0.3
g = erdos_renyi_graph(n, p)

# Creo un file e ci scrivo sopra la lista di adiacenza
file_uno = open("grafo.txt", "wb")
nx.write_adjlist(g, file_uno)
file_uno.close()  