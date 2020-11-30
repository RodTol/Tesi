# Import the functions and packages that are used
from dwave.system import EmbeddingComposite, DWaveSampler
# Scelgo il gamma
gamma = 21

# Definisco il problema, facendo una matrice dei coeff.
# gamma = 21 non è sufficiente, metto gamma = 40
Q = {('x1','x1'): 15-3*gamma, 
    ('x2','x2'): 20-3*gamma, 
    ('x3','x3'): 25-3*gamma, 
    ('x1','x2'): 2*gamma, 
    ('x1','x3'): 2*gamma,
    ('x2','x3'): 2*gamma}

# Convert the problem to a BQM
bqm = BinaryQuadraticModel.from_qubo(Q, offset=gamma*4.0)

# Define the sampler that will be used to run the problem
sampler = EmbeddingComposite(DWaveSampler())

# Run the problem on the sampler and print the results
sampleset = sampler.sample(bqm, num_reads = 10)
print(sampleset)