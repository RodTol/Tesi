import networkx as nx
import networkx.algorithms.approximation as nxaa
import time

start = time.time()
 
# build up a graph
#grafo = open("/workspace/Tesi/Esempi-commentati/Pipelines-Antennas/JOHNSON8-2-4.txt", "rb")
grafo = open("/workspace/Tesi/Esempi-commentati/Pipelines-Antennas/chesapeake.txt", "rb")
#grafo = open("grafo.txt", "rb")
G = nx.read_edgelist(grafo)
#G = nx.read_adjlist(grafo)
 
# Independent set
maximal_iset = nx.maximal_independent_set(G)
end = time.time()

print(end - start,"s")
print(maximal_iset)
print("la dimensione del massimo set indipendente è:", len(maximal_iset))