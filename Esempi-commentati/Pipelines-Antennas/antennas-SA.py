# Import networkx for graph tools
import networkx as nx

# Import dwave_networkx for d-wave graph tools/functions
import dwave_networkx as dnx

# Import matplotlib.pyplot to draw graphs on screen
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

# Set the solver we're going to use
# Uso un metodo classico, quindi il simulated annealing 
# La funzione è il neal
import neal

# Con questo comando preparo il sampler
sampler = neal.SimulatedAnnealingSampler()

# Create empty graph
G = nx.Graph()

#Mettiamo un grafo fisso in modo da controllare la bontà dei risultati
grafo = open("grafo.txt", "rb")
G = nx.read_adjlist(grafo)

# Find the maximum independent set, S
# Sto usando un funzione nota con il sampler da me scelto
S = dnx.maximum_independent_set(G, sampler=sampler, num_reads=100)

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
original_name = "antenna_plot_original-SA.png"
nx.draw_networkx(G, pos=pos, with_labels=True)
plt.savefig(original_name, bbox_inches='tight')

# Save solution graph
# Note: red nodes are in the set, blue nodes are not
solution_name = "antenna_plot_solution-SA.png"
nx.draw_networkx(k, pos=pos, with_labels=True, node_color='r', font_color='k')
nx.draw_networkx(othersubgraph, pos=pos, with_labels=True, node_color='b', font_color='w')
plt.savefig(solution_name, bbox_inches='tight')

print("Your plots are saved to {} and {}".format(original_name, solution_name))
