import sys
from numpy import *
#import pylab as pl
#import matplotlib.pyplot as plt
import networkx as nx
#import numpy as np


def separador(sep):
  
  if (sep == "cma"):
    sep = ","
  elif (sep == "tab"):
    sep = "\t"
  elif (sep == "spa"):
    sep = " "
    
  return sep

#def GetNetX(red,sep='tab',form='nIn'):
def GetNetX(red,sep,form):

  diccionario = {}
  genesDIC = []
  G = nx.Graph()

  sep = separador(sep)
  
  interacciones = open(red).readlines()

  k = 1
  tmp="---"
  for i in interacciones:
      genes = i.split(sep)
      
      a=genes[0].strip()
      b=genes[1].strip()
      if (form != 'nn'):
          c=genes[2].strip()    
      
      #print sep

      #if (form == "nn"):
        #a=genes[0].strip()
        #b=genes[1].strip()
      #else:
        #a=genes[0].strip()
        #b=genes[1].strip()
        #c=genes[2].strip()
        
    
      
      
      
      if (form == "nIn"):
	if (genes[0].strip() not in genesDIC): genesDIC.append(genes[0].strip())
	if (genes[2].strip() not in genesDIC): genesDIC.append(genes[2].strip())
	
      elif (form == "nnI"):      
	if (genes[0].strip() not in genesDIC): genesDIC.append(genes[0].strip())
	if (genes[1].strip() not in genesDIC): genesDIC.append(genes[1].strip())
	
      elif (form == "nn"):
	if (genes[0].strip() not in genesDIC): genesDIC.append(genes[0].strip())
	if (genes[1].strip() not in genesDIC): genesDIC.append(genes[1].strip())
	
      

  i = 1
  for n in genesDIC:
      diccionario[n] = i
      #SALIDA.write('%s "%s" \n' % (i,n))
      i+=1

      
  for i in interacciones:
      campos  = i.split(sep)

      a=campos[0].strip()
      b=campos[1].strip()
      if (form != 'nn'):
          c=campos[2].strip()
      
      if (form == "nIn"):
	if (b == "pp"):
	  b = 1
	else:
	  b=float(b)
	if (a in diccionario and c in diccionario):
	  if (diccionario[a] == diccionario[c]):
	    G.add_node(diccionario[a])
	  else:
	    if ((G.has_edge(diccionario[a],diccionario[c]) == False) and (G.has_edge(diccionario[c],diccionario[a]) == False)):
	      G.add_edge(diccionario[a],diccionario[c],w=b)
      
      elif (form == "nnI"):
	if (c == "pp"):
	  c = 1
	else:
	  c=float(c)
	if (a in diccionario and b in diccionario):
	  if (diccionario[a] == diccionario[b]):
	    G.add_node(diccionario[a])
	  else:
	    if ((G.has_edge(diccionario[a],diccionario[b]) == False) and (G.has_edge(diccionario[b],diccionario[a]) == False)):
	      G.add_edge(diccionario[a],diccionario[b],w=c)
	      
      elif (form == "nn"):
	c = 1
	if (a in diccionario and b in diccionario):
	  if (diccionario[a] == diccionario[b]):
	    G.add_node(diccionario[a])
	  else:
	    if ((G.has_edge(diccionario[a],diccionario[b]) == False) and (G.has_edge(diccionario[b],diccionario[a]) == False)):
	      G.add_edge(diccionario[a],diccionario[b],w=c)
  
	
  return G


def NetStats(G,name):
    
    s=0
    d = nx.degree(G)    
    for i in d.values():
        s = s + i
    
    n = len(G.nodes())
    m = len(G.edges())
    k = float(s)/float(n)
    #k = nx.average_node_connectivity(G)
        
    C = nx.average_clustering(G)
    l = nx.average_shortest_path_length(G)
    Cc = nx.closeness_centrality(G)
    d = nx.diameter(G) #The diameter is the maximum eccentricity.
    r = nx.radius(G) #The radius is the minimum eccentricity.


    
    output = "ESTADISITICOS_"+name
    SALIDA = open(output,"w")
    
    SALIDA.write(("Numero de nodos n = %s \n") %  n)
    SALIDA.write(("Numero de aristas m = %s \n") %  m)
    SALIDA.write(("Grado promedio <k> = %s \n") %  k)
        
    SALIDA.write(("Clustering Coeficient = %s \n") %  C)
    SALIDA.write(("Shortest Path Length = %s \n") %  l)
    #SALIDA.write(("Closeness = %s \n") %  Cc)
    SALIDA.write(("Diameter (maximum eccentricity) = %d \n") %  d)
    SALIDA.write(("Radius (minimum eccentricity) = %d \n") %  r)
    

red = sys.argv[1].split('.')
nombre = red[0]

print red[1]
print sys.argv[1]

if (red[1] == 'sif'):
    sep = raw_input("Separador = ")
    form = raw_input("Forma = ")
    G = GetNetX(sys.argv[1],sep,form)
    #G = GetNetX(sys.argv[1])
else:
    G = nx.read_gpickle(sys.argv[1])


NetStats(G,nombre)