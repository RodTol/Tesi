# Autore: Rodolfo Tolloi

# L'obbiettivo di questo programma è quello di colorare
# la mappa del Canada con 4 colori, assegnando colori diversi
# a regioni adiacenti. Per fare ciò creerò una QUBO 
# composta da due vincoli: il primo è quello di scegliere un
# solo colore per regione, mentre il secondo è di avere
# regioni confinanti con colori diversi. 
# Verrano utilizzate diverse librerie:
# -da dwawe.system verrano importati il sampler e il
# composite per l'embedding
# -dwave.inspector
# -pyqubo, per creare la formulazione matematica del problema
# -pprint, per visualizzare meglio i dati
# -networkx
# -matplotlib

# Importo il compiste per l'embedding e creo il sampler
from dwave.system import EmbeddingComposite, DWaveSampler
sampler = EmbeddingComposite(DWaveSampler(solver='Advantage_system1.1'))

# Analizzatore del d-wave
import dwave.inspector

# Importo da pyqubo le funzioni per creare i problemi
from pyqubo import Array, Binary
from pyqubo import  UserDefinedExpress

# Importo pprint e fisso delle impostazioni adatte
import pprint
pp = pprint.PrettyPrinter(indent=4)

# Importo networkx per creare i grafi
import networkx as nx

# Importo matplotlib per graficare i grafi
import matplotlib
matplotlib.use("agg")
import matplotlib.pyplot as plt

# Uso la funzione array di pyqubo per creare dei vettori
# di 4 variabili binarie, le quali rappresentano i colori, per ogni provincia
pi = Array.create('pi', shape=4, vartype='BINARY')   # Piemonte
va = Array.create('va', shape=4, vartype='BINARY')   # Valle d'Aosta
li = Array.create('li', shape=4, vartype='BINARY')   # Liguria
lo = Array.create('lo', shape=4, vartype='BINARY')   # Lombardia
ta = Array.create('ta', shape=4, vartype='BINARY')   # Trentino Alto Adige
ve = Array.create('ve', shape=4, vartype='BINARY')   # Veneto
fv = Array.create('fv', shape=4, vartype='BINARY')   # Friuli Venezia Giulia
er = Array.create('er', shape=4, vartype='BINARY')   # Emilia Romagna
to = Array.create('to', shape=4, vartype='BINARY')   # Toscana
ma = Array.create('ma', shape=4, vartype='BINARY')   # Marche
um = Array.create('um', shape=4, vartype='BINARY')   # Umbria
la = Array.create('la', shape=4, vartype='BINARY')   # Lazio
ab = Array.create('ab', shape=4, vartype='BINARY')   # Abruzzo 
mo = Array.create('mo', shape=4, vartype='BINARY')   # Molise  
ca = Array.create('ca', shape=4, vartype='BINARY')   # Campania  
pu = Array.create('pu', shape=4, vartype='BINARY')   # Puglia  
ba = Array.create('ba', shape=4, vartype='BINARY')   # Basilicata  
cl = Array.create('cl', shape=4, vartype='BINARY')   # Calabria
si = Array.create('si', shape=4, vartype='BINARY')   # Sicilia 
sa = Array.create('sa', shape=4, vartype='BINARY')   # Sardegna     

# Creo un vettore con all'interno tutte le provincie 
provinces = [pi, va, li, lo, ta, ve, fv, er, to, ma, um, la, ab,
    mo, ca, pu, ba, cl, si, sa]


# Creo un vettore con le coppie di provincie vicine
neighbours = [(pi, va),
              (pi, li),
              (pi, er),
              (pi, lo),
              (lo, er),
              (lo, ve),
              (lo, ta),
              (ve, ta),
              (ve, fv),
              (ve, er),
              (er, li),
              (er, ma),
              (er, to),
              (to, li),
              (to, ma),
              (to, um),
              (to, la),
              (ma, um),
              (ma, la),
              (ma, ab),
              (la, um),
              (la, ca),
              (la, mo),
              (la, ab),
              (ab, mo),
              (mo, pu),
              (mo, ca),
              (ca, pu),
              (ca, ba),
              (ba, cl),
              (ba, pu),]

# Creo una funzione che, dato un vettore di variabili, crea
# l'equazione che rappresenta il vincolo di scelta di un solo colore
class one_color(UserDefinedExpress):
 def __init__(self, a):
    express = (a[0]+a[1]+a[2]+a[3]-1)**2
    super().__init__(express)

# Creo la prima parte dell'Hamiltoniana unendo i vincoli di tutte 
# le 13 provincie
H1=one_color(provinces[len(provinces)-1])
for i in range(len(provinces)-1):
    H1=H1+one_color(provinces[i])

