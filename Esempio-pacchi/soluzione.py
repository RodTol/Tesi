# Import the functions and packages that are used
from dwave.system import EmbeddingComposite, DWaveSampler
from dimod import BinaryQuadraticModel
#Esempio da learn to formulate problem for dwawe system
#pagina 17

#importo l'analizzatore
import dwave.inspector

# Scelgo il gamma in maniera tale che la soluzione x1 x2 sa la energia piu bassa
gamma = 21

# Definisco il problema, facendo una matrice dei coeff.
#min[15x1 + 20x2 + 25x3 + gamma(x1+x2+x3-2)^2] -->
# (15-3gamma)x1 + (20-3gamma)x2 + (25-3gamma)x3 + 2gammax1x2 + 2gammax1x3 + 2gammax2x3 +4gamma 
Q = {('x1','x1'): 15-3*gamma, 
    ('x2','x2'): 20-3*gamma, 
    ('x3','x3'): 25-3*gamma, 
    ('x1','x2'): 2*gamma, 
    ('x1','x3'): 2*gamma,
    ('x2','x3'): 2*gamma}

# NOTA che ho messo l'offset ossia il termine noto
# Convert the problem to a BQM
bqm = BinaryQuadraticModel.from_qubo(Q, offset=gamma*4.0)

# Define the sampler that will be used to run the problem
sampler = EmbeddingComposite(DWaveSampler(solver={'qpu': True}))

# Ho dovuto mettere 100 estrazioni perche ho energie vicine e quindi senno
# cado nel buco sbagliato
# Run the problem on the sampler and print the results
sampleset = sampler.sample(bqm, num_reads = 100)
print(sampleset)

dwave.inspector.show(sampleset)