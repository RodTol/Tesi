# Import the functions and packages that are used
from dwave.system import EmbeddingComposite, DWaveSampler
from dimod import BinaryQuadraticModel

#Definire il problema
# Define the problem as a Python dictionary and convert it to a BQM
Q = {('B','B'): 1, 
    ('K','K'): 1, 
    ('A','C'): 2, 
    ('A','K'): -2, 
    ('B','C'): -2}

# Convert the problem to a BQM
bqm = BinaryQuadraticModel.from_qubo(Q)

# Define the sampler that will be used to run the problem
sampler = EmbeddingComposite(DWaveSampler())

# Run the problem on the sampler and print the results
sampleset = sampler.sample(bqm, num_reads = 10)
print(sampleset)