# Creo la funzione che, data una coppia di vettori, crea la funzione
# che penalizza il fatto che questi siano dello stesso colore
class colori_diversi(UserDefinedExpress):
 def __init__(self, a, b):
    express = a[0]*b[0]+a[1]*b[1]+a[2]*b[2]+a[3]*b[3]
    super().__init__(express)

# Creo la seconda parte dell'Hamiltoniana creando e unendo 
# tutti i vincoli per le coppie di provincie vicine
H2=colori_diversi(neighbours[len(neighbours)-1][0],neighbours[len(neighbours)-1][1])
for i in range(len(neighbours)-1):
    H2=H2+colori_diversi(neighbours[i][0],neighbours[i][1])

# Creo l'Hamiltoniana e la faccio diventare una BQM
model = H1+H2
bqm = model.compile().to_bqm()


# Creo il set dei risultati utilizzando il sampler definito prima
chainstrenght= None
sampleset = sampler.sample(bqm, num_reads = 20, chain_strength=chainstrenght, label="Problema della mappa")

#risultati
#print(sampleset)

# Uso l'inspector
dwave.inspector.show(sampleset)

# Seleziono il risultato migliore, ossia quello a energia minore
risultato = sampleset.first.sample

#print(risultato)
#print(risultato[0])

# Creo un grafo vuoto
G = nx.Graph()

# Creo un vettore con i nodi e uno con gli archi
nodes=  ['pi',
        'va',
        'li',
        'lo',
        'ta',
        've',
        'fv',
        'er',
        'to',
        'ma',
        'um',
        'la',
        'ab',
        'mo',
        'ca',
        'pu',
        'ba',
        'cl',
        'si',
        'sa']
    

edges =[('pi', 'va'),
              ('pi', 'li'),
              ('pi', 'er'),
              ('pi', 'lo'),
              ('lo', 'er'),
              ('lo', 've'),
              ('lo', 'ta'),
              ('ve', 'ta'),
              ('ve', 'fv'),
              ('ve', 'er'),
              ('er', 'li'),
              ('er', 'ma'),
              ('er', 'to'),
              ('to', 'li'),
              ('to', 'ma'),
              ('to', 'um'),
              ('to', 'la'),
              ('ma', 'um'),
              ('ma', 'la'),
              ('ma', 'ab'),
              ('la', 'um'),
              ('la', 'ca'),
              ('la', 'mo'),
              ('la', 'ab'),
              ('ab', 'mo'),
              ('mo', 'pu'),
              ('mo', 'ca'),
              ('ca', 'pu'),
              ('ca', 'ba'),
              ('ba', 'cl'),
              ('ba', 'pu'),]

# Creo il grafo che rappresenta la mappa del Canada              
G.add_nodes_from(nodes)
G.add_edges_from(edges)

# Creo un vettore i cui elementi sono il nome della provincia
# e il colore assegnato, sotto forma di numero
color_labels = [k for k, v in risultato.items() if v == 1]

# Divido l'elemento del vettore in nome e colore
for i in range(len(color_labels)):
        name = color_labels[i][:2]
        color = color_labels[i][3]
        G.nodes[name]["color"] = color

# Creo un vettore di dimensioni 13 con ogni colore associato alla provincia,
# sempre in forma di numero
color_map = [color for name, color in G.nodes(data="color")]

# Sostituisco il numero che indica il colore con la stringa
# intepretabile da networkx 
print(color_map)
for i in range(20):
    color_map[i]=color_map[i].replace('0','red')
    color_map[i]=color_map[i].replace('1','blue')
    color_map[i]=color_map[i].replace('2','green')
    color_map[i]=color_map[i].replace('3','violet')
print(color_map)    

# Creo un vettore con le posizioni dei nodi nel grafico
node_positions = {'pi': (0, 7),
        'va': (0, 8),
        'li': (1.5, 6),
        'lo': (1.5, 8),
        'ta': (3, 9),
        've': (4.5, 8),
        'fv': (5.5, 8),
        'er': (3, 7),
        'to': (3, 5),
        'ma': (6, 6),
        'um': (4.5, 5),
        'la': (6, 4),
        'ab': (7.5, 5),
        'mo': (7.5, 4),
        'ca': (7.5, 3),
        'pu': (9, 4),
        'ba': (9, 3),
        'cl': (9, 2),
        'si': (6, 2),
        'sa': (1.5, 4)} 

# Creo il grafico del grafo
nx.draw_networkx(G, pos=node_positions, with_labels=True,
                   node_color=color_map, font_color="w", node_size=400)

# Salvo il grafo in un file
filename = "/workspace/Tesi/Esempio-Mappa/mappa-colorata.png"
plt.savefig(filename)
print("The graph is saved in '{}'.".format(filename))

