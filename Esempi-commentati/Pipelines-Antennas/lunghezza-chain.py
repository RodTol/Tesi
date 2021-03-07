from dwave.embedding.pegasus import find_clique_embedding
import neal
import dimod
import dwave_networkx as dnx
import networkx as nx
import dwave.embedding

num_variables = 45
embedding = dwave.embedding.pegasus.find_clique_embedding(num_variables,8)
print(max(len(chain) for chain in embedding.values()))
