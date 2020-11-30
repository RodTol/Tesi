# Import the functions and packages that are used
from dwave.system import EmbeddingComposite, DWaveSampler
from dimod import BinaryQuadraticModel

# Definisco il problema, facendo una matrice dei coeff.
# Quelli doppi indicano i coefficienti singoli
# Esempio: problema è   a+4b+2ac
#
#  Q = {('a','a'):1,
# ('b','b'): 4,
# ('a','c'): 2}

# Define the problem as a Python dictionary and convert it to a BQM
Q = {('B','B'): 1, 
    ('K','K'): 1, 
    ('A','C'): 2, 
    ('A','K'): -2, 
    ('B','C'): -2}
# Questo è il problema: b+k+2ac-2ak-2bc
# Se faccio i conti a mano, trovo che le soluzioni con Ene minore
# sono:
# A B C K
# 1 0 0 1
# 0 1 1 0
# Quindi mi aspetto che siano quelle scelte più frequentemente

# Convert the problem to a BQM
bqm = BinaryQuadraticModel.from_qubo(Q)

# Define the sampler that will be used to run the problem
sampler = EmbeddingComposite(DWaveSampler())

# Run the problem on the sampler and print the results
sampleset = sampler.sample(bqm, num_reads = 10)
print(sampleset)