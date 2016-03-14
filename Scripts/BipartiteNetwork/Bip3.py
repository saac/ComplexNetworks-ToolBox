import sys
# the mock-0.3.1 dir contains testcase.py, testutils.py & mock.py
sys.path.append('../../lib/')


#import netanalysis
#import netanalysis as analysis
#import netanalysis.sif
#from netanalysis import *
from netanalysis import Sif

import csv

import matplotlib.pyplot as plt
import numpy as np
from scipy.sparse import csc_matrix

import networkx as nx
from networkx.algorithms import bipartite


def leerCSV(archivo):
  d = []
  with open(archivo, 'rb') as csvfile:
    data = csv.reader(csvfile, delimiter=',')
    for cadena in data:
      d.append(cadena)
  return d

  
  
data = leerCSV(sys.argv[1])

coms = data[0]
coms = coms[1:]
#print coms

proces = []
for i in data:
  proces.append(i[0])
proces = proces[1:]

#print proces
#print len(proces)

B = nx.Graph()
B.add_nodes_from(coms, bipartite=0)
B.add_nodes_from(proces, bipartite=1)

  
for i in range(1,len(data),1):
  cadena = data[i]
  com = data[0]
  for j in range(1,len(cadena),1):
    if (float(cadena[j]) < 0.001):
      B.add_edges_from([(com[j],cadena[0].strip('"'))]) 
  

remove = [node for node,degree in B.degree().items() if degree == 0]
B.remove_nodes_from(remove)
#print remove
  
for node,degree in (B.degree().items()):
  if (degree == 0):
    #print node
    B.remove_node(node)
  


#print(bipartite.is_bipartite(B))  

Sif(B,"Bipartita_MEF2e")

bottom_nodes, top_nodes = bipartite.sets(B)


pos=nx.spring_layout(B)
#pos=nx.shell_layout(B)
#pos=nx.spectral_layout(B)
#pos=nx.random_layout(B)


nx.draw_networkx_nodes(B,pos,nodelist=bottom_nodes,node_shape='o',node_color='r', node_size=100) #proces
nx.draw_networkx_nodes(B,pos,nodelist=top_nodes,node_shape='p',node_color='y', node_size=450) #coms
nx.draw_networkx_edges(B,pos, edge_color='gray')
nx.draw_networkx_labels(B, pos,font_size=7, font_color='k')

plt.show()