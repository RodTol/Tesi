import dwavebinarycsp
import dwave.inspector
from dwave.system.samplers import DWaveSampler
from dwave.system.composites import EmbeddingComposite

sampler = EmbeddingComposite(DWaveSampler(solver='Advantage_system1.1'))

# Creo una classe nuova per le provincie, le
# quali avranno 5 caratteristiche: nome, rosso,verde
# blu, viola

class Provincia:
  def __init__(self, name):
    self.name = name
    self.r = name + "_r"
    self.g = name + "_g"
    self.b = name + "_b"
    self.v = name + "_v"

# Set up provinces
bc = Provincia("bc")   # British Columbia
ab = Provincia("ab")   # Alberta
sk = Provincia("sk")   # Saskatchewan
mb = Provincia("mb")   # Manitoba
on = Provincia("on")   # Ontario
qc = Provincia("qc")   # Quebec
nl = Provincia("nl")   # Newfoundland and Labrador
nb = Provincia("nb")   # New Brunswick
pe = Provincia("pe")   # Prince Edward Island
ns = Provincia("ns")   # Nova Scotia
yt = Provincia("yt")   # Yukon
nt = Provincia("nt")   # Northwest Territories
nu = Provincia("nu")   # Nunavut


provinces = [bc, ab, sk, mb, on, qc, nl, nb, pe, ns, yt, nt, nu]


# Set up province neighbours (i.e. shares a border)
neighbours = [(bc, ab),
              (bc, nt),
              (bc, yt),
              (ab, sk),
              (ab, nt),
              (sk, mb),
              (sk, nt),
              (mb, on),
              (mb, nu),
              (on, qc),
              (qc, nb),
              (qc, nl),
              (nb, ns),
              (yt, nt),
              (nt, nu)]

# Initialize constraint satisfaction problem QUBO
csp = dwavebinarycsp.ConstraintSatisfactionProblem(dwavebinarycsp.BINARY)

not_both = {(0, 1), (1, 0), (0, 0)}
select_one = {(0, 0, 0, 1),
              (0, 0, 1, 0),
              (0, 1, 0, 0),
              (1, 0, 0, 0)}

# Apply one color constraint
for p in provinces:
    csp.add_constraint(select_one, {p.r, p.g, p.b, p.v})

# Apply no color sharing between neighbours
for x, y in neighbours:
    csp.add_constraint(not_both, {x.r, y.r})
    csp.add_constraint(not_both, {x.g, y.g})
    csp.add_constraint(not_both, {x.b, y.b})
    csp.add_constraint(not_both, {x.v, y.v})

# Combine constraints to form a BQM
Q = dwavebinarycsp.stitch(csp)

response=sampler.sample_qubo(Q, num_reads=50, label='Problema della mappa')
dwave.inspector.show(response)

risultato=response.first
print(risultato)
